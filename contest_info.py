import db
import requests

URL_BASE = 'https://clist.by/api/v2/'
clist_token="username=Sparsh&api_key=c5b41252e84b288521c92f78cc70af99464345f8"

async def codeforces_rating_changes():                     # function to get the rating changes of all users in codeforces
    codeforces_handle = await db.get_all_codeforces_handles()       # get all the codeforces handles from the database
    try: 
        returnlist=[]
        for handle in codeforces_handle:                                # iterate over all the handles
            url = URL_BASE+'statistics/?'+clist_token+'&contest_id=38185697'+'&account_id='+str(handle[1])+'&with_problems=True&with_more_fields=True'           # get the rating changes of the user
            response = requests.get(url).json()
            if response['objects']:
                if 'CONTESTANT' in response['objects'][0]['more_fields']['participant_type']:
                    print(handle[1])
                    data=response['objects'][0]
                    data_dict={'handle':handle[0],'position':data['place'],'score':data['score'],'rating_change':data['rating_change'],'old_rating':data['old_rating'],'new_rating':data['new_rating']}
                    for i in data['problems']:
                        if 'upsolving' in data['problems'][i].keys():
                            continue
                        data_dict[i]=data['problems'][i]['result']
                    returnlist.append(data_dict)
        print(returnlist)
        return returnlist
        
    except Exception as e:
        print(e)
