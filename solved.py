import requests
from db import update_last_checked_codeforces, update_last_checked_atcoder
import datetime
import time
# This function is used to find the solved problems of a codeforces handle
# It returns a list of solved problems
# It also updates the last_checked_codeforces and last_solved_codeforces field in the database
async def find_solved_codeforces(codeforces_handle, last_solved_codeforces, last_checked_codeforces):
    url = "https://codeforces.com/api/user.status?handle="+codeforces_handle+"&from="+str(last_checked_codeforces+1)
    response = requests.get(url).json()
    data=response['result']
    for obj in data:
        if obj['verdict']=='OK':
            last_solved_codeforces.append(str(obj['problem']['contestId'])+':'+str(obj['problem']['index']))
    last_checked_codeforces += len(data)
    await update_last_checked_codeforces(codeforces_handle, last_solved_codeforces, last_checked_codeforces)
    return last_solved_codeforces
    
# This function is used to find the solved problems of a atcoder handle
# It returns a list of solved problems
# It also updates the last_checked_atcoder and last_solved_atcoder field in the database

async def find_solved_atcoder(atcoder_handle, last_solved_atcoder, last_checked_atcoder):
    mytime = time.mktime(last_checked_atcoder.timetuple())
    url = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user="+ atcoder_handle+"&from_second="+str(int(mytime))
    response = requests.get(url).json()
    for obj in response:
        if(obj['result']=='AC'):
            last_solved_atcoder.append(obj['problem_id'])
    last_checked_atcoder = datetime.datetime.now()
    await update_last_checked_atcoder(atcoder_handle, last_solved_atcoder, last_checked_atcoder)
    return last_solved_atcoder

