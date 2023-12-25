#Documentation: https://ai.google.dev/tutorials/python_quickstart
import discord
import bot
import asyncio

from dotenv import load_dotenv
load_dotenv('process.env')

import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

GOOGLE_API = os.environ.get('GOOGLE_API')

#source(for getting API): https://ai.google.dev/?utm_source=google&utm_medium=cpc&utm_campaign=brand_core_brand&gad_source=1

genai.configure(api_key=GOOGLE_API)
model = genai.GenerativeModel('gemini-pro')


async def start_chat(ctx,bot):

    await ctx.channel.send("Ask me anything")
    prompt="CONTEXT: Your name is 'EnEm Jr.' . You are a replica of a legendary competitve programmer named 'EnEm' trained by Competitive Programming Module, IIT Guwahati.Your name is 'EnEm Jr.' . Since EnEm left the club, now it is your responsibility to guide the young ones. Don't forget it. You are a professional coach,a guide and a responsible programmer and always help aspiring programmers . You prefer Codeforces and AtCoder more as they are best sites for practice according to you. You also prefer Leetcode for Data Structures and Algorithm. You pick random problems from https://codeforces.com/problemset if codeforces is concerned. Your answers possess humour, motivation and kindness. Also you don't repeat answers and stick around the world of Competitive Programming. Don't forget to be humble and apologize for your mistakes. You also tend to ignore mild cuss words in a funny way. Now give answers to the 'User' in a motivating way .You also can ask questions sometimes.\n"
    
    
    while True:
        
        def is_ok(m):
            if ctx.author == bot.user:
                return 0
            else:
                return 1
        try:
            msg = await bot.wait_for('message', check=is_ok, timeout=150.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send(f'Sorry, you took too long to respond.')

        new_prompt = str(msg.content)
            

        
        if new_prompt[0]==';':
            await ctx.channel.send("Thanks for chatting. Ending Chat Mode.")
            break
        
        prompt+="LATEST User: " + new_prompt
        if len(new_prompt)<=3:
            prompt+="Now change the topic of conversation."
        
        response = model.generate_content(prompt + " Answer in the shortest way possible. " )
        
        await ctx.channel.send(response.text)
        prompt+=(" Your answer: " + response.text)
        
        
    return
