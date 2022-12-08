import json
import requests
import random
import string
import asyncio
from db import add_user, add_codeforces_handle, add_atcoder_handle
#Check whether handle exists or not
def check_cf(username, message):
    url = "https://codeforces.com/profile/" + username
    url_home = "https://codeforces.com/"
    response = requests.get(url)
    if response.url == url_home:
        # print('Web site does not exist')
        return False
    else:
        # print('Web site exists')
        return True



#Fetching firstName from codeforces
def firstname(cf_handle):
    cf_api = "https://codeforces.com/api/user.info?handles=" + cf_handle
    response = requests.get(cf_api)
    cf_list = response.json()['result'][0]
    if "firstName" in cf_list.keys():
        firstname_ = cf_list['firstName']
        return firstname_
    else:
        # print("first name does not exist")
        return ""


async def handle_verification(ctx):
    message = ctx
    username = str(message.author.name)
    user_message = str(message.content)
    await add_user(ctx)
    msg_data = user_message.split()
    if (len(msg_data) != 2):
        await message.channel.send(f"{message.author.mention} Command format is incorrect")
        return
        
    if msg_data[0] == ';identify_cf':
        cf_handle = msg_data[1]
        if check_cf(msg_data[1], message):
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            output = "set your firstname as `" + random_string + "` in your codeforces account within 60 seconds..."
            await message.channel.send(f"{message.author.mention} {output}")

            for i in range(30):
                await asyncio.sleep(2)
                first_name = firstname(cf_handle)
                if first_name == random_string:
                    await add_codeforces_handle(ctx, cf_handle)
                    #########################
                    # store in database if successfull then print

                    await message.channel.send(f"{message.author.mention} you are successfully identified... >_<")
                    break
            else:
                await message.channel.send(f"{message.author.mention} TimeOut, try again...")

        else:
            await message.channel.send(f"{message.author.mention} given handle is invalid")


    ###yet to build.....................
    elif msg_data[0] == ';identify_ac':
        await message.channel.send("Yet to be built!")
    elif msg_data[0] == ';identify_cc':
        await message.channel.send("Yet to be built!")
    else: 
        await message.channel.send(f"{message.author.mention} write identify correctly")