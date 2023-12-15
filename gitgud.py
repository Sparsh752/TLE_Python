# Importing the required libraries
import requests
import discord
from bs4 import BeautifulSoup
from db import find_solved_codeforces, get_codeforces_handle, get_atcoder_handle, get_current_question, delete_current_question
from db import problem_solving_cf, problem_solving_ac, find_solved_atcoder, update_point_cf, update_point_at
from db import add_in_gitgud_list, get_gitgud_list
from random_question import cf_get_random_question_rating, ac_get_random_question, cf_get_random_question_tag
import datetime
import math

# returns a problem of given contest id and index from codeforces
async def get_problem_cf(contest_id, problem_index):

    url = 'https://codeforces.com/api/problemset.problems'
    # get the response from the url
    response = requests.get(url)
    data = response.json()
    # problems from the api
    problems = data['result']['problems']
    for problem in problems:
        # if problem has required contest id and index
        if problem['contestId'] == int(contest_id) and problem['index'] == str(problem_index):
            return (problem['name'], problem['rating'], 'https://codeforces.com/contest/'+str(contest_id)+'/problem/'+str(problem_index))
    # if no problem is found in API call with the required parameters
    return None


# returns a problem of given contest id and index from codeforces
async def get_problem_atcoder(contest_id, problem_index):
    url = 'https://kenkoooo.com/atcoder/resources/problems.json'
    # get the response from the url
    response = requests.get(url)
    # problems from the api
    data = response.json()
    problem_id = str(contest_id)+'_'+str(problem_index)
    for problem in data:
        # if problem has required contest id and index
        if problem['contest_id'] == str(contest_id) and str(problem['problem_index']).capitalize() == str(problem_index).capitalize():
            # get the difficulty of the problem
            difficulty = await get_ac_problem_difficulty(problem_id)
            difficulty = int(difficulty)
            return (problem['name'], difficulty, 'https://atcoder.jp/contests/'+str(contest_id)+'/tasks/'+str(problem_id))
    # if no problem is found in API call with the required parameters
    return None

# returns the current rating of the given codeforces handle
async def get_cf_user_rating(codeforces_handle):
    url = f'https://codeforces.com/api/user.rating?handle={codeforces_handle}'
    data = requests.get(url).json()
    if data['status'] == 'OK':
        return data['result'][-1]['newRating']
    else:
        return None


# returns the current rating of the given atcoder handle
async def get_ac_user_rating(atcoder_handle):
    url = f'https://atcoder.jp/users/{atcoder_handle}/history/json'
    data = requests.get(url).json()
    return data[-1]['NewRating']


# returns the difficulty of the problem based on kenkoooo
async def get_ac_problem_difficulty(problem_id):
    url = f'https://kenkoooo.com/atcoder/resources/problem-models.json'
    data = requests.get(url).json()
    return data[problem_id]['difficulty']


# converts atcoder's ratings to codeforces
async def convertAC2CFrating(a):
    x1 = 0
    x2 = 3900
    y1 = -1000 + 60
    y2 = 4130 + 85
    res = ((x2 * (a - y1)) + (x1 * (y2 - a))) / (y2 - y1)
    return res

# gets random question from codeforces and atcoder according to the request of the user
async def gitgud(ctx):
    user_message = ctx.content
    user_message = user_message.split()
    msg= await ctx.channel.send(f"{ctx.author.mention} Checking the correctness of command")
    if(len(user_message) < 2):
        await msg.edit(content=f"{ctx.author.mention} Command format is incorrect")
        return
    if(user_message[1] not in ['cf', 'ac']):  # second word in the command should be either cf or ac
        await msg.edit(content=f"{ctx.author.mention} Please specify the judge correctly. It can be either `cf` or `ac`")
        return
    if(user_message[1] == 'cf'): # if codeforces is chosen as the judge
        cf_handle = await get_codeforces_handle(ctx) # getting the cf handle of the discord user
        points = 8
        if(cf_handle == None):
            await msg.edit(content=f"{ctx.author.mention} You have not identified your codeforces handle. First do it using ;identify_cf <handle>")
            return
        problem = await get_current_question(ctx.author.id, 'cf') # checking if any question is already assigned to the user
        if problem != None:
            await msg.edit(content=f"{ctx.author.mention} You already have a problem assigned to you. Please use ;nogud cf to remove it.")
            return
        cf_rating = await get_cf_user_rating(cf_handle)
        cf_rating = (cf_rating//100)*100
        solved_problems = await find_solved_codeforces(ctx, cf_handle)
        # giving points according to the difficulty of the question and rating of the user
        if(len(user_message) == 3):
            if(user_message[2] not in ['+100', '+200', '+300', '+400']):
                await msg.edit(content=f"{ctx.author.mention} Please specify the rating with +100, +200, +300 or +400 only")
                return
            if(user_message[2] == '+100'):
                points = 12
            elif(user_message[2] == '+200'):
                points = 17
            elif(user_message[2] == '+300'):
                points = 23
            elif(user_message[2] == '+400'):
                points = 30
            cf_rating += (int(user_message[2][1:]))
        if(cf_rating < 1000):
            cf_rating = 1000
            points = 12
        await msg.edit(content=f"Wait {ctx.author.mention} the bot is thinking :thinking: a problem for you.......")
        # getting a random question from codeforces
        random_problem = cf_get_random_question_rating(cf_rating)
        iter = 0
        while(iter < 50 and random_problem['prob_id'] in solved_problems):
            random_problem = cf_get_random_question_rating(cf_rating)
            iter += 1
        if(iter == 50):
            await msg.edit(content=f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :frowning2: ")
            return
        title = f"Contest {random_problem['prob_id']} {random_problem['prob_name']}"
        url = f"{random_problem['prob_link']}"
        description = f"Rating: {random_problem['prob_rating']} | You will get {points} points for solving this problem"
        embed = discord.Embed(title=title, url=url, description=description)
        await msg.edit(content=f"Challenge problem for `{cf_handle}`", embed=embed)
        await problem_solving_cf(ctx, random_problem['prob_id'], points)
    else: # if atcoder is chosen as the judge
        ac_handle = await get_atcoder_handle(ctx) # getting the atcoder handle of the discord user
        ac_rating = await get_ac_user_rating(ac_handle) 
        if(ac_handle == None):
            await msg.edit(content=f"{ctx.author.mention} You have not identified your atcoder handle. First do it using ;identify_ac <handle>")
            return
        problem = await get_current_question(ctx.author.id, 'ac')  # checking if any question is already assigned to the user
        if problem != None:
            await msg.edit(content=f"{ctx.author.mention} You already have a problem assigned to you. Please use ;nogud ac to remove it.")
            return
        if(len(user_message) < 4):
            await msg.edit(content=f"{ctx.author.mention} Please specify the contest and problem number For example `;gitgud ac abc e` for 'E' problem of 'ABC' contest")
            return
        await msg.edit(content=f"Wait {ctx.author.mention} the bot is thinking :thinking: a problem for you.......")
        # getting random question for the user from atcoder
        solved_problems = await find_solved_atcoder(ctx,ac_handle)
        # random problem based on the type of contest and problem number
        random_problem = ac_get_random_question(
            user_message[2], user_message[3])
        if random_problem is None:
            await msg.edit(content=f"{ctx.author.mention} Sorry I don't think I can give you problem of this type. Please try again later with some other type :frowning2: ")
            return
        iter = 0
        while(iter < 50 and random_problem["problem"]["id"] in solved_problems):
            random_problem = ac_get_random_question(
                user_message[2], user_message[3])
            difficulty = await get_ac_problem_difficulty(random_problem['problem']['id'])
            if difficulty is None:
                random_problem = None
            iter += 1
        if(iter == 50):
            await msg.edit(content=f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :frowning2: ")
            return
        # finding eqvivalent codeforces rating for the problem
        difficulty = await get_ac_problem_difficulty(random_problem['problem']['id'])
        equv_cf_rating = await convertAC2CFrating(ac_rating)
        equv_cf_prob_rating = await convertAC2CFrating(int(difficulty))
        points = 0
        delta = equv_cf_prob_rating-equv_cf_rating
        # print(equv_cf_prob_rating)
        # print(equv_cf_rating)
        # deciding the points based on the difficulty of the problem
        if(delta < 0):
            points = 2
        elif(delta < 100):
            points = 8
        elif(delta < 200):
            points = 12
        elif(delta < 300):
            points = 17
        elif(delta < 400):
            points = 23
        else:
            points = 30
        title = f"{random_problem['problem']['title']}"
        url = f"{random_problem['prob_link']}"
        desc = f'You will get {points} points for solving this problem'
        await msg.edit(content=f"Challenge problem for `{ac_handle}`", embed=discord.Embed(title=title, url=url, description=desc))
        await problem_solving_ac(ctx, random_problem['problem']['id'], points)


# returns true or false based on whether or not given problem is solved by given cf_handle on given platform
async def check_if_solved(ctx, cf_handle, problem, platform):
    if(platform == 'cf'):
        
        # list of all solved problems on codeforces
        solved_problems = await find_solved_codeforces(ctx, cf_handle)
        if(problem[0] in solved_problems):
            return True
        else:
            return False
    else:
        last_checked, last_solved_problems = await get_last_solved_problems(ctx, 'atcoder')
        # list of all solved problems on atcoder
        solved_problems = await find_solved_atcoder(ctx, cf_handle)
        if(str(problem[0]) in solved_problems):
            return True
        else:
            return False

# returns true or false based on current_question is done by ac_handle or not
async def check_if_solved_ac(ctx, ac_handle, current_question):
    url = 'https://atcoder.jp/contests/'+str(current_question[0][:-2])+'/submissions?f.Task='+str(current_question[0])+'&f.LanguageName=&f.Status=AC&f.User='+str(ac_handle)
    response = requests.get(url.encode('utf-8'))
    check1=response.text.find('No Submissions')
    print(check1)
    if check1 != -1:
        return False
    else:
        return True

# checks the status of the problem given to the user by gitgud and updates the points of the user
async def gotgud(ctx):
    user_message = ctx.content
    user_message = user_message.split()
    msg = await ctx.channel.send(f'{ctx.author.mention} Checking the correctness of your command....')
    if(len(user_message) < 2):
        await msg.edit(content=f"{ctx.author.mention} Command format is incorrect")
        return
    if(user_message[1] not in ['cf', 'ac']):
        await msg.edit(content=f"{ctx.author.mention} Please specify the judge correctly. It can be either `cf` or `ac`")
        return
    if(user_message[1] == 'cf'): # if codeforces is chosen as the judge
        id = ctx.author.id
        cf_handle = await get_codeforces_handle(ctx) # getting the cf handle of the discord user
        if(cf_handle == None):
            await msg.edit(content=f"{ctx.author.mention} You have not identified your codeforces handle. First do it using ;identify_cf <handle>")
            return
        # getting the current question assigned to the user
        current_question = await get_current_question(id, 'cf') 
        if(current_question == None):
            await msg.edit(content=f"{ctx.author.mention} You have not been given any problem yet. Please use ;gitgud cf to get a problem :slight_smile: ")
            return
        await msg.edit(content=f"{ctx.author.mention} Checking :face_with_monocle: if you have solved the problem....")
        # checking if the problem is solved by the user or not
        check = await check_if_solved(ctx, cf_handle, current_question, 'cf')
        if(check):
            # if solved then update the points of the user
            await update_point_cf(ctx, current_question[2])
            await add_in_gitgud_list(id, 'cf', current_question)
            time_date = str(current_question[1])
            time = datetime.datetime.now() - datetime.datetime(int(time_date[0:4]), int(time_date[5:7]), int(
                time_date[8:10]), int(time_date[11:13]), int(time_date[14:16]), int(time_date[17:19], 0))
            await msg.edit(content=f"{ctx.author.mention} Congratulations! :partying_face: You have solved the problem. You have been awarded {current_question[2]} points and it took you {int(time.total_seconds()/3600)} hours {int((time.total_seconds()%3600)/60)} minutes {int(time.seconds%60)} seconds")
            return
        else:
            # if not solved then ask the user to try again later
            await msg.edit(content=f"{ctx.author.mention} You have not solved the problem yet :expressionless:. Please try again later")
            return
    else: # if atcoder is chosen as the judge
        id = ctx.author.id
        ac_handle = await get_atcoder_handle(ctx) # getting the atcoder handle of the discord user
        if(ac_handle == None):
            await msg.edit(content=f"{ctx.author.mention} You have not identified your atcoder handle. First do it using ;identify_ac <handle>")
            return
        # getting the current question assigned to the user
        current_question = await get_current_question(id, 'ac')
        if(current_question == None):
            await msg.edit(content=f"{ctx.author.mention} You have not been given any problem yet. Please use ;gitgud ac to get a problem :slight_smile: ")
            return
        # checking if the problem is solved by the user or not
        check = await check_if_solved_ac(ctx, ac_handle, current_question)
        print(check)
        if(check):
            # if solved then update the points of the user
            await update_point_at(ctx, current_question[2])
            await add_in_gitgud_list(id, 'ac', current_question)
            await msg.edit(content=f"{ctx.author.mention} Congratulations! :partying_face: You have solved the problem. You have been awarded {current_question[2]} points")
            return
        else:
            # if not solved then ask the user to try again later
            await msg.edit(content=f"{ctx.author.mention} You have not solved the problem yet :expressionless: . Please try again later")
            return

# removes the current question assigned to the user after 2 hours of assigning
async def nogud_cf(ctx):
    # getting the current question assigned to the user
    problem = await get_current_question(ctx.author.id, 'cf')
    if(problem == None):
        return ctx.author.mention+" Currently you don't have any problem use ;gitgud cf to get a problem :slight_smile:"
    
    time_date = str(problem[1])
    try:
        # calculating the time difference between the time when the problem was assigned and current time
        time_passed = datetime.datetime.now() - datetime.datetime.strptime(time_date,"%Y-%m-%d %H:%M:%S.%f+00:00")
    except Exception as e:
        print(e)  
    if time_passed.total_seconds() > 7200:
        # if time difference is greater than 2 hours then remove the problem from the database
        await delete_current_question(ctx.author.id, 'cf')
        await ctx.channel.send(f"{ctx.author.mention} Challenge skipped :confused:")
        return
    else:
        # if time difference is less than 2 hours then ask the user to try again later
        await ctx.channel.send(f"{ctx.author.mention} Think more you can skip the problem in "+ str(math.ceil((7200-time_passed.total_seconds())/60)) +" minutes :thinking:")
        return 

# removes the current question assigned to the user after 1 hour of assigning
async def nogud_atcoder(ctx):
    # getting the current question assigned to the user
    problem = await get_current_question(ctx.author.id, 'atcoder')
    if problem == None:
        return ctx.author.mention+" Currently you don't have any problem use ;gitgud ac to get a problem :slight_smile:"
    time_date = str(problem[1])
    try:
        # calculating the time difference between the time when the problem was assigned and current time
        time_passed = datetime.datetime.now() - datetime.datetime.strptime(time_date,"%Y-%m-%d %H:%M:%S.%f+00:00")
    except Exception as e:
        print(e)
    if time_passed.total_seconds() > 3600:
        # if time difference is greater than 1 hour then remove the problem from the database
        await delete_current_question(ctx.author.id, 'atcoder')
        return ctx.author.mention+' Challenge skipped :confused:'
    else:
        # if time difference is less than 1 hour then ask the user to try again later
        return ctx.author.mention+' Think more you can skip the problem in '+str(math.ceil((3600-time_passed.total_seconds())/60))+' minutes :thinking:'


# returns the list of all the problems solved by the user using gitgud
async def gitlog(ctx):
    user_message = ctx.content
    user_message = user_message.split()
    msg= await ctx.channel.send(f"{ctx.author.mention} Checking command format ")
    if(len(user_message) < 2):
        await msg.edit(content=f"{ctx.author.mention} Command format is incorrect")
        return "error","error"
    if(user_message[1] not in ['cf', 'ac']):
        await msg.edit(content=f"{ctx.author.mention} Please specify the judge correctly. It can be either `cf` or `ac`")
        return "error","error"
    await msg.edit(content=f"{ctx.author.mention} Fetching your gitgud list :hourglass_flowing_sand:")
    if(user_message[1] == 'cf'): # if codeforces is chosen as the judge
        id = ctx.author.id
        # getting the list of all the problems solved by the user
        problems = await get_gitgud_list(id, 'cf')
        all_problems = []
        i = 0
        # getting the details of all the problems solved by the user, and forming an array of dictionaries
        while i < len(problems):
            problem = [problems[i], problems[i+1], problems[i+2]]
            contest_id = problem[0][:-2]
            problem_index = problem[0][-1]
            my_problem = await get_problem_cf(contest_id, problem_index)
            all_problems.append((my_problem, problem[1], problem[2]))
            i = i+3
        l = []
        for problem in all_problems:
            mydict = {}
            mydict['Problem Name'] = f'[{problem[0][0]}]({problem[0][2]})'
            mydict['Problem Rating'] = problem[0][1]
            mydict['Points'] = problem[2]
            l.append(mydict)
        return l, msg
    else: # if atcoder is chosen as the judge
        id = ctx.author.id
        # getting the list of all the problems solved by the user
        problems = await get_gitgud_list(id, 'ac')
        all_problems = []
        i = 0
        # getting the details of all the problems solved by the user, and forming an array of dictionaries
        while i < len(problems):
            problem = [problems[i], problems[i+1], problems[i+2]]
            contest_id = problem[0][:-2]
            problem_index = problem[0][-1]
            my_problem = await get_problem_atcoder(contest_id, problem_index)
            all_problems.append((my_problem, problem[1], problem[2]))
            i += 3
        l = []
        for problem in all_problems:
            mydict = {}
            mydict['Problem Name'] =  f'[{problem[0][0]}]({problem[0][2]})'
            mydict['Problem Rating'] = problem[0][1]
            mydict['Points'] = problem[2]
            l.append(mydict)
        return l, msg


# gives the user a problem of given tag and rating
async def gimme(ctx):
    user_message = ctx.content
    user_message = user_message.split()
    msg = await ctx.channel.send(f"{ctx.author.mention} Checking command format ")
    cf_handle = await get_codeforces_handle(ctx) # getting the cf handle of the discord user
    points = 8
    if(cf_handle == None):
        await msg.edit(content=f"{ctx.author.mention} Please set your codeforces handle first")
        return
    
    cf_rating = await get_cf_user_rating(cf_handle) # getting the current rating of the user
    cf_rating = (cf_rating//100)*100
    
    solved_problems = await find_solved_codeforces(ctx, cf_handle)
    # giving points according to the difficulty of the question and rating of the user
    if(len(user_message) == 3):
        if(user_message[2] not in ['+100', '+200', '+300', '+400']):
            await msg.edit(content=f"{ctx.author.mention} Please specify the rating with +100, +200, +300 or +400 only")
            return
        if(user_message[2] == '+100'):
            points = 12
        elif(user_message[2] == '+200'):
            points = 17
        elif(user_message[2] == '+300'):
            points = 23
        elif(user_message[2] == '+400'):
            points = 30
        cf_rating += (int(user_message[2][1:]))
    await msg.edit(content=f"{ctx.author.mention} Thinking of a problem of {user_message[1]} for you :thinking:")
    if(cf_rating < 1000):
        cf_rating = 1000
        points = 12
    random_problem = cf_get_random_question_tag(user_message[1], cf_rating)
    if random_problem == None:
        await msg.edit(content=f"{ctx.author.mention} Sorry we could not give you a problem of this tag in this rating range. Please try with some other rating range :frowning: ")
        return
    iter = 0
    while(iter < 50 and random_problem['prob_id'] in solved_problems):
        random_problem = cf_get_random_question_tag(user_message[1], cf_rating)
        iter += 1
    if(iter == 50):
        await msg.edit(content=f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :frowning: ")
        return
    title = f"Contest {random_problem['prob_id']} {random_problem['prob_name']}"
    url = f"{random_problem['prob_link']}"
    description = f"Rating: {random_problem['prob_rating']} | You will get {points} points for solving this problem"
    embed = discord.Embed(title=title, url=url, description=description)
    await msg.edit(content=f"Challenge problem for `{cf_handle}`", embed=embed)
    await problem_solving_cf(ctx, random_problem['prob_id'], points)
