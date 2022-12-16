from datetime import datetime
from quickchart import QuickChart
import discord
import json
import requests
from db import get_codeforces_handle

async def bargraph(ctx,ndict, user, width=500, height=300):
    qc = QuickChart()
    qc.width = width
    qc.height = height
    labels = []
    data1 = []
    data2 = []
    data3 = []
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
                "label": "Constest",
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


async def rating_vs_problems(ctx):
    user = await get_codeforces_handle(ctx)
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
                    prob_rating[rating][0] += 1
                elif (submission['author']['participantType'] == 'VIRTUAL'):
                    prob_rating[rating][1] += 1
                elif (submission['author']['participantType'] == 'PRACTICE'):
                    prob_rating[rating][2] += 1
    await bargraph(ctx,prob_rating, user)


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


async def problem_vs_time(ctx):
    user = await get_codeforces_handle(ctx)
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
