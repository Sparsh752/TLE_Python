import discord

# A simple message displayed when the ;help command is called
async def help():
    content_body = [
        [";help", "Shows this message"],
        [";identify\_cf <handle>", "Identify yourself on codeforces"],
        [";identify\_ac <handle>", "Identify yourself on atcoder"],
        [";gitgud cf", "Gives you a codeforces problem to solve"],
        [";gitgud cf +x", "Gives you a codeforces problem of rating (x+current\_rating) where x = 100,200,300,400 to solve"],
        [";gitgud ac abc e", "Gives you a atcoder problem of Atcoder Beginner Contest indexed 'e' to solve ( Here you can replace 'abc' with 'arc' or 'agc' and 'e' with 'a','b','c','d','e','f' whichever applicable )"],
        [";gotgud cf", "If you solved the problem given by ;gitgud cf or ;gimme"],
        [";gotgud ac", "If you solved the problem given by ;gitgud ac"],
        [";nogud cf", "If you didn't solve the problem given by ;gitgud cf or ;gimme and want to skip it"],
        [";nogud ac", "If you didn't solve the problem given by ;gitgud ac and want to skip it"],
        [";gimme <tag>", "Gives you a problem of tag <tag> to solve. If the tag contains a space then replace it with a '\_' For example binary search -> binary\_search"],
        [";challenge cf <user\_mention>", "Challenge a user on codeforces"],
        [";challenge ac <user\_mention>", "Challenge a user on atcoder"],
        [";gitlog cf", "Shows your all gitgud problems on codeforces"],
        [";gitlog ac", "Shows your all gitgud problems on atcoder"],
        [";next", "Shows the next 5 contest on codeforces, atcoder and codechef"],
        [";leaderboard cf", "Shows the leaderboard of codeforces gitgudders"],
        [";leaderboard ac", "Shows the leaderboard of atcoder gitgudders"],
        [";leaderboard both", "Shows the leaderboard of both codeforces and atcoder gitgudders"],
        [";stalk <handle>", "Shows the all the last solved problems by the given handle on cf"],
        [";stalk <handle> hardest", "Shows the all the last solved problems by the given handle on cf sorted by difficulty"],
        [";stalk <handle> 1200", "Shows the all the last solved problems by the given handle greater than 1200 on cf"],
        [";ratingchange cf <contest\_id>", "Shows the rating change of all the participants of the given contest id on codeforces"],
        [";ratingchange ac <contest\_id>", "Shows the rating change of all the participants of the given contest id on atcoder"],
        [";graph rvp", "Shows the rating vs problem graph of your codeforces account"],
        [";graph pvt", "Shows the problem vs time graph of the your codeforces account"],
        [";performance <handle>", "Shows the contest wise performance of the given handle on codeforces"],

    ]
    content=''
    for i in content_body:
        content+="__**"+i[0]+"**__"+'\n'+i[1]+'\n\n\n'
    return discord.Embed(
        title="Help",
        description=content,
        color=discord.Color.blue()
    )