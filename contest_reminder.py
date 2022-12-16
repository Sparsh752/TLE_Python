import requests
import asyncio
from datetime import timezone
import datetime
import discord
import paginator
from bs4 import BeautifulSoup
import contest_info
counter=0
previous_contestId=""
### checks just completed contest
channel_id = 1052888188479348787
async def completed_contest(html_):
    soup1 = BeautifulSoup(html_,'html.parser')
    for el in soup1.find_all("tr"):
        if el.has_attr("data-contestid"):
            contest_ID=el.attrs["data-contestid"]
            break
    return contest_ID


async def print_final_standings(bot,channel): 
    global previous_contestId
    try:
        returnlist,header= await contest_info.codeforces_rating_changes_shower(str(previous_contestId),bot,channel)
        print(returnlist)
        if header=="error":
            previous_contestId=""
        elif len(returnlist)==0:
            pass
        else:
            await channel.send(f"@everyone The rating changes of the last contest are:")
            await paginator.table(channel,bot,header, returnlist, isChannel=True)
    except Exception as e:
        print(e)
        previous_contestId=""

URL_BASE = 'https://clist.by/api/v2/'
clist_token="username=Sparsh&api_key=c5b41252e84b288521c92f78cc70af99464345f8"


async def next_contest():
    now = datetime.datetime.now(timezone.utc)
    year = now.year
    month = now.month
    day = now.day 
    hour=now.hour
    minute=now.minute
    seconds=now.second

    url=URL_BASE+'contest/?'+clist_token+'&resource_id=1&limit=1&start__gte='+str(year)+'-'+str(month)+'-'+str(day)+'%20'+str(hour)+':'+str(minute)+':'+str(seconds)+'&order_by=start'

    try:
        resp=requests.get(url)
        contests=resp.json()['objects'][0]
        print((contests['event'],contests['start'],contests['href']))
        return contests['event'],contests['start'],contests['href']

    except Exception as e:
        print(e)
        return None,None,None




async def reminder(bot):
    channel = bot.get_channel(channel_id)
    while(1):
        try:
            bool_ = await check_rating_changed()
            if(bool_):
                await print_final_standings(bot,channel)
            else:
                print('NO')
            event,start, href = await next_contest()
            start=str(start)
            time_date=str(datetime.datetime.now(timezone.utc))
            print((str(start[0:4]), str(start[5:7]), str(start[8:10]), str(start[11:13]), str(start[14:16]), str(start[17:19])))
            # print()
            dif_time = datetime.datetime(int(start[0:4]), int(start[5:7]), int(start[8:10]), int(start[11:13]), int(start[14:16]), int(start[17:19], 0)) - datetime.datetime(int(time_date[0:4]), int(time_date[5:7]), int(time_date[8:10]), int(time_date[11:13]), int(time_date[14:16]), int(time_date[17:19]))
            if dif_time.total_seconds()<7201:
                
                embed = discord.Embed(title=event, url=href, description="contest is coming")
                await channel.send('contest is coming within 2h @everyone' +str(event),embed=embed )
                await asyncio.sleep(7201)
            else:
                await asyncio.sleep(60)
        except Exception as e:
            continue

async def check_rating_changed():
    url = "https://codeforces.com/contests"
    r = requests.get(url)   
    soup = BeautifulSoup(r.content, 'html.parser')  
    s = soup.find('div', class_= 'contests-table')  
    _html=str(s)
    contest_id= await completed_contest(_html)
    global counter
    global previous_contestId
    # if(counter==0):
    #     previous_contestId=contest_id
    #     counter=1
    if(contest_id==previous_contestId):          # if contest updates already given then end func
        print(contest_id)
        return False
    else:
        s1= soup.find('a', href= '/contest/'+str(contest_id)+'/standings')
        nlist = s1.text
        if 'Final standings' in nlist:
            url = ('https://codeforces.com/contest/'+str(contest_id)+'/standings')
            r = requests.get(url)  
            soup = BeautifulSoup(r.content, 'html.parser')  
            
            s = soup.find('div', class_= 'second-level-menu')  
            nlist = s.text
            if "Rating Changes" in nlist:
                print("yes rating changes came")

                previous_contestId=contest_id
                print(previous_contestId)

                #### Update previous contest Id in Firebase with ((( contest_id )))  #######



                return True
            else:
                return False

        else:
            return False

 

        
