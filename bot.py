import discord
from contest_reminder import reminder
from _handle_verification_ import handle_verification
import gitgud
from paginator import table
import asyncio
import clist_api
import db
import stalk
import contest_info
import challenge
from graphs import rating_vs_problems, problem_vs_time,performance
from help import help as help_command
import os
from dotenv import load_dotenv
load_dotenv('process.env') 

async def reconnect():
    await asyncio.sleep(10)
    await client.close()
    await client.connect()
client = None
async def run_discord_bot():
    global client
    TOKEN=os.environ.get('TOKEN')    #bot id
    print(TOKEN)
    print('hello')
    client = discord.Client(intents=discord.Intents.all())                              #giving permissions and intents to the bot
    # guild_id=1048212913539784805        #guild id
    # guild=client.get_guild(guild_id)
    @client.event
    async def on_ready():                                                               #logged in successfully
        print('hello')
        # await reminder(client)
    @client.event
    async def on_disconnect():
        await reconnect()
    @client.event
    async def on_connection_error(error):
        print(error)
        await reconnect()

    @client.event
    async def on_message(ctx):
        if ctx.author == client.user:                                               #will keep messaging itself without this
            return
        user_message=str(ctx.content)
        if (user_message.startswith(';challenge')):
            await challenge.challenge_question_cf(ctx,client)
        if (user_message.startswith(';identify')):
            await handle_verification(ctx,client)
        # if user_message[0]=='?':                                                        #checking if message is private
        #     user_message=user_message[1:]
        #     await send_message(ctx,user_message,is_private=True) #message is private
        elif user_message.split()[0]==";gitlog":
             mydict, msg =  await gitgud.gitlog(ctx)
             if msg=="error":
                return
             if(len(mydict)==0):
                await msg.edit(content=f"{ctx.author.mention} You have not solved any problem yet. use ;gitgud to get a problem")
             else:   
                await table(ctx,client,['Problem Name','Problem Rating','Points'], mydict, isEmbed=True, current_message=msg)
        elif user_message.split()[0]==";next":
            await clist_api.nextcontests(ctx)
        elif user_message.split()[0]==";leaderboard":
            if len(user_message.split())==2:
                mylist,res = await db.Leaderboard_list(ctx,user_message.split()[1])
                if(len(mylist)==0):
                    await res.edit(content=f"{ctx.author.mention} No one is there on leaderboard yet")
                if(user_message.split()[1]=="cf"):
                    await table(ctx,client,['Discord Name','Score','Codeforces Handle'], mylist,current_message=res)
                elif(user_message.split()[1]=="ac"):
                    await table(ctx,client,['Discord Name','Score','Atcoder Handle'], mylist,current_message=res)
                elif(user_message.split()[1]=="both"):
                    await table(ctx,client,['Discord Name','Total Score'], mylist,current_message=res)
                else:
                    await res.edit(content=f"{ctx.author.mention} Please enter a valid platform")
            else:
                await ctx.channel.send(f"{ctx.author.mention} Please enter a valid platform")
        elif user_message.split()[0]==";stalk":
            if len(user_message.split())==2:
                temp =  await stalk.stalk_user(ctx,user_message.split()[1])
                if(temp==None):
                    return
                header,mylist,msg = temp[0],temp[1],temp[2]
                if(len(mylist)==0):
                    await msg.edit(content=f"{ctx.author.mention} No user found")
                else:
                    await table(ctx,client,header,mylist,current_message=msg)
            elif len(user_message.split())==3:
                if user_message.split()[2]=="hardest":
                    header,mylist,msg = await stalk.stalk_user(ctx,user_message.split()[1],hardest=True)
                    if(len(mylist)==0):
                        await msg.edit(content=f"{ctx.author.mention} No user found")
                    else:
                        await table(ctx,client,header,mylist,current_message=msg)
                elif user_message.split()[2].isdigit():
                    header,mylist,msg = await stalk.stalk_user(ctx,user_message.split()[1],R=int(user_message.split()[2]))
                    if(len(mylist)==0):
                        await msg.edit(content=f"{ctx.author.mention} No user found")
                    else:
                        await table(ctx,client,header,mylist,current_message=msg)
                else:
                    await ctx.channel.send(f"{ctx.author.mention} Please follow the message format")
                    return
            else:
                await ctx.channel.send(f"{ctx.author.mention} Please follow the message format")
        elif user_message.split()[0]==";ratingchange":
            if len(user_message.split())==3:
                if(user_message.split()[1]=="cf"):
                    mylist,header,msg=await contest_info.codeforces_rating_changes(str(user_message.split()[2]),ctx)
                    if header=="error":
                        await msg.edit(content=f"{ctx.author.mention} Some error occurred 🧐")
                    elif(len(mylist)==0):
                        await msg.edit(content=f"{ctx.author.mention} Either no user gave the contest or the contest id is invalid 😲")
                    else:
                        await table(ctx,client,header,mylist,current_message=msg)
                elif(user_message.split()[1]=="ac"):
                    mylist,header,msg=await contest_info.atcoder_rating_changes(str(user_message.split()[2]),ctx)
                    if header=="error":
                        await msg.edit(content=f"{ctx.author.mention} Perhaps the contest id is invalid 🧐")
                    elif(len(mylist)==0):
                        await msg.edit(content=f"{ctx.author.mention} No user gave this contest or contest is unrated 😲")
                    else:
                        await table(ctx,client,header,mylist,current_message=msg)
                else:
                    await ctx.channel.send(f"{ctx.author.mention} Please specify a valid platform")
            else:
                await ctx.channel.send(f"{ctx.author.mention} Please follow the message format")
        elif user_message.split()[0]==";performance":
            if len(user_message.split())==2:
                await performance(ctx,user_message.split()[1])
            else:
                await ctx.channel.send(f"{ctx.author.mention} Please follow the message format")
        elif user_message.split()[0]==";graph":
            if(user_message.split()[1]=="rvp"):
                await rating_vs_problems(ctx)
            elif(user_message.split()[1]=="pvt"):
                await problem_vs_time(ctx)
            else:
                await ctx.channel.send(f"{ctx.author.mention} Please follow the message format")
        elif user_message.split()[0]==";help":
            content=await help_command()
            await ctx.channel.send(embed=content)
        elif user_message.split()[0]==";gitgud":
            return await gitgud.gitgud(ctx)
        elif user_message.split()[0]==";gotgud":
            return await gitgud.gotgud(ctx)
        elif user_message.split()[0]==";nogud":
            if len(user_message.split())==2:
                if user_message.split()[1]=="cf":
                    return await gitgud.nogud_cf(ctx)
                elif user_message[1]=="ac":
                    return await gitgud.nogud_atcoder(ctx)
        elif user_message.split()[0]==";gimme":
            return await gitgud.gimme(ctx)
        return "Sorry, I didn't understand that :smiling_face_with_tear: Try ;help for more info"
        



    client.run(TOKEN)

