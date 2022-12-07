import requests

URL_BASE=URL_BASE = 'https://clist.by/api/v2/'

def nextcontests():
    clist_token="username=Sparsh&api_key=c5b41252e84b288521c92f78cc70af99464345f8"
    url=URL_BASE+'contest/?'+clist_token+'&resource_id=1&limit=5&start__gte=2022-12-05%2012:00:00&order_by=start'           #url of the list of contests on codeforces
    try:
        resp=requests.get(url)                                                                                              #fetches response from the url
        list=resp.json()['objects']                                                                                         #splitting into json objects
        return_string="Sr No. | Name | Platform | Start Time (dd-mm-yyyy) | Duration (in minutes) \n"
        count=1
        for item in list:
            return_string=return_string+str(count)+"  "+item['event']+"  "+item['resource']+"  "+item['start'][8:10]+item['start'][4:8]+item['start'][:4]+" "+item['start'][11:16]+"  "+str(item['duration']/60)+"\n"
            count=count+1
        return return_string                                                                                                #returns string to be messaged by bot
    except Exception as e:                                                                                                  #in case of any error, code doesn't crash but tells about it in the terminal
        print(e)
        return "Error"