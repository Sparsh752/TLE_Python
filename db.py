# Description: This file is used to connect to the firebase database
# Importing the required libraries
import firebase_admin
import datetime
import asyncio
from firebase_admin import firestore_async,credentials
from clist_api import codeforces_handle_to_number, atcoder_handle_to_number
from solved import find_solved_codeforces, find_solved_atcoder

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
# NEEDED FUNCTIONS THAT ARE NOT YET IMPLEMENTED:
# 1. codeforces_handle_to_number
# 2. atcoder_handle_to_number
# 3. find_solved_codeforces
# 4. find_solved_atcoder
async def add_user(ctx):
    discord_name = ctx.message.author.name
    await db.collection('users').document(ctx.message.author.id).set({
        'discord_name': discord_name,
    })

async def add_codeforces_handle(ctx, codeforces_handle):
    handle_number_codeforces = await codeforces_handle_to_number(codeforces_handle)
    last_checked_codeforces = datetime.datetime.now()
    solved_codeforces = await find_solved_codeforces(ctx,[],0)
    await db.collection('users').document(ctx.message.author.id).update({
        'codeforces_handle': codeforces_handle,
        'handle_number_codeforces': handle_number_codeforces,
        'last_checked_codeforces': last_checked_codeforces,
        'solved_codeforces': solved_codeforces,
    })

async def add_atcoder_handle(ctx, atcoder_handle):
    handle_number_atcoder = await atcoder_handle_to_number(atcoder_handle)
    last_checked_atcoder = datetime.datetime.now()
    solved_atcoder = await find_solved_atcoder(ctx,[],datetime.datetime.now()-datetime.timedelta(years=50))
    await db.collection('users').document(ctx.message.author.id).update({
        'atcoder_handle': atcoder_handle,
        'handle_number_atcoder': handle_number_atcoder,
        'last_checked_atcoder': last_checked_atcoder,
        'solved_atcoder': solved_atcoder,
    })

#Function to remove a user from the database
# Note that this function should only be called when the user has identified so do the error handling their itself
async def remove_user(ctx):
    await db.collection('users').document(ctx.message.author.id).delete()

# Function to get the list of all codeforces handles in the database
async def get_all_codeforces_handles():
    users = await db.collection('users').get()
    codeforces_handles = []
    for user in users:
        user = user.to_dict()
        if user['codeforces_handle']:
            codeforces_handles.append(user['codeforces_handle'])
    return codeforces_handles

# Function to get the list of all atcoder handles in the database
async def get_all_atcoder_handles():
    users = await db.collection('users').get()
    atcoder_handles = []
    for user in users:
        user = user.to_dict()
        if user['atcoder_handle']:
            atcoder_handles.append(user['atcoder_handle'])
    return atcoder_handles


# solved problems on stage (atconder or codeforces)
async def solved_problems(ctx,stage):
    discord_name = ctx.message.author.name

    doc_ref=await db.collection('users').document(ctx.message.author.id).get()

    docs=doc_ref.to_dict()

    if stage=='atcoder':
        return (docs['last_checked_atcoder'],docs['solved_atcoder'])
    else:
        return (docs['last_checked_codeforces'],docs['solved_codeforces'])

async def update_last_checked_codeforces(ctx, solved_codeforces, last_checked_codeforces):
    await db.collection('users').document(ctx.message.author.id).update({
        'last_checked_codeforces': last_checked_codeforces,
        'solved_codeforces': solved_codeforces,
    })

async def update_last_checked_atcoder(ctx, solved_atcoder, last_checked_atcoder):
    await db.collection('users').document(ctx.message.author.id).update({
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
        'solved_atcoder': solved_atcoder
    })

if __name__ == '__main__':
    asyncio.run(main())"""
