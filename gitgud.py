import requests
import discord
from db import get_last_solved_problems, find_solved_codeforces, get_codeforces_handle, get_atcoder_handle, get_current_question,delete_current_question
from db import problem_solving_cf, problem_solving_ac, find_solved_atcoder, update_point_cf, update_point_at
from codeforces_scraping import cf_get_random_question_rating, ac_get_random_question
import asyncio
import datetime
async def get_cf_user_rating(codeforces_handle):
    url = f'https://codeforces.com/api/user.rating?handle={codeforces_handle}'
    data = requests.get(url).json()
    if data['status'] == 'OK':
            return data['result'][-1]['newRating']
    else:
            return None
async def get_ac_user_rating(atcoder_handle):
    url = f'https://atcoder.jp/users/{atcoder_handle}/history/json'
    data = requests.get(url).json()
    return data[-1]['NewRating']

async def get_ac_problem_difficulty(problem_id):
    url = f'https://kenkoooo.com/atcoder/resources/problem-models.json'
    data = requests.get(url).json()
    return data[problem_id]['difficulty']

async def convertAC2CFrating(a):
    x1 = 0
    x2 = 3900
    y1 = -1000 + 60
    y2 = 4130 + 85
    res = ((x2 * (a - y1)) + (x1 * (y2 - a))) / (y2 - y1)
    return res

async def gitgud(ctx):
    user_message = ctx.content
    user_message = user_message.split()
    if(len(user_message)<2):
        await ctx.channel.send(f"{ctx.author.mention} Command format is incorrect")
        return
    if(user_message[1] not in ['cf','ac']):
        await ctx.channel.send(f"{ctx.author.mention} Please specify the judge correctly. It can be either `cf` or `ac`")
        return
    if(user_message[1]=='cf'):
        cf_handle = await get_codeforces_handle(ctx)
        points = 8
        if(cf_handle==None):
            await ctx.channel.send(f"{ctx.author.mention} You have not identified your codeforces handle. First do it using ;identify_cf <handle>")
            return
        cf_rating = await get_cf_user_rating(cf_handle)
        cf_rating = (cf_rating//100)*100
        last_checked,last_solved_problems = await get_last_solved_problems(ctx,'codeforces')
        solved_problems = await find_solved_codeforces(ctx,cf_handle,last_solved_problems,last_checked)
        if(len(user_message)==3):
            if(user_message[2] not in ['+100','+200','+300','+400']):
                await ctx.channel.send(f"{ctx.author.mention} Please specify the rating with +100, +200, +300 or +400 only")
                return
            if(user_message[2]=='+100'):
                points = 12
            elif(user_message[2]=='+200'):
                points = 17
            elif(user_message[2]=='+300'):
                points = 23
            elif(user_message[2]=='+400'):
                points = 30
            cf_rating+=(int(user_message[2][1:]))
        if(cf_rating<1000):
            cf_rating=1000
            points = 12
        random_problem = cf_get_random_question_rating(cf_rating)
        iter=0
        while(iter < 50 and random_problem in solved_problems):
            random_problem = cf_get_random_question_rating(cf_rating)
            iter+=1
        if(iter==50):
            await ctx.channel.send(f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :( ")
            return
        title = f"Contest {random_problem['prob_id']} {random_problem['prob_name']}"
        url = f"{random_problem['prob_link']}"
        description = f"Rating: {random_problem['prob_rating']} | You will get {points} points for solving this problem"
        embed = discord.Embed(title=title, url=url, description=description)
        await ctx.channel.send(f"Challenge problem for `{cf_handle}`", embed = embed)
        await problem_solving_cf(ctx,random_problem['prob_id'],points)
    else:
        ac_handle = await get_atcoder_handle(ctx)
        ac_rating = await get_ac_user_rating(ac_handle)
        if(ac_handle==None):
            await ctx.channel.send(f"{ctx.author.mention} You have not identified your atcoder handle. First do it using ;identify_ac <handle>")
            return
        if(len(user_message)<4):
            await ctx.channel.send(f"{ctx.author.mention} Please specify the contest and problem number")
            await ctx.channel.send(f"{ctx.author.mention} For example `;gitgud ac abc e` for 'E' problem of 'ABC' contest")
            return
        last_checked, last_solved_problems = await get_last_solved_problems(ctx,'atcoder')
        solved_problems = await find_solved_atcoder(ctx,ac_handle,last_solved_problems,last_checked)
        random_problem = ac_get_random_question(user_message[2], user_message[3])
        iter=0
        while(iter < 50 and random_problem in solved_problems):
            random_problem = ac_get_random_question(user_message[2], user_message[3])
            difficulty = await get_ac_problem_difficulty(random_problem['problem']['id'])
            if difficulty is None :
                random_problem = None
            iter+=1
        if(iter==50):
            await ctx.channel.send(f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :( ")
            return
        difficulty = await get_ac_problem_difficulty(random_problem['problem']['id'])
        equv_cf_rating = await convertAC2CFrating(ac_rating)
        equv_cf_prob_rating = await convertAC2CFrating(int(difficulty))
        points = 0
        delta = equv_cf_prob_rating-equv_cf_rating
        print(equv_cf_prob_rating)
        print(equv_cf_rating)
        if(delta<0):
            points = 2
        elif(delta<100):
            points = 8
        elif(delta<200):
            points = 12
        elif(delta<300):
            points = 17
        elif(delta<400):
            points = 23
        else:
            points = 30
        title = f"{random_problem['problem']['title']}"
        url = f"{random_problem['prob_link']}"
        desc = f'You will get {points} points for solving this problem'
        await ctx.channel.send(f"Challenge problem for `{ac_handle}`", embed = discord.Embed(title=title, url=url, description=desc))
        await problem_solving_ac(ctx,random_problem['problem']['id'],points)

async def check_if_solved(ctx, cf_handle, problem, platform):
    if(platform=='cf'):
        last_checked, last_solved_problems = await get_last_solved_problems(ctx,'codeforces')
        solved_problems = await find_solved_codeforces(ctx,cf_handle,last_solved_problems,last_checked)
        if(problem[0] in solved_problems):
            return True
        else:
            return False
    else:
        last_checked, last_solved_problems = await get_last_solved_problems(ctx,'atcoder')
        solved_problems = await find_solved_atcoder(ctx,cf_handle,last_solved_problems,last_checked)
        if(problem[0] in solved_problems):
            return True
        else:
            return False

async def gotgud(ctx):
    user_message = ctx.content
    user_message = user_message.split()
    if(len(user_message)<2):
        await ctx.channel.send(f"{ctx.author.mention} Command format is incorrect")
        return
    if(user_message[1] not in ['cf','ac']):
        await ctx.channel.send(f"{ctx.author.mention} Please specify the judge correctly. It can be either `cf` or `ac`")
        return
    if(user_message[1]=='cf'):
        id = ctx.author.id
        current_question = await get_current_question(id,'cf')
        if(current_question==None):
            await ctx.channel.send(f"{ctx.author.mention} You have not been given any problem yet. Please use ;gitgud cf to get a problem")
            return
        cf_handle = await get_codeforces_handle(ctx)
        check = await check_if_solved(ctx,cf_handle,current_question,'cf')
        if(check):
            await update_point_cf(ctx,current_question[2])
            time = datetime.datetime.now() - current_question[0]
            await ctx.channel.send(f"{ctx.author.mention} Congratulations! You have solved the problem. You have been awarded {current_question[2]} points and it took you {time.hours} hours {time.minutes} minutes {time.seconds} seconds")
            return
        else:
            await ctx.channel.send(f"{ctx.author.mention} You have not solved the problem yet. Please try again later")
            return
    else:
        id = ctx.author.id
        current_question = await get_current_question(id,'ac')
        if(current_question==None):
            await ctx.channel.send(f"{ctx.author.mention} You have not been given any problem yet. Please use ;gitgud ac to get a problem")
            return
        ac_handle = await get_atcoder_handle(ctx)
        check = await check_if_solved(ctx,ac_handle,current_question,'ac')
        if(check):
            await update_point_at(ctx,current_question[2])
            time = datetime.datetime.now() - current_question[1]
            await ctx.channel.send(f"{ctx.author.mention} Congratulations! You have solved the problem. You have been awarded {current_question[2]} points and it took you {time.hours} hours {time.minutes} minutes {time.seconds} seconds")
            return
        else:
            await ctx.channel.send(f"{ctx.author.mention} You have not solved the problem yet. Please try again later")
            return
        

async def nogud_cf(ctx):

    date_time= datetime.datetime.now()
    try:
        problem = await get_current_question( ctx.author.id,'cf')
        time_date=str(problem[1])
        date_time =datetime.datetime.now() - datetime.datetime(int(time_date[0:4]), int(time_date[5:7]) , int(time_date[8:10]) ,int(time_date[11:13]), int(time_date[14:16]), int(time_date[17:19],0))

    except:
        return "you don't have any problem"

    print(date_time.total_seconds())
    if date_time.total_seconds()>7200:
        await delete_current_question(ctx.author.id,'cf')
        return 'challenge skipped'
    else:
        return 'you have not worked on the problem of cf for 2h'


async def nogud_atcoder(ctx):

    date_time= datetime.datetime.now()
    try:
        print('hello')
        problem = await get_current_question( ctx.author.id,'atcoder')
        time_date=str(problem[1])
        date_time =datetime.datetime.now() - datetime.datetime(int(time_date[0:4]), int(time_date[5:7]) , int(time_date[8:10]) ,int(time_date[11:13]), int(time_date[14:16]), int(time_date[17:19],0))

    except:
        return "you don't have any problem"

 
    if date_time.total_seconds()>3600:
        await delete_current_question(ctx.author.id,'atcoder')
        return 'challenge skipped'
    else:
        return 'you have not worked on the problem of atcoder for 1h'

