from db import get_codeforces_handle,get_last_solved_problems,find_solved_codeforces
from gitgud import get_cf_user_rating
from codeforces_scraping import cf_get_random_question_rating
import asyncio
import discord
class author:
    id=5
class cttx:
    author=author()

async def challenge_question_cf(ctx,bot):
    user_message = ctx.content
    user_message=user_message.split()
    if len(user_message) < 3:
        await ctx.channel.send(f"{ctx.author.mention} Command format is incorrect")
        return
    if(user_message[1] not in ['cf','ac']):
        await ctx.channel.send(f"{ctx.author.mention} Please specify the judge correctly. It can be either `cf` or `ac`")
        return
    if(user_message[1]=='cf'):
        discord_id = ctx.mentions[0].id
        ctx_second=cttx()
        ctx_second.author.id=discord_id
        cf_handle_1 = await get_codeforces_handle(ctx)
        cf_handle_2 = await get_codeforces_handle(ctx_second)
        if cf_handle_1 is None:
            await ctx.channel.send(f"{ctx.author.mention} Please set your Codeforces handle first")
            return
        if cf_handle_2 is None:
            await ctx.channel.send(f"{cf_handle_2} Please set your Codeforces handle first")
            return
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
        while(iter < 50 and random_problem in solved_problems):
            random_problem = cf_get_random_question_rating(cf_rating)
            iter+=1
        if(iter==50):
            await ctx.channel.send(f"{ctx.author.mention} Sorry we could not give you a problem now. Please try again later :( ")
            return
        msg=await ctx.channel.send(f"{ctx.mentions[0].mention} Do you want to accept the challenge?")
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
                    title = f"Contest {random_problem['prob_id']} {random_problem['prob_name']}"
                    url = f"{random_problem['prob_link']}"
                    description = f"Rating: {random_problem['prob_rating']}"
                    embed = discord.Embed(title=title, url=url, description=description)
                    await ctx.channel.send(f"Challenge problem for `{cf_handle_1}` and `{cf_handle_2}`", embed = embed)
                    return
                elif reaction.emoji == "❌":
                    await ctx.channel.send(f"{ctx.author.mention} {ctx.mentions[0].mention} has declined the challenge")
                    return

