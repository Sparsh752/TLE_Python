from discord.utils import get

async def remove_rating_roles(username):
    rating_roles = ["Newbie", "Pupil", "Specialist", "Expert", "Candidate_Master", "Master", "Internation_Master", "Grandmaster", "International_Grandmaster", "Legendary_Grandmaster"]
    for role in rating_roles:
        for user_role in username.roles:
            if role == user_role.name:
                await username.remove_roles(user_role)
    print("All roles removed")

async def rating_role(id, rating,bot):
    guild = await bot.fetch_guild(1048212913539784805)
    user = await guild.query_members(user_ids=[id])
    username=user[0]
    if (rating < 800):
        await remove_rating_roles(username)
        return
    elif (rating < 1200):
        role = get(username.guild.roles, name="Newbie")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    elif (rating < 1400):
        role = get(username.guild.roles, name="Pupil")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    elif (rating < 1600):
        role = get(username.guild.roles, name="Specialist")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    elif (rating < 1900):
        role = get(username.guild.roles, name="Expert")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    elif (rating < 2100):
        role = get(username.guild.roles, name="Candidate_Master")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    elif (rating < 2300):
        role = get(username.guild.roles, name="Master")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    elif (rating < 2400):
        role = get(username.guild.roles, name="International_Master")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    elif (rating < 2600):
        role = get(username.guild.roles, name="Grandmaster")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    elif (rating < 3000):
        role = get(username.guild.roles, name="International_Grandmaster")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return
    else:
        role = get(username.guild.roles, name="Legendary_Grandmaster")
        await remove_rating_roles(username)
        await username.add_roles(role)
        print("Role added")
        return