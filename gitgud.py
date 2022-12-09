import requests
import discord
from db import get_last_solved_problems, find_solved_codeforces, get_codeforces_handle
from codeforces_scraping import cf_get_random_question_rating, ac_get_random_question
async def get_user_rating(codeforces_handle):
    url = f'https://codeforces.com/api/user.rating?handle={codeforces_handle}'
    data = requests.get(url).json()
    if data['status'] == 'OK':
            return data['result'][-1]['newRating']
    else:
            return None

async def gitgud(ctx):
    discord_id = str(ctx.author.id)
    user_message = ctx.content
    user_message = user_message.split()
    if(user_message<2):
        await ctx.channel.send(f"{ctx.author.mention} Command format is incorrect")
        return
    if(user_message[1] not in ['cf','ac']):
        await ctx.channel.send(f"{ctx.author.mention} Please specify the judge from which you want the problem")
        return
    if(user_message[1]=='cf'):
        cf_handle = await get_codeforces_handle(discord_id)
        if(cf_handle==None):
            await ctx.channel.send(f"{ctx.author.mention} You have not identified your codeforces handle. First do it using ;identify_cf <handle>")
            return
        cf_rating = await get_user_rating(cf_handle)
        cf_rating = (cf_rating//100)*100
        last_checked,last_solved_problems = await get_last_solved_problems(ctx,'codeforces')
        solved_problems = await find_solved_codeforces(ctx,cf_handle,last_solved_problems,last_checked)
        random_problem = cf_get_random_question_rating(cf_rating)
        iter=0
        while(iter < 50 and random_problem in solved_problems):
            random_problem = cf_get_random_question_rating(cf_rating)
            iter+=1
        if(iter==50):
            await ctx.channel.send(f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :( ")
            return
        title = f"Contest {random_problem['prob_id']} {random_problem['prob_name']}"
        url = f"{random_problem['prob_link']}"
        description = f"Rating: {random_problem['prob_rating']}"
        embed = discord.Embed(title=title, url=url, description=description)
        await ctx.channel.send(f"Challenge problem for `{cf_handle}`", embed = embed)
