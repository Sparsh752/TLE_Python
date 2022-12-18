from db import get_codeforces_handle,get_last_solved_problems,find_solved_codeforces,get_atcoder_handle,find_solved_atcoder
from gitgud import get_cf_user_rating,get_ac_user_rating,check_if_solved,get_ac_problem_difficulty,convertAC2CFrating,check_if_solved_ac
from codeforces_scraping import cf_get_random_question_rating,ac_get_random_question
import asyncio
import discord
import time
import random
class author:
    id=5
class cttx:
    author=author()

async def challenge_question_cf(ctx,bot):
    user_message = ctx.content
    user_message=user_message.split()
    msg= await ctx.channel.send(f"{ctx.author.mention} Checking the correctness of command")
    if len(user_message) < 3:
        await msg.edit(content=f"{ctx.author.mention} Command format is incorrect")
        return
    if(user_message[1] not in ['cf','ac']):
        await msg.edit(content=f"{ctx.author.mention} Please specify the judge correctly. It can be either `cf` or `ac`")
        return
    if len(ctx.mentions) == 0:
            await msg.edit(content=f"{ctx.author.mention} The mentioned user can't be challenged")
            return
    if discord_id == ctx.author.id:
        await msg.edit(content=f"{ctx.author.mention} You cannot challenge yourself")
        return
    if discord_id == bot.user.id:
        await msg.edit(content=f"{ctx.author.mention} You cannot challenge me")
        return
    if(user_message[1]=='cf'):
        discord_id = ctx.mentions[0].id
        ctx_second=cttx()
        ctx_second.author.id=discord_id
        cf_handle_1 = await get_codeforces_handle(ctx)
        cf_handle_2 = await get_codeforces_handle(ctx_second)
        if cf_handle_1 is None:
            await msg.edit(content=f"{ctx.author.mention} Please set your Codeforces handle first")
            return
        if cf_handle_2 is None:
            await msg.edit(content=f"{cf_handle_2} Please set your Codeforces handle first")
            return
        await msg.edit(content=f"Wait {ctx.author.mention} the bot is thinking 🤔 a problem for you....... ")
        cf_rating = await get_cf_user_rating(cf_handle_2)
        cf_rating = (cf_rating//100)*100
        last_checked_1,last_solved_problems_1 = await get_last_solved_problems(ctx,'codeforces')
        last_checked_2,last_solved_problems_2 = await get_last_solved_problems(ctx_second,'codeforces')
        solved_problems_1 = await find_solved_codeforces(ctx,cf_handle_1,last_solved_problems_1,last_checked_1)
        solved_problems_2 = await find_solved_codeforces(ctx_second,cf_handle_2,last_solved_problems_2,last_checked_2)
        solved_problems=[]
        solved_problems.extend(solved_problems_1)
        solved_problems.extend(solved_problems_2)
        random_problem = cf_get_random_question_rating(cf_rating)
        iter=0
        while(iter < 50 and random_problem["prob_id"] in solved_problems):
            random_problem = cf_get_random_question_rating(cf_rating)
            iter+=1
        if(iter==50):
            await msg.edit(content=f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :( ")
            return
        await msg.edit(content=f"{ctx.mentions[0].mention} Do you want to accept the challenge by {ctx.author.mention}?")
        buttons = ["✅", "❌"]
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.mentions[0] and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                await msg.edit(content=f"{ctx.author.mention} Ig that's a no from {ctx.mentions[0].mention}")
                for button in buttons:
                    await msg.remove_reaction(button, bot.user)
                return
            else:
                if reaction.emoji == "✅":
                    await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} has accepted the challenge")
                    title = f"Contest {random_problem['prob_id']} {random_problem['prob_name']}"
                    url = f"{random_problem['prob_link']}"
                    description = f"Rating: {random_problem['prob_rating']}"
                    embed = discord.Embed(title=title, url=url, description=description)
                    await ctx.channel.send(f"Challenge problem for `{cf_handle_1}` and `{cf_handle_2}`, you have 1 hour to complete the challenge", embed = embed)
                    timeout = time.time() + 60*60
                    while True:
                        check1 = await check_if_solved(ctx,cf_handle_1,[random_problem["prob_id"]],"cf")
                        check2 = await check_if_solved(ctx_second,cf_handle_2,[random_problem["prob_id"]],"cf")
                        if check1 and check2:
                            await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} both of you have solved the problem at the same time")
                            break
                        elif check1:
                            await ctx.channel.send(f"{ctx.author.mention} {cf_handle_1} has solved the problem first and won the challenge")
                            break
                        elif check2:
                            await ctx.channel.send(f"{ctx.mention[0].mention} {cf_handle_2} has solved the problem first and won the challenge")
                            break
                        elif time.time() > timeout:
                            await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} both of you have not solved the problem in time")
                            break
                        else:
                            await asyncio.sleep(10)
                elif reaction.emoji == "❌":
                    await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} has declined the challenge")
                    return
    else:
        discord_id = ctx.mentions[0].id
        ctx_second=cttx()
        ctx_second.author.id=discord_id
        ac_handle_1 = await get_atcoder_handle(ctx)
        ac_handle_2 = await get_atcoder_handle(ctx_second)
        if ac_handle_1 is None:
            await ctx.channel.send(f"{ctx.author.mention} Please set your Codeforces handle first")
            return
        if ac_handle_2 is None:
            await ctx.channel.send(f"{ctx.mentions[0].mention} Please set your Codeforces handle first")
            return
        last_checked_1,last_solved_problems_1 = await get_last_solved_problems(ctx,'atcoder')
        last_checked_2,last_solved_problems_2 = await get_last_solved_problems(ctx_second,'atcoder')
        solved_problems_1 = await find_solved_atcoder(ctx,ac_handle_1,last_solved_problems_1,last_checked_1)
        solved_problems_2 = await find_solved_atcoder(ctx_second,ac_handle_2,last_solved_problems_2,last_checked_2)
        solved_problems=[]
        solved_problems.extend(solved_problems_1)
        solved_problems.extend(solved_problems_2)
        n=random.randint(0,1)
        contest_type=''
        question_type=''
        if n==1:
            contest_type='abc'
            q=random.randint(0,3)
            question_types=['b','c','d','e']
            question_type=question_types[q]
        else:
            contest_type='arc'
            q=random.randint(0,2)
            question_types=['a','b','c']
            question_type=question_types[q]
        random_problem = ac_get_random_question(contest_type,question_type)
        iter=0
        while(iter < 50 and random_problem["problem"]["id"] in solved_problems):
            random_problem = ac_get_random_question(contest_type, question_type)
            difficulty = await get_ac_problem_difficulty(random_problem['problem']['id'])
            if difficulty is None :
                random_problem = None
            iter+=1
        if(iter==50):
            await ctx.channel.send(f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :( ")
            return
        difficulty = await get_ac_problem_difficulty(random_problem['problem']['id'])
        equv_cf_prob_rating = await convertAC2CFrating(int(difficulty))
        msg=await ctx.channel.send(f"{ctx.mentions[0].mention} Do you want to accept the challenge by {ctx.author.mention}?")
        buttons = ["✅", "❌"]
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.mentions[0] and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                for button in buttons:
                    await msg.remove_reaction(button, bot.user)
                return
            else:
                if reaction.emoji == "✅":
                    await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} has accepted the challenge")
                    title = f"{random_problem['problem']['title']}"
                    url = f"{random_problem['prob_link']}"
                    description = f"Dificulty: {int(equv_cf_prob_rating)}"
                    embed = discord.Embed(title=title, url=url, description=description)
                    await ctx.channel.send(f"Challenge problem for `{ac_handle_1}` and `{ac_handle_2}`, you have 1 hour to complete the challenge", embed = embed)
                    timeout = time.time() + 60*60
                    while True:
                        check1 = await check_if_solved_ac(ctx,ac_handle_1,[random_problem["problem"]["id"]])
                        check2 = await check_if_solved_ac(ctx_second,ac_handle_2,[random_problem["problem"]["id"]])
                        if check1 and check2:
                            await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} both of you have solved the problem at the same time")
                            break
                        elif check1:
                            await ctx.channel.send(f"{ctx.author.mention} {ac_handle_1} has solved the problem first and won the challenge")
                            break
                        elif check2:
                            await ctx.channel.send(f"{ctx.mention[0].mention} {ac_handle_2} has solved the problem first and won the challenge")
                            break
                        elif time.time() > timeout:
                            await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} both of you have not solved the problem in time")
                            break
                        else:
                            await asyncio.sleep(10)

                elif reaction.emoji == "❌":
                    await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} has declined the challenge")
                    return