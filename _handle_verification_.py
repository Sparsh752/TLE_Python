import json
import requests
import random
import string
import asyncio
from bs4 import BeautifulSoup
from db import add_user, add_codeforces_handle, add_atcoder_handle,check_user
from gitgud import get_cf_user_rating
import discord
from rating_roles import rating_role

##Codeforces
#Check whether handle exists or not
async def check_cf(username):
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
async def firstname(cf_handle):
    cf_api = "https://codeforces.com/api/user.info?handles=" + cf_handle
    response = requests.get(cf_api)
    cf_list = response.json()['result'][0]
    if "firstName" in cf_list.keys():
        firstname_ = cf_list['firstName']
        return firstname_
    else:
        # print("first name does not exist")
        return ""

##CodeChef
#Check whether handle exists or not
async def check_cc(cc_handle):
    url = "https://www.codechef.com/users/" + cc_handle
    url_home = "https://www.codechef.com/"
    response = requests.get(url)
    if response.url == url_home:
        # print('Web site does not exist')
        return False
    else:
        # print('Web site exists')
        return True

#Check Name from codechef
async def check_Name(cc_handle, random_string):
    url = "https://www.codechef.com//users/" + cc_handle
    r = requests.get(url)   
    soup = BeautifulSoup(r.content, 'html.parser')  
    s = soup.find('div', class_= 'breadcrumb')  
    nlist = s.text

    if random_string in nlist:
        return True
    else:
        return False

##AtCoder
#Check whether handle exists or not
async def check_ac(ac_handle):
    url = "https://atcoder.jp/users/" + ac_handle
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        return False

#Check Affiliation from Atcoder
def check_Affiliation(ac_handle, random_string):
    url = "https://atcoder.jp/users/" + ac_handle
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', class_= 'col-md-3 col-sm-12')
    table = s.find('table', class_='dl-table')
    
    nlist = table.text

    if random_string in nlist:
        return True
    else:
        return False

async def handle_verification(ctx,bot):
    channel = discord.utils.get(bot.get_all_channels(), name="reminder")                              
    message=ctx
    username = str(message.author.name)
    user_message = str(message.content)
    await add_user(ctx)
    msg_data = user_message.split()
    msg = await ctx.channel.send(f"{ctx.author.mention} Checking the correctness of command")
    if (len(msg_data) != 2):
        await message.channel.send(f"{message.author.mention} Command format is incorrect, please check the help section... ")
        return
        
    if msg_data[0] == ';identify_cf':
        check=await check_user(ctx,'cf')
        if(check):
            await msg.edit(content = f"{message.author.mention} you are already identified on codeforces... :sweat_smile: ")
            return
        cf_handle = msg_data[1]
        check1=await check_cf(msg_data[1])
        if check1:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            output = "Set your firstname as `" + random_string + "` in your codeforces account within 60 seconds... Click [here](https://codeforces.com/settings/social) to set your firstname..."
            await msg.delete()
            await ctx.channel.send(embed=discord.Embed(description=f"{message.author.mention} {output}", color=discord.Color.blue()))
            for i in range(30):
                await asyncio.sleep(2)
                first_name = await firstname(cf_handle)
                if first_name == random_string:
                    await add_codeforces_handle(ctx, cf_handle)
                    rating=await get_cf_user_rating(cf_handle)
                    #########################
                    # store in database if successfull then print

                    await message.channel.send(f"{message.author.mention} you are successfully identified on codeforces... :smiley:")
                    await rating_role(ctx.author.id,int(rating),bot,channel)
                    break
            else:
                await msg.edit(content=f"{message.author.mention} TimeOut, try again...")

        else:
            await msg.edit(content=f"{message.author.mention} given handle is invalid")


    elif msg_data[0] == ';identify_ac':
        check=await check_user(ctx,'ac')
        if(check):
            await msg.edit(content=f"{message.author.mention} you are already identified on atcoder... :sweat_smile: ")
            return
        ac_handle = msg_data[1]
        check1 = await check_ac(msg_data[1])
        if check1:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            output = "Set your Affiliation as `" + random_string + "` in your Atcoder account within 60 seconds...\n Click [here](https://atcoder.jp/settings) to set you affilation"
            await msg.delete()
            await ctx.channel.send(embed=discord.Embed(description=f"{message.author.mention} {output}", color=0x00ff00))
            for i in range(30):
                await asyncio.sleep(2)
                if check_Affiliation(ac_handle, random_string):
                    #########################
                    # store in database if successfull then print
                    await add_atcoder_handle(ctx, ac_handle)
                    await message.channel.send(f"{message.author.mention} you are successfully identified on on atcoder... :smiley:")
                    break
            else:
                await msg.edit(content=f"{message.author.mention} TimeOut, try again...")
        else:
            await msg.edit(content=f"{message.author.mention} given handle is invalid")

    elif msg_data[0] == ';identify_cc':
        cc_handle = msg_data[1]
        check1=await check_cc(msg_data[1])
        if check1:
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            output = "set your Name as `" + random_string + "` in your codechef account within 60 seconds..."
            await msg.edit(content=f"{message.author.mention} {output}")
            for i in range(30):
                await asyncio.sleep(2)
                check2 = await check_Name(cc_handle, random_string)
                if check2:
                    #########################
                    # store in database if successfull then print
                    await message.channel.send(f"{message.author.mention} you are successfully identified on codechef... >_<")
                    break
            else:
                await msg.edit(content=f"{message.author.mention} TimeOut, try again...")
        else:
            await msg.edit(content=f"{message.author.mention} given handle is invalid")
    else: 
        await msg.edit(content=f"{message.author.mention} Write identify correctly")
