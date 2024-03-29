from datetime import datetime
from quickchart import QuickChart
import discord
import json
import requests
from db import get_codeforces_handle

# creates a bar graph for the number of problems solved graph
async def bargraph(ctx,ndict, user, width=500, height=300):
    qc = QuickChart()
    qc.width = width
    qc.height = height
    labels = [] # each rating is a label in the graph
    data1 = [] # problems solved in contest
    data2 = [] # problems solved in virtual
    data3 = [] # problems solved in practice
    for key in ndict.keys():
        labels.append(key)
    labels.sort()
    for key in labels:
        data1.append(ndict[key][0])
    for key in labels:
        data2.append(ndict[key][1])
    for key in labels:
        data3.append(ndict[key][2])
    qc.config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Contest",
                "data": data1
            },
                {
                "label": "Virtual",
                "data": data2
            },
                {
                "label": "Practice",
                "data": data3
            }]
        },
        "options": {
            "title": {
                "display": True,
                "text": 'Number of problems solved -' + user,
            },
            "scales": {
                "xAxes": [
                    {
                        "stacked": True,
                    },
                ],
                "yAxes": [
                    {
                        "stacked": True,
                    },
                ],
            },
        },
    }

    page = discord.Embed()
    page.set_image(url=qc.get_short_url())
    await ctx.channel.send(embed=page)

# main function which returns the graph of rating vs number of problems solved
async def rating_vs_problems(ctx):
    user = await get_codeforces_handle(ctx)
    if(user == None):
        await ctx.channel.send(f"{ctx.author.mention} You have not identified your codeforces handle. First do it using ;identify_cf <handle>")
        return
    prob_rating = {}
    url = "https://codeforces.com/api/user.status?handle=" + user
    response = requests.get(url)
    submissions = response.json()['result']
    for submission in submissions:
        if (submission['verdict'] == 'OK'):
            if ('rating' in submission['problem'].keys()):
                rating = submission['problem']['rating']
                if (rating not in prob_rating.keys()):
                    prob_rating[rating] = [0, 0, 0]
                if (submission['author']['participantType'] == 'CONTESTANT'):
                    prob_rating[rating][0] += 1 # counting the number of questions solved while in contest
                elif (submission['author']['participantType'] == 'VIRTUAL'):
                    prob_rating[rating][1] += 1 # counting the number of questions solved while in virtual contest
                elif (submission['author']['participantType'] == 'PRACTICE'):
                    prob_rating[rating][2] += 1 # counting the number of questions solved while in practice
    await bargraph(ctx,prob_rating, user)

# calculates the graph required by the function problem_vs_time
async def timegraph(ctx,data, user, width=500, height=300):
    qc = QuickChart()
    qc.width = width
    qc.height = height
    qc.config = {
        "type": "line",
        "data": {
            "datasets": [
                {
                    "label": "Number of problems solved",
                    "backgroundColor": "rgba(255, 99, 132, 0.5)",
                    "borderColor": "rgb(255, 99, 132)",
                    "fill": False,
                    "data": data
                    # data format:
                    #         "data": [
                    #             {
                    #                 "x": "2020-06-14",
                    #                 "y": 75
                    #             },
                    #             {
                    #                 "x": "2020-06-16",
                    #                 "y": -53
                    #             },
                    #             {
                    #                 "x": "2020-06-18",
                    #                 "y": 31
                    #             },
                    #             {
                    #                 "x": "2020-06-19",
                    #                 "y": 6
                    #             }
                    #         ]
                }
            ]
        },
        "options": {
            "responsive": True,
            "title": {
                "display": True,
                "text": user
            },
            "scales": {
                "xAxes": [{
                    "type": "time",
                    "display": True,
                    "scaleLabel": {
                        "display": True,
                        "labelString": "Time"
                    },
                    "ticks": {
                        "major": {
                            "enabled": True
                        },
                        # "minor": {
                        #     "enabled": False
                        # }
                    }
                }],
                "yAxes": [{
                    "display": True,
                    "scaleLabel": {
                        "display": True,
                        "labelString": "Problems"
                    }
                }]
            },
            "elements": {
                "point": {
                    "radius": 0
                }
            }
        }
    }

    page = discord.Embed()
    page.set_image(url=qc.get_short_url())
    await ctx.channel.send(embed=page)

# calculates the cumulative number of problems done over time
async def problem_vs_time(ctx):
    user = await get_codeforces_handle(ctx)
    if(user == None):
        await ctx.channel.send(f"{ctx.author.mention} You have not identified your codeforces handle. First do it using ;identify_cf <handle>")
        return
    dates = []
    url = "https://codeforces.com/api/user.status?handle=" + user
    response = requests.get(url)
    submissions = response.json()['result']
    for submission in submissions:
        if (submission['verdict'] == 'OK'):
            date = submission['creationTimeSeconds']
            date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
            dates.append(date)
    dates.sort()
    ques_date = {}
    for i in range(len(dates)):
        if (i == 0):
            ques_date[dates[i]] = 1
        else:
            ques_date[dates[i]] = ques_date[dates[i - 1]] + 1
    data = []
    for date in ques_date.keys():
        data.append({
            "x": date,
            "y": ques_date[date]
        })
    Today = str(datetime.today())[0:10]
    if data[-1]['x'] != Today:
        data.append(
            {
                "x": Today,
                "y": data[-1]['y']
            }
        )
    await timegraph(ctx,data, user)

# calculates the graph required to the function performance
def timegraph2(data, user, width=500, height=300):
    qc = QuickChart()
    qc.width = width
    qc.height = height
    qc.config = {
        "type": "line",
        "data": {
            "datasets": [
                {
                    "label": "Performance",
                    "backgroundColor": "rgba(255, 99, 132, 0.5)",
                    "borderColor": "rgb(255, 99, 132)",
                    "fill": False,
                    "data": data
                }
            ]
        },
        "options": {
            "responsive": True,
            "title": {
                "display": True,
                "text": user
            },
            "scales": {
                "xAxes": [{
                    "type": "time",
                    "display": True,
                    "scaleLabel": {
                        "display": True,
                        "labelString": "Time"
                    },
                    "ticks": {
                        "major": {
                            "enabled": True
                        },
                    }
                }],
                "yAxes": [{
                    "display": True,
                    "scaleLabel": {
                        "display": True,
                        "labelString": "Rating"
                    }
                }]
            },
            "elements": {
                "point": {
                    "radius": 0
                }
            }
        }
    }

    page = discord.Embed()
    page.set_image(url=qc.get_short_url())
    return page


# returns an embed with performance graph image
async def performance(ctx,user):
    msg= await ctx.channel.send(f"{ctx.author.mention} Please wait while I fetch the data")
    ret_data = []
    try:
        url = "https://codeforces.com/api/user.rating?handle=" + user
        response = requests.get(url)
        data = response.json()['result']
    except:
        await msg.edit(content=f"Sorry {ctx.author.mention} I am unable to fetch the data")
        return
    for contest in data:
        date = contest['ratingUpdateTimeSeconds']
        date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
        performance = 0
        oldRating = contest['oldRating']
        newRating = contest['newRating']



# ===========Performance Calculation===================
        ratingChange = newRating - oldRating
        performance = 100
        if oldRating == 0:
            if newRating < 1400:
                ratingChange = newRating - 100
                performance =  100 + 3 * ratingChange
            else:
                ratingChange = newRating - 1400
                performance =  1400 + 3 * ratingChange
        else:
            performance =  oldRating + 3 * ratingChange




        ret_data.append({'x': date, 'y':performance})
    page = timegraph2(ret_data, user)
    await msg.edit(content=f"Here is the performance graph of {user}")
    await ctx.channel.send(embed=page)
    
