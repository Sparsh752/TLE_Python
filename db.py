# Description: This file is used to connect to the firebase database
# Importing the required libraries
import requests
import firebase_admin
import datetime
import asyncio
from firebase_admin import firestore_async,credentials,firestore
from clist_api import codeforces_handle_to_number, atcoder_handle_to_number
import time
# from solved import find_solved_codeforces, find_solved_atcoder

# This is an object which is used to authenticate while connecting to the database
# Please don't change the path of the file or delete it
# Also note that firestore allows only 30 days read and write permissions, also need to change that
cred=credentials.Certificate('./firebase_key.json')

# Initializing the app and the database
app = firebase_admin.initialize_app(cred)
db = firestore_async.client()

# TODO, README 
# 1. Add a function to add a new user to the database
# 2. Add a function to get the user details from the database
# 3. Add a function to get the solved problems of a user from the database
# 4. Note that the discord name of the user will be the primary key
# 5. Database structure is as follows:
#    There is a collection named "users" which contains documents of the users
#    Each document has the following fields:
#    1. discord_name: string PRIMARY KEY
#    2. codeforces_handle: string
#    3. atcoder_handle: string
#    4. handle_number_codeforces: string
#    5. handle_number_atcoder: string
#    6. last_check : datetime
#    7. solved_codeforces: object list of id's of solved problems on codeforces
#    8. solved_atcoder: object list of id's of solved problems on atcoder

# Function to add a new user to the database
# Input: discord_name, codeforces_handle, atcoder_handle
# Output: None
async def add_user(ctx):
    discord_name = ctx.author.name
    if(await db.collection('users').document(str(ctx.author.id)).get()).exists:
        await db.collection('users').document(str(ctx.author.id)).update({ #TODO
            'discord_name': discord_name,   
        })
    else:
        await db.collection('users').document(str(ctx.author.id)).set({
            'discord_name': discord_name,
        })

async def add_codeforces_handle(ctx, codeforces_handle):
    handle_number_codeforces = codeforces_handle_to_number(codeforces_handle)
    solved_codeforces = await find_solved_codeforces(ctx,codeforces_handle,[],0)
    await db.collection('users').document(str(ctx.author.id)).update({
        'codeforces_handle': codeforces_handle,
        'handle_number_codeforces': handle_number_codeforces,
        'solved_codeforces': solved_codeforces,
        'score_codeforces':0,
    })

async def add_atcoder_handle(ctx, atcoder_handle):
    handle_number_atcoder = atcoder_handle_to_number(atcoder_handle)
    solved_atcoder = await find_solved_atcoder(ctx,atcoder_handle,[],datetime.datetime.now(datetime.timezone.utc))
    await db.collection('users').document(str(ctx.author.id)).update({
        'atcoder_handle': atcoder_handle,
        'handle_number_atcoder': handle_number_atcoder,
        'solved_atcoder': solved_atcoder,
        'score_atcoder':0,
    })

#Function to remove a user from the database
# Note that this function should only be called when the user has identified so do the error handling their itself
async def remove_user(ctx):
    await db.collection('users').document(str(ctx.author.id)).delete()

# Function to get the list of all codeforces handles in the database
async def get_all_codeforces_handles():
    users = await db.collection('users').get()
    codeforces_handles = []
    for user in users:
        user = user.to_dict()
        if 'codeforces_handle' in user.keys():
            codeforces_handles.append((user['codeforces_handle'],user['handle_number_codeforces']))
    return codeforces_handles

# Function to get the list of all atcoder handles in the database
async def get_all_atcoder_handles():
    users = await db.collection('users').get()
    atcoder_handles = []
    for user in users:
        user = user.to_dict()
        if 'atcoder_handle' in user.keys():
            atcoder_handles.append((user['atcoder_handle'],user['handle_number_atcoder']))
    return atcoder_handles


# solved problems on stage (atconder or codeforces)
async def get_last_solved_problems(ctx,stage):
    
    doc_ref=await db.collection('users').document(str(ctx.author.id)).get()

    docs=doc_ref.to_dict()

    if stage=='atcoder':
        return (docs['last_checked_atcoder'],docs['solved_atcoder'])
    else:
        return (docs['last_checked_codeforces'],docs['solved_codeforces'])

async def update_last_checked_codeforces(ctx, solved_codeforces, last_checked_codeforces):
    await db.collection('users').document(str(ctx.author.id)).update({
        'last_checked_codeforces': last_checked_codeforces,
        'solved_codeforces': solved_codeforces,
    })

async def update_last_checked_atcoder(ctx, solved_atcoder, last_checked_atcoder):
    await db.collection('users').document(str(ctx.author.id)).update({
        'last_checked_atcoder': last_checked_atcoder,
        'solved_atcoder': solved_atcoder,
    })

#This is for testing purposes
"""async def main():
    discord_name = 'discord_name'
    codeforces_handle = 'codeforces_handle'
    atcoder_handle = 'atcoder_handle'
    handle_number_codeforces = 'handle_number_codeforces'
    handle_number_atcoder = 'handle_number_atcoder'
    last_checked_codeforces = datetime.datetime.now()
    last_checked_atcoder = datetime.datetime.now()
    solved_codeforces = ['solved_codeforces', 'solved_codeforces1']
    solved_atcoder = ['solved_atcoder', 'solved_atcoder1']
    await db.collection('users').document(discord_name).set({
        'discord_name': discord_name,
        'codeforces_handle': codeforces_handle,
        'atcoder_handle': atcoder_handle,
        'handle_number_codeforces': handle_number_codeforces,
        'handle_number_atcoder': handle_number_atcoder,
        'last_checked_codeforces': last_checked_codeforces,
        'last_checked_atcoder': last_checked_atcoder,
        'solved_codeforces': solved_codeforces,
        'solved_atcoder': solved_atcoder,
        'score_atcoder':0,
        'score_codeforces':0,
    })

if __name__ == '__main__':
    asyncio.run(main())"""

async def find_solved_codeforces(ctx,codeforces_handle, last_solved_codeforces, last_checked_codeforces):
    url = "https://codeforces.com/api/user.status?handle="+str(codeforces_handle)+"&from="+str(1)
    response = requests.get(url).json()
    total=len(response['result'])
    if total == last_checked_codeforces:
        return last_solved_codeforces
    url = "https://codeforces.com/api/user.status?handle="+str(codeforces_handle)+"&count="+str(total-last_checked_codeforces)
    response = requests.get(url).json()
    data=response['result']
    for obj in data:
        if obj['verdict']=='OK':
            last_solved_codeforces.append(str(obj['problem']['contestId'])+':'+str(obj['problem']['index']))
    last_checked_codeforces += len(data)
    await update_last_checked_codeforces(ctx, last_solved_codeforces, last_checked_codeforces)
    return last_solved_codeforces
    
# This function is used to find the solved problems of a atcoder handle
# It returns a list of solved problems
# It also updates the last_checked_atcoder and last_solved_atcoder field in the database

async def find_solved_atcoder(ctx,atcoder_handle, last_solved_atcoder, last_checked_atcoder):
    last_checked_atcoder = last_checked_atcoder - datetime.datetime(2010, 1 ,1 ,0,0,0,0, datetime.timezone.utc)
    mytime = int(last_checked_atcoder.total_seconds())
    url = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user="+ atcoder_handle+"&from_second="+str(int(mytime))
    response = requests.get(url).json()
    for obj in response:
        if(obj['result']=='AC'):
            last_solved_atcoder.append(obj['problem_id'])
    last_checked_atcoder = datetime.datetime.now(datetime.timezone.utc)
    await update_last_checked_atcoder(ctx, last_solved_atcoder, last_checked_atcoder)
    return last_solved_atcoder

async def get_codeforces_handle(ctx):
    user_dict=await db.collection('users').document(str(ctx.author.id)).get()
    user_dict=user_dict.to_dict()
    if 'codeforces_handle' in user_dict.keys():
        return user_dict['codeforces_handle']
    else:
        return None

async def get_atcoder_handle(ctx):
    user_dict=await db.collection('users').document(str(ctx.author.id)).get()
    user_dict=user_dict.to_dict()
    if 'atcoder_handle' in user_dict.keys():
        return user_dict['atcoder_handle']
    else:
        return None

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
async def problem_solving_cf(ctx,problem,points):
    await db.collection('users').document(str(ctx.author.id)).update({
        'problem_solving_cf': (problem,datetime.datetime.now(),points),
    })
async def problem_solving_ac(ctx,problem,points):
    await db.collection('users').document(str(ctx.author.id)).update({
        'problem_solving_atcoder': (problem,datetime.datetime.now(),points),
    })
    
async def get_current_question(id, platform):
    if platform == 'cf':
        problem = await db.collection('users').document(str(id)).get(field_paths={'problem_solving_cf'})
        problem = problem.to_dict()['problem_solving_cf']
        return problem
    else:
        problem = await db.collection('users').document(str(id)).get(field_paths={'problem_solving_atcoder'})
        problem = problem.to_dict()['problem_solving_atcoder']
        return problem

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