import db
import requests
import json
import asyncio
from operator import itemgetter
import rating_roles
import os
URL_BASE = 'https://clist.by/api/v2/' # common url for clist api call
clist_token=os.environ.get('clist_token')


# function to convert cf contest name to contest id
async def codeforces_contest_id_finder(event_name):
    url = URL_BASE+'contest/?'+clist_token+'&resource_id=1' + \
        '&order_by=-start&limit=1000'  # url to be fetched
    if (event_name == None):  # if event is none, return none
        return None
    try:
        resp = requests.get(url)  # fetching response
        # converting to json
        details = json.dumps(resp.json(), ensure_ascii=False)
        data = json.loads(details)['objects']
        for contest in data:  # iterating over all fetched contests to find the contest id
            if contest['href'] == 'https://codeforces.com/contests/'+event_name:
                return contest['id']
    except Exception as e:  # tackiling errors
        print(e)

# used when someone has given a contest as an unrated user
def fun(a):  # function to return -- if a is none
    if a == None:
        return "--"
    else:
        return a


# function to get the rating changes and standing of all users in the database that participated in 
# the contest being given by the user
async def codeforces_rating_changes(event_name, ctx):
    msg = await ctx.channel.send(f"{ctx.author.mention} Getting data for contest `{event_name}` from codeforces ...")
    # get all the codeforces handles from the database
    codeforces_handle = await db.get_all_codeforces_handles()
    returnlist = []
    req_list = []
    header = ['rank', 'handle', 'score', 'Δ', 'from', 'to']
    for handle in codeforces_handle:                                # iterate over all the handles
        try:
            try:
                url = "https://codeforces.com/api/user.rating?handle=" + \
                    str(handle[0])
                response = requests.get(url)
                response = response.json()                        # fetching response
                url2 = "https://codeforces.com/api/contest.standings?contestId=" + \
                    str(event_name)+"&handles=" + str(handle[0])
                response2 = requests.get(url2)
                response2 = response2.json()
            except Exception as e:
                print(e)
                continue
            req_list = list(filter(lambda d: d['contestId'] in [
                            int(event_name)], response['result']))
            if len(req_list) == 0:
                continue
            else:
                data = req_list[0]
                data_dict = {'rank': data['rank'], 'handle': handle[0], 'score': response2['result']['rows'][0]['points'],
                             'Δ': data['newRating']-data['oldRating'], 'from': data['oldRating'], 'to': data['newRating']}
                # append the dictionary to the return list
                returnlist.append(data_dict)
        except Exception as e:
            print(e)
            continue
    if (len(returnlist) == 0):
        return returnlist, header, msg
    returnlist = sorted(returnlist, key=itemgetter('rank'))
    return returnlist, header, msg  # returning the list


# function to convert atcoder contest name to contest id
async def atcoder_contest_id_finder(event_name):
    url = URL_BASE+'contest/?'+clist_token+'&resource_id=93' + \
        '&order_by=-start&limit=1000'  # url to be fetched
    if (event_name == None):  # if event is none, return none
        return None
    try:
        resp = requests.get(url)  # fetching response
        # converting to json
        details = json.dumps(resp.json(), ensure_ascii=False)
        data = json.loads(details)['objects']
        for contest in data:  # iterating over all fetched contests to find the contest id
            if contest['href'] == 'https://atcoder.jp/contests/'+event_name:
                return contest['id']
    except Exception as e:  # tackiling errors
        print(e)


# function to get the rating changes of all users in atcoder
async def atcoder_rating_changes(event_name, ctx):
    msg = await ctx.channel.send(f"{ctx.author.mention} Getting data for contest `{event_name}` from atcoder ...")
    # get all the codeforces handles from the database
    atcoder_handle = await db.get_all_atcoder_handles()
    # get the contest id of the contest
    contest_id = await atcoder_contest_id_finder(event_name)
    # if the contest id is none, return none
    if contest_id == None:
        return None, "error", msg
    question_url = URL_BASE+'statistics/?'+clist_token+'&contest_id=' + \
        str(contest_id)+'&order_by=place' + \
        '&with_problems=True&limit=1'  # url to be fetched
    # fetching response
    response = requests.get(question_url)
    # converting to json
    try:
        response = response.json()
    except Exception as e:
        print(e)
        return None, "error", msg
    problemlist = []
    header = ['rank', 'handle', 'score', 'Δ', 'to']
    # iterating over all the problems
    try:
        for i in response['objects'][0]['problems']:
        # appending the problem codes to a list
            problemlist.append(i)
    except Exception as e:
        print(e)
        return None, "error", msg
    # try:
    returnlist = []
    for handle in atcoder_handle:                                # iterate over all the handles
        url = URL_BASE+'statistics/?'+clist_token+'&contest_id='+str(contest_id)+'&account_id='+str(handle[1])+'&with_problems=True&with_more_fields=True'           # url to be fetched
        response = requests.get(url)
        print(response.status_code)
        if response.status_code!=200:
            print(handle)
            continue
        response = response.json()                        # fetching response

        # if the response is not empty
        if response['objects']:
            # if the user is a contestant
            if "is_rated" not in response['objects'][0]['more_fields'].keys():
                continue
            if response['objects'][0]['more_fields']['is_rated'] == True:
                # get the data of the user
                data = response['objects'][0]
                data_dict = {'rank': data['place'], 'handle': handle[0], 'score': data['score'], 'Δ': fun(data['rating_change']), 'to': fun(data['new_rating'])}  # create a dictionary of the data
                for i in problemlist:  # adding the solved problems to the dictionary
                    if i in data['problems'].keys():
                        if data['problems'][i]['verdict'] == "AC":
                            data_dict[i] = data['problems'][i]['result']
                        else:
                            data_dict[i] = ""
                    else:
                        data_dict[i] = ""
                    # append the dictionary to the return list
                returnlist.append(data_dict)
    if (len(returnlist) == 0):
        return returnlist, header, msg
    header.extend(problemlist)
        # sorting the list according to the rank
    returnlist = sorted(returnlist, key=itemgetter('rank'))
    return returnlist, header, msg  # returning the list

    # except Exception as e:
    #     print(e)
    #     return None,"error"


# function to get the rating changes of all users in the databse that participated in the last 
# contest conducted on codeforces
async def codeforces_rating_changes_shower(event_name, bot, channel):
    # get all the codeforces handles from the database
    codeforces_handle = await db.get_all_codeforces_handles()
    returnlist = []
    req_list = []
    print(await codeforces_contest_id_finder(event_name))
    header = ['rank', 'handle', 'Δ', 'from', 'to']
    for handle in codeforces_handle:                                # iterate over all the handles
        print(handle)
        try:
            try:
                url = "https://codeforces.com/api/user.rating?handle=" + \
                    str(handle[0])
                response = requests.get(url)    # fetching response
                response = response.json()
            except Exception as e:
                print('hi')
                print(e)
                continue
            req_list = list(filter(lambda d: d['contestId'] in [
                            int(event_name)], response['result']))
            if len(req_list) == 0:
                continue
            else:
                data = req_list[0]
                data_dict = {'rank': data['rank'], 'handle': handle[0], 'Δ': data['newRating'] -
                             data['oldRating'], 'from': data['oldRating'], 'to': data['newRating']}
                await rating_roles.rating_role(str(handle[2]), data['newRating'], bot, channel)
                # append the dictionary to the return list
                returnlist.append(data_dict)
        except Exception as e:
            print('hi')
            print(e)
            continue
    if (len(returnlist) == 0):
        return returnlist, header
    returnlist = sorted(returnlist, key=itemgetter('rank'))
    return returnlist, header  # returning the list
