from discord.utils import get
import os

#Whenever this function is called it will remove all the rating roles for the given username
async def remove_rating_roles(username):
    rating_roles = ["Newbie", "Pupil", "Specialist", "Expert", "Candidate Master", "Master", "Internation Master", "Grandmaster", "International Grandmaster", "Legendary Grandmaster"]
    for role in rating_roles:
        for user_role in username.roles:
            if role == user_role.name:
                await username.remove_roles(user_role)
    print("All roles removed")

#This function will add the rating role to the user based on the rating
async def rating_role(id, rating,bot,channel):
    #Fetch the guild from the environment variable
    GUILD=os.environ.get('GUILD') 
    guild = await bot.fetch_guild(GUILD)
    #Get the user from the id and guild then fetch the username
    user = await guild.query_members(user_ids=[id])
    username=user[0]
    msg = await channel.send(f"Fetching rating changes")
    #Now based on the rating add the role to the user
    if (rating < 800):
        await remove_rating_roles(username)
        return
    elif (rating < 1200):
        role = get(username.guild.roles, name="Newbie")
        await remove_rating_roles(username)
        await username.add_roles(role)
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        print("Role added")
        return
    elif (rating < 1400):
        role = get(username.guild.roles, name="Pupil")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return
    elif (rating < 1600):
        role = get(username.guild.roles, name="Specialist")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return
    elif (rating < 1900):
        role = get(username.guild.roles, name="Expert")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return
    elif (rating < 2100):
        role = get(username.guild.roles, name="Candidate Master")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return
    elif (rating < 2300):
        role = get(username.guild.roles, name="Master")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return
    elif (rating < 2400):
        role = get(username.guild.roles, name="International Master")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return
    elif (rating < 2600):
        role = get(username.guild.roles, name="Grandmaster")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return
    elif (rating < 3000):
        role = get(username.guild.roles, name="International Grandmaster")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return
    else:
        role = get(username.guild.roles, name="Legendary Grandmaster")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        await msg.edit(content=f"{username.mention} is a <@&{role.id}>")
        return