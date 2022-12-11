from table2ascii import table2ascii as t2a
import asyncio

#Building pages
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
        
        output = t2a(
            header=head_row,
            body=page,
            first_col_heading=line_after_first_col
        )
        pages.append(output)
    return pages


#make pages with table
async def table(ctx, bot, head_row, ndict, line_after_first_col=False, page_row=5):
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
    current = 0

    output = paginator(head_row, ndict, line_after_first_col, page_row)

    ##if message requires Title then make an embed and print here------

    msg =  await ctx.send(f"```\n{output[current]}\npage: {current+1}/{len(output)}\n```")
    
    if len(output) < 2:
        return

    for button in buttons:
        await msg.add_reaction(button)
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

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

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(content=(f"```\n{output[current]}\npage: {current+1}/{len(output)}\n```"))


#=======================================Formate of calling ';help'==========================================
# from discord.ext import commands
# from paginator import table

# bot = commands.Bot(command_prefix=";", help_command=None, intents=discord.Intents.all())


# @bot.command()
# async def help(ctx):
#     await table(ctx, bot, head_row, ndict)



#========================================Format of head_row and ndict=====================================
# head_row = ['#', '=', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# ndict = [{'#': '#', '=': '=', 'A': 'A', 'B': 'M', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'},
#          {'#': '#', '=': '=', 'A': 'O', 'B': 'B', 'C': 'C', 'D': 'D', 'E':'E', 'F':'F', 'G':'G', 'H':'H'} ]