# Description: This file is used to connect to the firebase database
# Importing the required libraries
import requests
import firebase_admin
import datetime
from firebase_admin import firestore_async,credentials,firestore
from clist_api import codeforces_handle_to_number, atcoder_handle_to_number

# This is an object which is used to authenticate while connecting to the database
# Please don't change the path of the file or delete it
# Also note that firestore allows only 30 days read and write permissions, also need to change that
cred=credentials.Certificate('./firebase_key.json')

# Initializing the app and the database
app = firebase_admin.initialize_app(cred)
db = firestore_async.client()

# Database structure is as follows:
#    There is a collection named "users" which contains documents of the users
#    Each document is identified by the discord id of the user
#    Each document has the following fields:
#    1. discord_name: string 
#    2. codeforces_handle: string
#    3. atcoder_handle: string
#    4. handle_number_codeforces: string (Used in CLIST API)
#    5. handle_number_atcoder: string (Used in CLIST API)
#    8. solved_codeforces: object list of id's of solved problems on codeforces
#    9. solved_atcoder: object list of id's of solved problems on atcoder
#    10. gitgud_cf: object list of id's of solved problems on codeforces using gitgud
#    11. gitgud_ac: object list of id's of solved problems on atcoder using gitgud
#    12. score_codeforces: integer (Score of the user on codeforces)
#    13. score_atcoder: integer (Score of the user on atcoder)
#    14. problem_solving_cf: tuple (Contains the problem id, time when it was given and points) of the problem given by gitgud on codeforces
#    15. problem_solving_atcoder: tuple (Contains the problem id, time when it was given and points) of the problem given by gitgud on atcoder

# Function to check if a user exists in the database and has identified himself on the given platform
# Input: context (Use to get discord id of the message sender), handle platform (cf or ac)
# Output: boolean (True if user exists, False otherwise)
async def check_user(ctx,handle):
    # Getting the user details from the database
    data = await db.collection('users').document(str(ctx.author.id)).get()
    # Checking if the the user has identified himself on the given platform
    if handle == 'cf':
        if data.exists:
            if 'codeforces_handle' in data.to_dict().keys():
                return True
            else:
                return False
    elif handle == 'ac':
        if data.exists:
            if 'atcoder_handle' in data.to_dict().keys():
                return True
            else:
                return False

# Function to add a user to the database
# Input: context (Use to get discord id of the message sender)
# Output: None
async def add_user(ctx):
    discord_name = ctx.author.name
    # Adding the user to the database with the discord id as the primary key
    if(await db.collection('users').document(str(ctx.author.id)).get()).exists:
        await db.collection('users').document(str(ctx.author.id)).update({ 
            'discord_name': discord_name,   
        })
    else:
        await db.collection('users').document(str(ctx.author.id)).set({
            'discord_name': discord_name,
        })

# Function to add a codeforces handle to the database
# Note that this function should only be called when the user has identified his username so do the error handling their itself
# We also need to add the solved problems id's of the user to the database so that we don't need to find this list again and again since it takes a lot of time
# We can also add the number of problems that were solved when it was last time checked to the database so that we don't need to check the solved problems of the user again and again
# Now whenever their is requirement to find the solved problems of a user, we can just get it from the database and get the new solved problems from the last checked time
# This way we can greatly reduce time of finding the solved problems of a user
# Input: context (Use to get discord id of the message sender), codeforces_handle
# Output: None
async def add_codeforces_handle(ctx, codeforces_handle):
    handle_number_codeforces = codeforces_handle_to_number(codeforces_handle)
    await db.collection('users').document(str(ctx.author.id)).update({
        'codeforces_handle': codeforces_handle,
        'handle_number_codeforces': handle_number_codeforces,
        'gitgud_cf': [],
        'score_codeforces':0,
    })

# Function to add a atcoder handle to the database
# Note that this function should only be called when the user has identified his username so do the error handling their itself
# Again we need to add the solved problems id's of the user to the database so that we don't need to find this list again and again since it takes a lot of time
# Here we store the time when it was last checked to the database this was done because of difference in atcoder and codeforces api
# Input: context (Use to get discord id of the message sender), atcoder_handle
# Output: None
async def add_atcoder_handle(ctx, atcoder_handle):
    handle_number_atcoder = atcoder_handle_to_number(atcoder_handle)
    await db.collection('users').document(str(ctx.author.id)).update({
        'atcoder_handle': atcoder_handle,
        'handle_number_atcoder': handle_number_atcoder,
        'gitgud_ac':[],
        'score_atcoder':0,
    })

#Function to remove a user from the database
# Note that this function should only be called when the user has identified so do the error handling their itself
async def remove_user(ctx):
    await db.collection('users').document(str(ctx.author.id)).delete()

# Function to get the list of all codeforces handles in the database
async def get_all_codeforces_handles():
    users = await db.collection('users').get()
    #Simply iterate over all the users and get the codeforces handles
    codeforces_handles = []
    for user in users:
        discord_id = user.id
        user = user.to_dict()
        if 'codeforces_handle' in user.keys():
            codeforces_handles.append((user['codeforces_handle'],user['handle_number_codeforces'],discord_id))
    return codeforces_handles

# Function to get the list of all atcoder handles in the database
async def get_all_atcoder_handles():
    users = await db.collection('users').get()
    #Simply iterate over all the users and get the atcoder handles
    atcoder_handles = []
    for user in users:
        discord_id = user.id
        user = user.to_dict()
        if 'atcoder_handle' in user.keys():
            atcoder_handles.append((user['atcoder_handle'],user['handle_number_atcoder'],discord_id))
    return atcoder_handles






# Function to find the solved problems of a codeforces handle
# It returns a list of solved problems
# Input: context (Use to get discord id of the message sender), codeforces_handle, last_solved_codeforces (List of all the problem solved last time it was checked), last_checked_codeforces(Time when it was last checked)
async def find_solved_codeforces(ctx,codeforces_handle):
    # This function returns the list of all the submissions of a user
    # This function returns the list of all the submissions of a user
    url = "https://codeforces.com/api/user.status?handle="+str(codeforces_handle)+"&from="+str(1)
    response = requests.get(url).json()
    data=response['result']
#    # Check all the solved problems
    solved_codeforces=[]
    for obj in data:
        if obj['verdict']=='OK':
            solved_codeforces.append(str(obj['problem']['contestId'])+':'+str(obj['problem']['index']))
    
    return solved_codeforces
    
    
# This function is used to find the solved problems of a atcoder handle
# It returns a list of solved problems

async def find_solved_atcoder(ctx,atcoder_handle):
    last_checked_atcoder = last_checked_atcoder - datetime.datetime(1970,1,1,0,0,0,0,datetime.timezone.utc)
    mytime = int(last_checked_atcoder.total_seconds())
    url = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user="+ atcoder_handle+"&from_second="+str(int(mytime))
    response = requests.get(url).json()
    solved_atcoder=[]
    for obj in response:
        if(obj['result']=='AC'):
            solved_atcoder.append(obj['problem_id'])
    return solved_atcoder

# Find the codeforces handle of a user with the given discord id
async def get_codeforces_handle(ctx):
    user_dict=await db.collection('users').document(str(ctx.author.id)).get()
    if user_dict.exists:
        user_dict=user_dict.to_dict()
        if 'codeforces_handle' in user_dict.keys():
            return user_dict['codeforces_handle']
        else:
            return None
    else:
        return None
        
# Find the atcoder handle of a user with the given discord id
async def get_atcoder_handle(ctx):
    user_dict=await db.collection('users').document(str(ctx.author.id)).get()
    if user_dict.exists:
        user_dict=user_dict.to_dict()
        if 'atcoder_handle' in user_dict.keys():
            return user_dict['atcoder_handle']
        else:
            return None
    else:
        return None
        
# This is used to increase the score of a user if he solves a problem using gitgud on codeforces
async def update_point_cf(ctx,points):
    Id=ctx.author.id
    old=await db.collection('users').document(str(Id)).get(field_paths={'score_codeforces'})
    old=old.to_dict()['score_codeforces']
    new=old+points
    await db.collection('users').document(str(Id)).update({
        'score_codeforces':new,
        'problem_solving_cf': None,
    }
    )
    
# This is used to increase the score of a user if he solves a problem using gitgud on atcoder
async def update_point_at(ctx,points):
    Id=ctx.author.id
    old=await db.collection('users').document(str(Id)).get(field_paths={'score_atcoder'})
    old=old.to_dict()['score_atcoder']
    new=old+points
    await db.collection('users').document(str(Id)).update({
        'score_atcoder':new,
        'problem_solving_atcoder': None,
    }
    )
    
# This is used to get the current points of a user on codeforces
async def problem_solving_cf(ctx,problem,points):
    await db.collection('users').document(str(ctx.author.id)).update({
        'problem_solving_cf': (problem,datetime.datetime.now(),points),
    })
    
# This is used to get the current points of a user on atcoder
async def problem_solving_ac(ctx,problem,points):
    await db.collection('users').document(str(ctx.author.id)).update({
        'problem_solving_atcoder': (problem,datetime.datetime.now(),points),
    })
    
# This is used to get the current question the user has taken from gitgud on codeforces
async def get_current_question(id, platform):
    if platform == 'cf':
        problem = await db.collection('users').document(str(id)).get(field_paths={'problem_solving_cf'})
        if problem.to_dict()=={}:
            return None
        problem = problem.to_dict()['problem_solving_cf']
        if problem == None:
            return None
        if len(problem)==0:
            return None
        return problem
    else:
        problem = await db.collection('users').document(str(id)).get(field_paths={'problem_solving_atcoder'})
        if problem.to_dict()=={}:
            return None
        problem = problem.to_dict()['problem_solving_atcoder']
        if problem == None:
            return None
        if len(problem)==0:
            return None
        return problem
        
# This is used to delete the current question the user has taken from gitgud on codeforces in the case of NOGUD
async def delete_current_question(id,platform):
    if platform == 'cf':
        await db.collection('users').document(str(id)).update({
            'problem_solving_cf': firestore.DELETE_FIELD
        }
        )
    else:
        await db.collection('users').document(str(id)).update({
            'problem_solving_atcoder': firestore.DELETE_FIELD
        }
        )
        
# This is used to add the question into the gitgud list of the user on codeforces or atcoder
async def add_in_gitgud_list(id, platform, problem):
    if platform == 'cf':
        gitgud_cf_list= await get_gitgud_list(id,platform)
        gitgud_cf_list.append(problem[0])
        gitgud_cf_list.append(problem[1])
        gitgud_cf_list.append(problem[2])

        await db.collection('users').document(str(id)).update({
            'gitgud_cf': gitgud_cf_list
        }
        )
    else:
        gitgud_ac_list= await get_gitgud_list(id,platform)
        gitgud_ac_list.append(problem[0])
        gitgud_ac_list.append(problem[1])
        gitgud_ac_list.append(problem[2])
        await db.collection('users').document(str(id)).update({
            'gitgud_ac': gitgud_ac_list
        }
        )
        
# This is used to get the gitgud list of the user on codeforces or atcoder
async def get_gitgud_list(id, platform):
    if platform == 'cf':
        problem = await db.collection('users').document(str(id)).get(field_paths={'gitgud_cf'})
        problem = problem.to_dict()['gitgud_cf']
        return problem
    else:
        problem = await db.collection('users').document(str(id)).get(field_paths={'gitgud_ac'})
        problem = problem.to_dict()['gitgud_ac']
        return problem

# This is the function to get the leaderboard of the users

async def Leaderboard_list(ctx , msg):
    res = await ctx.channel.send(f'{ctx.author.mention} Fetching the Leaderboard ... ⌛')
    if msg == 'cf':
        users = db.collection(u'users')
        # Get the users in descending order of their score
        a=users.order_by('score_codeforces', direction=firestore.Query.DESCENDING).stream()
        data = [item async for item in a]
        codeforces_handles = []
        for user in data:
            user=user.to_dict()
            if ('codeforces_handle' in user.keys()):
                score = user['score_codeforces']
                codeforces_handles.append({'Discord Name':user['discord_name'],'Score': score , 'Codeforces Handle': user['codeforces_handle']})
        return codeforces_handles,res

    elif msg == 'ac':
        users = db.collection(u'users')
        a=users.order_by('score_atcoder', direction=firestore.Query.DESCENDING).stream()
        data = [item async for item in a]
        atcoder_handles = []
        for user in data:
            user=user.to_dict()
            if ('atcoder_handle' in user.keys()):
                score = user['score_atcoder']
                atcoder_handles.append({'Discord Name':user['discord_name'],'Score': score , 'Atcoder Handle': user['atcoder_handle'] } )
        return atcoder_handles,res
    elif msg == 'both':
        # In case of both we need to get the users in descending order of their total score (codeforces + atcoder)
        users = await db.collection('users').get()
        handles = []
        # find all the users having both codeforces and atcoder handles and get their score
        for user in users:
            user=user.to_dict()
            if ('codeforces_handle' in user.keys()) and ('atcoder_handle' in user.keys()):
                score = user['score_codeforces'] + user['score_atcoder']
                handles.append({'Discord Name':user['discord_name'],'Total Score': score})
            elif 'codeforces_handle' in user.keys():
                score = user['score_codeforces'] 
                handles.append({'Discord Name':user['discord_name'],'Total Score': score})
            elif 'atcoder_handle' in user.keys():
                score = user['score_atcoder']
                handles.append({'Discord Name':user['discord_name'],'Total Score': score})
        # sort the users in descending order of their total score
        handles = sorted(handles, key=lambda d:d['Total Score'] , reverse=True)
        return handles,res
    else:
        return "error",res

