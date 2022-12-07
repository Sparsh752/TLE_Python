import discord
import responses
async def send_message(message,user_message,is_private,user_name):                                      #giving back response to the user
    try:
        response=responses.handle_response(str(user_message),str(user_name))                            #fetching response
        await message.author.send(response) if is_private else await message.channel.send(response)     #sending response in dm if private or in channel if not
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN='MTA0ODIzNTAxMjcxMTAxMDM2NA.G6wi4q.6AE7Q3otjPtQ-Hu9JJ0C6hNnVDEc_M9xSsmLTc'    #bot id
    print('hello')
    client = discord.Client(intents=discord.Intents.all())                              #giving permissions and intents to the bot
    
    @client.event
    async def on_ready():                                                               #logged in successfully
        print('We have logged in')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:                                               #will keep messaging itself without this
            return
    
        username=str(message.author.name)                                               #extracting useful info from the message
        user_message=str(message.content)
        channel=str(message.channel)
        print('Message from '+username+' in '+channel+': '+user_message)
        print(message)
        if user_message[0]=='?':                                                        #checking if message is private
            user_message=user_message[1:]
            await send_message(message,user_message,is_private=True,user_name=username) #message is private
        else:
            await send_message(message,user_message,is_private=False,user_name=username)#message is not private


    client.run(TOKEN)