import requests
import asyncio
from datetime import timezone
import datetime
import discord


URL_BASE = 'https://clist.by/api/v2/'
clist_token="username=Sparsh&api_key=c5b41252e84b288521c92f78cc70af99464345f8"
channel_id = 1048212913539784808

async def next_contest():
    now = datetime.datetime.now(timezone.utc)
    year = now.year
    month = now.month
    day = now.day 
    hour=now.hour
    minute=now.minute
    seconds=now.second

    url=URL_BASE+'contest/?'+clist_token+'&resource_id=1&limit=1&start__gte='+str(year)+'-'+str(month)+'-'+str(day)+'%20'+str(hour)+':'+str(minute)+':00&order_by=start'

    try:
        resp=requests.get(url)
        contests=resp.json()['objects'][0]
        print((contests['event'],contests['start'],contests['href']))
        return contests['event'],contests['start'],contests['href']

    except Exception as e:
        print(e)




async def contest_remi(bot):

    while(1):

        event,start, href = await next_contest()
        start=str(start)
        time_date=str(datetime.datetime.now(timezone.utc))
        print((str(start[0:4]), str(start[5:7]), str(start[8:10]), str(start[11:13]), str(start[14:16]), str(start[17:19])))
        # print()
        dif_time = datetime.datetime(int(start[0:4]), int(start[5:7]), int(start[8:10]), int(start[11:13]), int(start[14:16]), int(start[17:19], 0)) - datetime.datetime(int(time_date[0:4]), int(time_date[5:7]), int(time_date[8:10]), int(time_date[11:13]), int(time_date[14:16]), int(time_date[17:19]))

        if dif_time.total_seconds()<7201:
            channel = bot.get_channel(channel_id)
            embed = discord.Embed(title=event, url=href, description="comtest is comming")
            await channel.send('contest is comming within 2h @everyone' +str(event),embed=embed )
            await asyncio.sleep(7201)
        else:
            await asyncio.sleep(min(dif_time.total_seconds()-7200,216000))

            

        
