import requests
import datetime
import discord
URL_BASE = 'https://clist.by/api/v2/' # the common url used in all clist api calls
clist_token = "username=Sparsh&api_key=c5b41252e84b288521c92f78cc70af99464345f8"

async def nextcontests(ctx):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day  # fetching current time
    msg = await ctx.channel.send(f"{ctx.author.mention} Looking for upcoming contests... 🔍")
    url = URL_BASE+'contest/?'+clist_token+'&start__gte='+str(year)+'-'+str(
        month)+'-'+str(day)+'%2012:00:00&order_by=start'  # url of the list of contests on codeforces
    try:
        resp = requests.get(url)  # fetches response from the url
        contests = resp.json()['objects']  # splitting into json objects
        count = 1
        mylist = [] # list of contests to be returned
        for item in contests:
            mydict = {} # holds information about a contest
            # checking the url length so that it's display is not awkward
            if (len(item['event']) > 15):
                string = item['event']
                mydict['Name'] = f'[{string}]({item["href"]})'
            else:
                mydict['Name'] = item['event']
            mydict['Start Time (dd-mm-yyyy)'] = item['start'][8:10] + \
                item['start'][4:8]+item['start'][:4]+" "+item['start'][11:16]
            mydict['Duration(in min.)'] = str(item['duration']/60)
            mydict['Platform'] = item['resource']
            # 1 -> codeforces
            # 2 -> codechef
            # 25 -> usaco
            # 73 -> hackerearth
            # 93 -> atcoder
            if(item['resource_id'] in [1,93,2,73,25]):
                count = count+1
                mylist.append(mydict)
            if(count == 11):
                break
        content = ''
        # deletes the previous "looking for upcoming contests" message
        await msg.delete()
        for contest in mylist:
            timings=datetime.datetime.strptime(contest['Start Time (dd-mm-yyyy)'],"%d-%m-%Y %H:%M")+datetime.timedelta(minutes=330)
            content += "_"+contest['Name']+"_"+'\n'+'Start Time (dd-mm-yyyy):\a'+str(timings.day//10)+str(timings.day%10)+"-"+str(timings.month//10)+str(timings.month%10)+"-"+str(timings.year)+" "+str(timings.hour//10)+str(timings.hour%10)+":"+str(timings.minute//10)+str(timings.minute%10) + \
                '\n' + 'Platform:\a'+contest['Platform']+\
                '\n'+'Duration(in min.):\a' + \
                contest['Duration(in min.)']+'\n\n\n'
        await ctx.channel.send(embed=discord.Embed(
            title="Contests",
            description=content,
            color=discord.Color.blue()))  # returns string to be messaged by bot
    except Exception as e:  # in case of any error, code doesn't crash but tells about it in the terminal
        await ctx.channel.send("Sorry couldn't fetch the data. Please try again later.")


# function to convert codeforces handle to codeforces id to facilitate clist api call
def codeforces_handle_to_number(handle_name):
    url = URL_BASE+'account/?'+clist_token+'&resource_id=1' + \
        '&handle='+handle_name  # url of the to be fetched
    if (handle_name == None):  # if handle is none, return none
        return None
    try:
        resp = requests.get(url)  # fetching response
        return resp.json()['objects'][0]['id']  # returning id
    except Exception as e:  # tackiling errors
        return None


# function to convert atcoder handle to atcoder id similar to codeforces
def atcoder_handle_to_number(handle_name):
    url = URL_BASE+'account/?'+clist_token+'&resource_id=93'+'&handle='+handle_name
    if (handle_name == None):
        return None
    try:
        resp = requests.get(url)
        return resp.json()['objects'][0]['id']
    except Exception as e:
        return None


# function to convert codechef handle to codechef id similar to codeforces
def codechef_handle_to_number(handle_name):
    url = URL_BASE+'account/?'+clist_token+'&resource_id=2'+'&handle='+handle_name
    if (handle_name == None):
        return None
    try:
        resp = requests.get(url)
        return resp.json()['objects'][0]['id']
    except Exception as e:
        return None
