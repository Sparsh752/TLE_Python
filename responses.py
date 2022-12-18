import clist_api
import _handle_verification_
import contest_info
import gitgud
import db
import random 
async def handle_response(message,ctx):
    p_message=message.lower()                   #to maintain uniformity
    msg_data=p_message.split()               #to split the message into words
    if p_message=="hello":
        return "Hey there "+ctx.author.name
    if p_message=="roll":
        return str(random.randint(1,6))
    if p_message=="!help":
        return "Commands: hello, roll"
    if msg_data[0]==";gitgud":
        return await gitgud.gitgud(ctx)
    if msg_data[0]==";gotgud":
        return await gitgud.gotgud(ctx)
    if msg_data[0]==";nogud":
        if len(msg_data)==2:
            if msg_data[1]=="cf":
                return await gitgud.nogud_cf(ctx)
            elif msg_data[1]=="ac":
                return await gitgud.nogud_atcoder(ctx)
    if msg_data[0]==";gimme":
        return await gitgud.gimme(ctx)
