import clist_api
import _handle_verification_

import random 
async def handle_response(message,ctx):
    p_message=message.lower()                   #to maintain uniformity
    if p_message=="hello":
        return "Hey there "+ctx.author.name
    if p_message=="roll":
        return str(random.randint(1,6))
    if p_message=="!help":
        return "Commands: hello, roll"
    if p_message=="!next":                      #gives list of next contests on codeforces
        return clist_api.nextcontests()         #fetches next contests