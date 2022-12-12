import db
import requests
import json 

URL_BASE = 'https://clist.by/api/v2/'
clist_token="username=Sparsh&api_key=c5b41252e84b288521c92f78cc70af99464345f8"

async def codeforces_contest_id_finder(event_name):                    #function to convert cf contest name to contest id
    url=URL_BASE+'contest/?'+clist_token+'&resource_id=1'+'&order_by=-start'+'&limit=100'  #url to be fetched
    if(event_name==None):                                                    #if event is none, return none
        return None 
    try:            
        resp= requests.get(url)                                              #fetching response
        details=json.dumps(resp.json(),ensure_ascii=False)                    #converting to json
        data=json.loads(details)['objects']
        for contest in data:                         #iterating over all fetched contests to find the contest id
            if contest['href']=='https://codeforces.com/contests/'+event_name:     
                return contest['id']
    except Exception as e:                                                  #tackiling errors    
        print(e)

async def codeforces_rating_changes(event_name):            # function to get the rating changes of all users in codeforces
    codeforces_handle = await db.get_all_codeforces_handles()       # get all the codeforces handles from the database
    contest_id=await codeforces_contest_id_finder(event_name)                  # get the contest id of the contest 
    try: 
        returnlist=[]
        for handle in codeforces_handle:                                # iterate over all the handles
            url = URL_BASE+'statistics/?'+clist_token+'&contest_id='+str(contest_id)+'&account_id='+str(handle[1])+'&with_problems=True&with_more_fields=True'           # url to be fetched
            response = requests.get(url).json()                        # fetching response
            if response['objects']:                                # if the response is not empty
                if 'CONTESTANT' in response['objects'][0]['more_fields']['participant_type']: # if the user is a contestant
                    data=response['objects'][0]                     # get the data of the user
                    data_dict={'handle':handle[0],'position':data['place'],'score':data['score'],'rating_change':data['rating_change'],'old_rating':data['old_rating'],'new_rating':data['new_rating']} # create a dictionary of the data
                    for i in data['problems']:  # adding the solved problems to the dictionary
                        if 'upsolving' in data['problems'][i].keys():
                            continue
                        if data['problems'][i]['result']=='+':
                            data_dict[i]=data['problems'][i]['result']
                            continue
                        if int(data['problems'][i]['result'])<=0:
                            continue
                        data_dict[i]=data['problems'][i]['result']
                    returnlist.append(data_dict) # append the dictionary to the return list
        return returnlist  # returning the list
        
    except Exception as e:
        print(e)
