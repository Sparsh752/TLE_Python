import clist_api

import random 
def handle_response(message,username):
    p_message=message.lower()
    if p_message=="hello":
        return "Hey there "+username
    if p_message=="roll":
        return str(random.randint(1,6))
    if p_message=="!help":
        return "Commands: hello, roll"
    if p_message=="!next":
        return clist_api.nextcontests()
