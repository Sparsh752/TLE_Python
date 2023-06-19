import requests
from operator import itemgetter
from datetime import datetime,timezone

#Get the problems submitted by a user using his codeforces handle and also be able to see them sorted by Rating
async def stalk_user(ctx,codeforces_handle,hardest=False,R=0):
    msg = await ctx.channel.send(f"{ctx.author.mention} Getting data for `{codeforces_handle}` from codeforces")

    #Get the problems solved by a user using codeforces API
    url = "https://codeforces.com/api/user.status?handle="+str(codeforces_handle)+"&from="+str(1)
    response = requests.get(url,timeout=5)
    response=response.json()

    #If user does not exist send error message
    if response['status']=='FAILED':
        await msg.edit(content=f"{ctx.author.mention} No user found :scream_cat:")
        return None
    
    total=len(response['result'])
    url = "https://codeforces.com/api/user.status?handle="+str(codeforces_handle)+"&count="+str(total)
    response = requests.get(url).json()
    data=response['result']
    n_dict=[]
    for obj in data:
        if obj['verdict']=='OK':
            rounded_dt1 = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) #Current UTC datetime rounded to beginning of day 
            rounded_dt2 = datetime.fromtimestamp(obj['creationTimeSeconds'],timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) #Rounding up the date stored in obj to beginning of day
            time_delta=(rounded_dt1-rounded_dt2).days #Finding the difference in days between the two

            #Converting numeric difference in days to string
            if time_delta==0:
                days="Today"
            elif time_delta==1:
                days="Yesterday"
            else:
                days=str(time_delta)+" Days Ago"
            
            #If problem not yet rated, set rating to zero so sorting later is easier
            if 'rating' not in obj['problem']:
                obj['problem']['rating']=0
            
            #Appending Problem as a dictionnary for paginator function
            n_dict.append({'Problem':str(obj['problem']['name']),'Rating':int(obj['problem']['rating']),'Time': days})

    #If hardest is asked in command to bot, sort the problems by difficulty rating with highest rating in first
    if hardest==True:
        n_dict = sorted(n_dict, key=itemgetter('Rating'),reverse=True)

    #If R parameter is provided then only display ratings above rating 'R'
    if R!=0:
        temp=[]
        for i in n_dict:
            if i['Rating']>=R:
                temp.append(i)
        n_dict=temp 
    else:
        for i in n_dict:
            if i['Rating']==0:
                i['Rating']='---' #Convert Rating 0 to '---' to indicate to user that problem is not rated yet

    #Provide the header row for paginator
    head_row=['Problem','Rating','Time'] 
    return head_row,n_dict,msg
