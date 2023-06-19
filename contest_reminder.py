import requests
import asyncio
from datetime import timezone
import datetime
import discord
import paginator
from bs4 import BeautifulSoup
import os
import contest_info

URL_BASE = 'https://clist.by/api/v2/'
counter=0
previous_contestId=""
# This is a function that finds the contest id of the last completed contest
async def completed_contest(html_):
    soup1 = BeautifulSoup(html_,'html.parser')
    # Find all the table rows
    for el in soup1.find_all("tr"):
        # Find the table row with the contest id this is the first row or the last completed contest
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
            previous_contestId=""
            pass
        else:
            await channel.send(f"@everyone The rating changes of the last contest are:")
            await paginator.table(channel,bot,header, returnlist, isChannel=True)
    except Exception as e:
        print(e)
        previous_contestId=""

# This is a function that finds the next contest on codeforces, atcoder and codechef
# This uses Clist API
async def next_contest(id):
    clist_token=os.environ.get('CLIST_TOKEN')
    now = datetime.datetime.now(timezone.utc)
    year = now.year
    month = now.month
    day = now.day 
    hour=now.hour
    minute=now.minute
    seconds=now.second

    url=URL_BASE+'contest/?'+clist_token+'&resource_id='+str(id)+'&limit=1&start__gte='+str(year)+'-'+str(month)+'-'+str(day)+'%20'+str(hour)+':'+str(minute)+':'+str(seconds)+'&order_by=start'

    try:
        resp=requests.get(url)
        contests=resp.json()['objects'][0]
        return [contests['event'],contests['start'],contests['href']]

    except Exception as e:
        print(e)
        return [None,None,None]


def sortDate(date_time):
    return date_time[1][0:4], date_time[1][5:7], date_time[1][8:10], date_time[1][11:13], date_time[1][14:16], date_time[1][17:19] 


# This is a function that runs in the background and check if a contest is coming within 2 hours and if it is then it sends a message in the reminders channel
# This also checks for rating changes and sends a message in the reminders channel if there is a rating change
async def reminder(bot):
    # Get the reminders channel
    channel = discord.utils.get(bot.get_all_channels(), name="reminders") 
    while(1):
        try:
            # Check if there is a rating change
            bool_ = await check_rating_changed()
            if(bool_):
                await print_final_standings(bot,channel)
            else:
                print('NO')
            # Get the next contest on codeforces, atcoder and codechef
            list_=[]
            list_.append(await next_contest(1))
            list_.append(await next_contest(2))
            list_.append(await next_contest(93))
            # Sort the list according to the start time of the contest
            list_.sort(key=sortDate)
            event,start, href = list_[0][0],list_[0][1],list_[0][2]
            
            start=str(start)
            time_date=str(datetime.datetime.now(timezone.utc))
            print((str(start[0:4]), str(start[5:7]), str(start[8:10]), str(start[11:13]), str(start[14:16]), str(start[17:19])))

            dif_time = datetime.datetime(int(start[0:4]), int(start[5:7]), int(start[8:10]), int(start[11:13]), int(start[14:16]), int(start[17:19], 0)) - datetime.datetime(int(time_date[0:4]), int(time_date[5:7]), int(time_date[8:10]), int(time_date[11:13]), int(time_date[14:16]), int(time_date[17:19]))
            if dif_time.total_seconds()<7201:
                # If the contest is coming within 2 hours then send a message in the reminders channel
                embed = discord.Embed(title=event, url=href, description="contest is coming")
                await channel.send('contest is coming within 2h @everyone' +str(event),embed=embed )
                # Sleep for 2 hours so that it doesn't send the message again
                await asyncio.sleep(7201)
            else:
                # Sleep for 1 minute and then check again
                await asyncio.sleep(60)
        except Exception as e:
            continue

# This is a function that can check if the rating changes of the last contest are released or not
async def check_rating_changed():
    url = "https://codeforces.com/contests"
    r = requests.get(url)   
    soup = BeautifulSoup(r.content, 'html.parser')  
    s = soup.find('div', class_= 'contests-table')  
    _html=str(s)
    contest_id= await completed_contest(_html)
    global counter
    global previous_contestId
    if(contest_id==previous_contestId):          # if contest updates already given then end func
        return False
    else:
        try:
            # Find the standings link
            s1= soup.find('a', href= '/contest/'+str(contest_id)+'/standings')
            nlist = s1.text
        except Exception as e:
            print(e)
            return False
        
        if 'Final standings' in nlist:
            url = ('https://codeforces.com/contest/'+str(contest_id)+'/standings')
            r = requests.get(url)  
            soup = BeautifulSoup(r.content, 'html.parser')  
            # Again find the top menu where the rating changes link is shown
            s = soup.find('div', class_= 'second-level-menu')  
            nlist = s.text
            # If the rating changes link is present then return True
            if "Rating Changes" in nlist:
                previous_contestId=contest_id
                return True
            else:
                return False

        else:
            return False

 

        
