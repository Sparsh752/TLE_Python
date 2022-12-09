import json
import requests
import random
import string
import asyncio
from bs4 import BeautifulSoup

##Codeforces
#Check whether handle exists or not
def check_cf(username):
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

##CodeChef
#Check whether handle exists or not
def check_cc(cc_handle):
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
def check_Name(cc_handle, random_string):
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
def check_ac(ac_handle):
    url = "https://atcoder.jp/users/" + ac_handle
    r = requests.get(url);
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

async def handle_verification(message):

    username = str(message.author.name)
    user_message = str(message.content)

    msg_data = user_message.split()
    if (len(msg_data) != 2):
        await message.channel.send(f"{message.author.mention} Command format is incorrect")
        return
        
    if msg_data[0] == ';identify_cf':
        cf_handle = msg_data[1]
        if check_cf(msg_data[1]):
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            output = "set your firstname as `" + random_string + "` in your codeforces account within 60 seconds..."
            await message.channel.send(f"{message.author.mention} {output}")

            for i in range(30):
                await asyncio.sleep(2)
                first_name = firstname(cf_handle)
                if first_name == random_string:


                    #########################
                    # store in database if successfull then print

                    await message.channel.send(f"{message.author.mention} you are successfully identified on codeforces... >_<")
                    break
            else:
                await message.channel.send(f"{message.author.mention} TimeOut, try again...")

        else:
            await message.channel.send(f"{message.author.mention} given handle is invalid")


    elif msg_data[0] == ';identify_ac':
        ac_handle = msg_data[1]
        if check_ac(msg_data[1]):
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            output = "set your Affiliation as `" + random_string + "` in your Atcoder account within 60 seconds..."
            await message.channel.send(f"{message.author.mention} {output}")
            for i in range(30):
                await asyncio.sleep(2)
                if check_Affiliation(ac_handle, random_string):
                    #########################
                    # store in database if successfull then print
                    await message.channel.send(f"{message.author.mention} you are successfully identifiedon on atcoder... >_<")
                    break
            else:
                await message.channel.send(f"{message.author.mention} TimeOut, try again...")
        else:
            await message.channel.send(f"{message.author.mention} given handle is invalid")

    elif msg_data[0] == ';identify_cc':
        cc_handle = msg_data[1]
        if check_cc(msg_data[1]):
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
            output = "set your Name as `" + random_string + "` in your codechef account within 60 seconds..."
            await message.channel.send(f"{message.author.mention} {output}")
            for i in range(30):
                await asyncio.sleep(2)
                if check_Name(cc_handle, random_string):
                    #########################
                    # store in database if successfull then print
                    await message.channel.send(f"{message.author.mention} you are successfully identified on codechef... >_<")
                    break
            else:
                await message.channel.send(f"{message.author.mention} TimeOut, try again...")
        else:
            await message.channel.send(f"{message.author.mention} given handle is invalid")
    else: 
        await message.channel.send(f"{message.author.mention} Write identify correctly")
