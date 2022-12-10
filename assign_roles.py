from discord.utils import get
 ############# for setting the role first time use this
async def assign_role(member_id,rating_,_guild):                           
    member_ = _guild.get_member(member_id)
    if(rating_<"1200"):
        role = get(member_.guild.roles, name="Newbie")
        await member_.add_roles(role)
    elif(rating_<"1400"):
        role = get(member_.guild.roles, name="Pupil")
        await member_.add_roles(role)
    elif(rating_<"1600"):
        role = get(member_.guild.roles, name="Specialist")
        await member_.add_roles(role)
    elif(rating_<"1900"):
        role = get(member_.guild.roles, name="Expert")
        await member_.add_roles(role)
    elif(rating_<"2100"):
        role = get(member_.guild.roles, name="Candidate Master")
        await member_.add_roles(role)
    elif(rating_<"2300"):
        role = get(member_.guild.roles, name="Master")
        await member_.add_roles(role)
    elif(rating_<"2400"):
        role = get(member_.guild.roles, name="International Master")
        await member_.add_roles(role)
    elif(rating_<"2600"):
        role = get(member_.guild.roles, name="Grandmaster")
        await member_.add_roles(role)
    elif(rating_<"3000"):
        role = get(member_.guild.roles, name="International Grandmaster")
        await member_.add_roles(role)
    else:
        role = get(member_.guild.roles, name="Legendary Grandmaster")
        await member_.add_roles(role)

#this removes previous roles
async def deassign_role(member_id,_guild):
    member_ = _guild.get_member(member_id)
    role = get(member_.guild.roles, name="Newbie")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="Pupil")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="Specialist")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="Expert")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="Candidate Master")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="Master")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="International Master")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="Grandmaster")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="International Grandmaster")
    await member_.remove_roles(role)
    role = get(member_.guild.roles, name="Legendary Grandmaster")
    await member_.remove_roles(role)

########### for updating roles use this ###########
async def reassign_role(member_id,rating_,_guild):                
    await deassign_role(member_id,_guild)
    await assign_role(member_id,rating_,_guild)
