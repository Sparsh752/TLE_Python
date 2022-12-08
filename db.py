# Description: This file is used to connect to the firebase database
# Importing the required libraries
import firebase_admin
import datetime
import asyncio
from firebase_admin import firestore_async,credentials
from clist_api import codeforces_handle_to_number, atcoder_handle_to_number, codechef_handle_to_number

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
# 3. Note that the discord name of the user will be the primary key
# 4. Database structure is as follows:
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
async def add_user(ctx, codeforces_handle, atcoder_handle):
    discord_name = ctx.message.author.name
    handle_number_codeforces = codeforces_handle_to_number(codeforces_handle)
    handle_number_atcoder = atcoder_handle_to_number(atcoder_handle)
    solved_codeforces = find_solved_codeforces(codeforces_handle, None) # The second aregument is last_checked
    solved_atcoder = find_solved_atcoder(atcoder_handle, None)
    # Since we are creating a new user, we don't have any last_checked so it is set to None
    await db.collection('users').document(ctx.message.author.id).set({
        'discord_name': discord_name,
        'codeforces_handle': codeforces_handle,
        'atcoder_handle': atcoder_handle,
        'handle_number_codeforces': handle_number_codeforces,
        'handle_number_atcoder': handle_number_atcoder,
        'last_check': datetime.datetime.now(),
        'solved_codeforces': solved_codeforces,
        'solved_atcoder': solved_atcoder
    })

#This is for testing purposes
"""async def main():
    discord_name = 'discord_name'
    codeforces_handle = 'codeforces_handle'
    atcoder_handle = 'atcoder_handle'
    handle_number_codeforces = 'handle_number_codeforces'
    handle_number_atcoder = 'handle_number_atcoder'
    last_check = datetime.datetime.now()
    solved_codeforces = ['solved_codeforces', 'solved_codeforces1']
    solved_atcoder = ['solved_atcoder', 'solved_atcoder1']
    await db.collection('users').document(discord_name).set({
        'discord_name': discord_name,
        'codeforces_handle': codeforces_handle,
        'atcoder_handle': atcoder_handle,
        'handle_number_codeforces': handle_number_codeforces,
        'handle_number_atcoder': handle_number_atcoder,
        'last_check': last_check,
        'solved_codeforces': solved_codeforces,
        'solved_atcoder': solved_atcoder
    })

if __name__ == '__main__':
    asyncio.run(main())"""
