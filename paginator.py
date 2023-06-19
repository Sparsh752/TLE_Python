from table2ascii import table2ascii as t2a
import discord
import asyncio

#Building pages(in embed form i.e. links can be added)
def embed_paginator(head_row, ndict, page_row):
    no_pages = len(ndict) // page_row + (len(ndict) % page_row != 0)
    pages = []
    for i in range(no_pages):

        # creates a single page of the embed
        content_body = ''
        for k in head_row:
            content_body += str(k) + '\a\a\a\a\a\a\a'
        content_body += '\n\n'
        for j in range(i * page_row, i * page_row + page_row):
            if j == len(ndict):
                break
            for head in head_row:
                content_body += str(ndict[j][head]) + '\a\a\a\a\a\a\a'
            content_body += '\n'
        # renders a single page
        page = discord.Embed( 
            description=content_body,
            color = discord.Color.blue()
        )
        page.set_footer(text="page: "+str(i + 1)+"/"+str(no_pages))
        pages.append(page)
    return pages

#Building pages(in simple text form)
def paginator(head_row, ndict, line_after_first_col, page_row):
    no_pages = len(ndict) // page_row + (len(ndict) % page_row != 0)
    pages = []
    for i in range(no_pages):
        page = []

        #builds one page
        for j in range(i * page_row, i * page_row + page_row):
            if j == len(ndict):
                break
            line = []
            for head in head_row:
                line.append(ndict[j][head])
            page.append(line)
        #converts table of one page into string
        output = t2a(
            header=head_row,
            body=page,
            first_col_heading=line_after_first_col
        )
        pages.append(output)
    return pages


#make pages with table
async def table(ctx, bot, head_row, ndict, line_after_first_col=False, page_row=5, isEmbed=False,isChannel=False, current_message=None):
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
    current = 0
    #creates pages
    if isEmbed:
        output = embed_paginator(head_row, ndict, page_row)
    else:
        output = paginator(head_row, ndict, line_after_first_col, page_row)
    #replace last page
    if current_message != None:
        await current_message.delete()
        await ctx.channel.send(f"{ctx.author.mention} Here is the list you wanted: :nerd:")
    if isChannel:
        if isEmbed:
            msg = await ctx.send(embed=output[current])
        else:
            msg = await ctx.send(f"```\n{output[current]}\npage: {current+1}/{len(output)}\n```")
    else:
        if isEmbed:
            msg =  await ctx.channel.send(embed=output[current])
        else:
            msg =  await ctx.channel.send(f"```\n{output[current]}\npage: {current+1}/{len(output)}\n```")
    # end if only single page required
    if len(output) < 2:
        return
    # adds reaction buttons for navigating through pages
    for button in buttons:
        await msg.add_reaction(button)
    # navigation through pages
    while True:
        try:
            if isChannel:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user in bot.get_all_members() and reaction.emoji in buttons, timeout=60.0)
            else:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
        # time for navigating is up, resets on each reaction
        except asyncio.TimeoutError:
            for button in buttons:
                await msg.remove_reaction(button, bot.user)
            return

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
                
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
                    
            elif reaction.emoji == u"\u27A1":
                if current < len(output)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(output)-1
            # remove user reaction after page changed
            for button in buttons:
                if reaction.emoji==button:
                    await msg.remove_reaction(button, user)
            # change message only if a new page was requested
            if current != previous_page:
                if isEmbed:
                    await msg.edit(embed=output[current])
                else:
                    await msg.edit(content=(f"```\n{output[current]}\npage: {current+1}/{len(output)}\n```"))


#=======================================Formate of calling ';help'==========================================
# from discord.ext import commands
# from paginator import table

# bot = commands.Bot(command_prefix=";", help_command=None, intents=discord.Intents.all())


# @bot.command()
# async def help(ctx):
#     await table(ctx, bot, head_row, ndict)


# ==============make sure to do isEmbed=True for link type table
# @bot.command()
# async def hi(ctx):
#     await table(ctx, bot, head_row, ndict, isEmbed=True)




#Format for link:   '[text to be printed](https://codeforces.com/)'

#========================================Format of head_row and ndict=====================================
# head_row = ['#', '=', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# ndict = [{'#': '#', '=': '=', 'A': 'A', 'B': 'M', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 1, 'B': '[hi](https://codeforces.com/)', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'O', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'} ]