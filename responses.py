import clist_api
import _handle_verification_
import contest_info
import gitgud
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
    if p_message=="!next":                      #gives list of next contests on codeforces
        return clist_api.nextcontests()         #fetches next contests
    if msg_data[0]=="!rating_changes":
        if len(msg_data)==2:
            return await contest_info.codeforces_rating_changes(msg_data[1])
    if msg_data[0]=="gitgud":
        return await gitgud.gitgud(ctx)