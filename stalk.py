import requests
from operator import itemgetter

async def stalk_user(ctx,codeforces_handle,hardest=False,R=None):
    url = "https://codeforces.com/api/user.status?handle="+str(codeforces_handle)+"&from="+str(1)
    response = requests.get(url,timeout=5).json()
    total=len(response['result'])
    url = "https://codeforces.com/api/user.status?handle="+str(codeforces_handle)+"&count="+str(total)
    response = requests.get(url).json()
    data=response['result']
    n_dict=[]
    for obj in data:
        if obj['verdict']=='OK':
            n_dict.append({'Prob':str(obj['problem']['name']),'Rating':int(obj['problem']['rating'])})
    if hardest==True:
        n_dict = sorted(n_dict, key=itemgetter('Rating'),reverse=True)
    if R!=None:
        temp=[]
        for i in n_dict:
            if i['Rating']>=R:
                temp.append(i)
        n_dict=temp 
    head_row=['Prob','Rating']
    return head_row,n_dict