import os
import json
import random
import re
import asynctest
import signal
import sys
import datetime
import requests
import random
import traceback
import time


import discord
from pretty_help import DefaultMenu, PrettyHelp
from discord.ext.commands import cooldown, BucketType
from discord.ext import commands
from discord.utils import get
from discord import Color
try:
     from googlesearch import search 
except ImportError:
     print("No module found!")
     
     
TOKEN = "ODA2OTQ0MzQyNjUxNjk5Mjgy.YBwzew.Z2iOI0aYPcBpjqTKpLFH9fIHRmg"

bot = commands.Bot(command_prefix='-')
bot.help_command = PrettyHelp()

@bot.event
async def on_ready():
    activity = discord.Game(name="Parancsokért -help/ Swift by 0nyx", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"{bot.user.name} has been logged in.")
    print(".")
    time.sleep(2)
    print(".")
    time.sleep(2)
    print(".")
    time.sleep(1)
    print("Cogs are ready.")
    print(".")
    time.sleep(2)
    print(".")
    time.sleep(2)
    print(".")
    time.sleep(1)
    print("The bot now is ready to use!")
    time.sleep(2)
    print(".")
    time.sleep(3)
    print("All command loaded...")
    time.sleep(1)


@bot.command(
	help="Ugy tunik segitsegre van szukseged",

	brief="Törli az összes üzenetet az adott csatornán."
)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount = 10000):
    embed = discord.Embed(description="Üzenetek törölve:gear:.",color=discord.Color.from_rgb(0, 255, 0))
    await ctx.channel.send(embed=embed)
    await ctx.channel.purge(limit=amount)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
@commands.has_permissions(send_messages=True)
async def smile(ctx):
   embed = discord.Embed(title="`Smile.`", description=f"> :sunglasses:",colour=discord.Colour.dark_orange())
   await ctx.send(embed=embed)

@smile.error
async def smile_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = discord.Embed(title="Calm down, this command is on a cooldown.", description="> Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=msg)
    else:
        raise error

@bot.command(
	help="Ugy tunik segitsegre van szukseged.",

	brief="Elküldi a Bot jelenlegi verzióját.")
@commands.has_permissions(send_messages=True)
@commands.cooldown(1, 60, commands.BucketType.user)
async def ver(ctx):
   embed = discord.Embed(description="> `5.0` :gear:",colour=discord.Colour.from_rgb(0, 255, 0))
   await ctx.channel.send(embed=embed)

@ver.error
async def ver_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = discord.Embed(title="Calm down, this command is on a cooldown.", description="> Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=msg)
    else:
        raise error


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description="Valami hiányzik, próbáld meg újra!",colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="`Nincsenek meg a szükséges engedélyeid` :angry:",colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=embed)

@bot.command(
	help="Ugy tunik segitsegre van szukseged.",

	brief="Ha jó személy használja,akkor bannolja az adott embert."
)

@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    embed = discord.Embed(description=f"> {member} bannolva {author.mention} által.",colour=discord.Colour.from_rgb(0, 255, 0))
    await ctx.channel.send(embed=embed)
    await ctx.author.send(embed=embed)

@bot.command(
	help="Ugy tunik segitsegre van szukseged.",

	brief="Unbannolja az adott embert,ha jó személy használja."
)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member :  discord.Member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'UNBANNED {user.mention}')
            return

@bot.command(
	help="Ugy tunik segitsegre van szukseged",

	brief="Lenémitja az adott embert,ha megfelelő ember használja."
)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False, read_messages=False)
    embed = discord.Embed(description=f"`{member} némitva lett {ctx.author} által`", colour=discord.Colour.from_rgb(0, 255, 0))
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" lenémitott: `{ctx.author}` indok: `{reason}`")

@bot.command(
	help="Ugy tunik segitsegre van szukseged.",

	brief="Unmute-olja az adott embert,ha megfelelő személy használja."
)
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   embed = discord.Embed(description=f"`{member}` némitása fel lett oldva `{ctx.author}` által:white_check_mark:",colour=discord.Colour.from_rgb(0, 255, 0))
   await ctx.send(embed=embed)


@bot.command(
	help="Ugy tunik segitsegre van szukseged.",

	brief="Ha jó személy használja,akkor kickeli az adott embert."
)

@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    embed = discord.Embed(description=f"> Sikeresen kidobtad {member}-t",colour=discord.Colour.from_rgb(0, 255, 0))
    await member.kick(reason = reason)
    await ctx.channel.send(embed=embed)

@bot.command(
    help="> Küld egy privát üzenetet.",

    brief="> Ugy tunik segitsegre van szukseged."
)
@commands.cooldown(1, 360, commands.BucketType.user)
async def pü(ctx):
    embed = discord.Embed(description="`Privát üzenet elküldve.` :gear:", colour=discord.Colour.from_rgb(0, 255, 0))
    embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)
    await ctx.author.send("Itt a **PÜ-d**:eyes:")

@pü.error
async def pü_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = discord.Embed(title="Calm down, this command is on a cooldown.", description="> Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=msg)
    else:
        raise error

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def delrole(ctx, role: discord.Role):
    await bot.delete_role(role)
    await bot.say("A {} jelvény sikeresen törölve lett!".format(role.name))




@bot.command()
@commands.cooldown(1, 3000, commands.BucketType.user)
async def addtext(ctx, channelName, roleName):
    guild = ctx.guild
    member = ctx.author
    role = await guild.create_role(name=roleName)
    admin_role = get(guild.roles, name=roleName)

    embed = discord.Embed(title="`Szöveges Csatorna létrehozva!`", description="> What we think, we become.", colour=discord.Colour.from_rgb(0, 255, 0))
    embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(name=channelName, overwrites=overwrites)
    await ctx.send(embed=embed)

@addtext.error
async def addtext_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = discord.Embed(title="Calm down, this command is on a cooldown.", description="> Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=msg)
    else:
        raise error
            

@bot.command()
@commands.has_role("Tulajdonos")
async def takerole(ctx, member:discord.Member = None, *, role:discord.Role = None):
    embed = discord.Embed(description=f"> A(z) {role.mention} rang el lett távolitva tőle: {member}", colour=discord.Colour.from_rgb(255, 0, 0))
    embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    await member.remove_roles(role)

@bot.command()
@commands.cooldown(1, 3000, commands.BucketType.user)
async def addvoice(ctx, channelName, roleName):
    guild = ctx.guild
    member = ctx.author
    role = await guild.create_role(name=roleName)
    admin_role = get(guild.roles, name=roleName)

    embed = discord.Embed(title="`Hang Csatorna létrehozva!`", description="> What we think, we become.", colour=discord.Colour.from_rgb(0, 255, 0))
    embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_voice_channel(name=channelName, overwrites=overwrites)
    await ctx.send(embed=embed)
@addvoice.error
async def addvoice_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = discord.Embed(title="Calm down, this command is on a cooldown.", description="> Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=msg)
    else:
        raise error

@bot.command()
@commands.has_role("Tulajdonos")
async def addrole(ctx, member:discord.Member = None, *, role:discord.Role = None):
    embed = discord.Embed(description=f"> {member} kapott egy {role.mention} rangot!", colour=discord.Colour.from_rgb(0, 255, 0))
    embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    await member.add_roles(role)
    
@bot.command()
async def pinglatency(ctx):
    await ctx.send(f"Latency ping: {bot.latency}")  
    
@bot.command()
async def pingms(ctx):
    before = time.monotonic()
    message = await ctx.send("1,000,000ms")
    ping = (time.monotonic() - before) * 1000
    time.sleep(2)
    await message.edit(content=f"JK, `{int(ping)}ms`")
    
@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)
        
data = {"foo": "bar"}

with open("ecoBal.json", "w+") as fp:
    json.dump(data, fp, sort_keys=True, indent=4)    
with open("ecoBal.json", "r") as fp:
    data = json.load(fp) # loading json contents into data variable - this will be a dict

data["foo"] = "baz" # updating values
data["bar"] = "foo" # writing new values

with open("ecoBal.json", "w+") as fp:
    json.dump(data, fp, sort_keys=True, indent=4)

def add_score(member: discord.Member, amount: int):
    if os.path.isfile("ecoBal.json"):
        with open("ecoBal.json", "r") as fp:
            data = json.load(fp)
        try:
            data[f"{member.id}"]["score"] += amount
        except KeyError: # if the user isn't in the file, do the following
            data[f"{member.id}"] = {"score": amount} # add other things you want to store
    else:
        data = {f"{member.id}": {"score": amount}}
    # saving the file outside of the if statements saves us having to write it twice
    with open("ecoBal.json", "w+") as fp:
        json.dump(data, fp, sort_keys=True, indent=4) # kwargs for beautification
   # you can also return the new/updated score here if you want
        

def get_score(member: discord.Member):
    with open("ecoBal.json", "r") as fp:
        data = json.load(fp)
    return data[f"{member.id}"]["score"]


#work commands
@bot.command()
async def work_hotel(ctx):
    add_score(ctx.author, 3000)
    await ctx.send(f"Ma a Hotelben dolgoztál és kaptál `3000`Ft-ot. A jelenlegi egyenleged `{get_score(ctx.author)}`Ft.")

@bot.command()
async def work_friend(ctx):
    add_score(ctx.author, 2500)
    await ctx.send(f"Ma a barátodnál dolgoztál, igy kaptál `2500`Ft-ot. A jelenlegi egyenleged `{get_score(ctx.author)}`Ft.")

@bot.command()
async def work_boss(ctx):
    add_score(ctx.author, 10000)
    await ctx.send(f"Ma a munkahelyeden a főködtől kaptál `10.000`Ft-ot. A jelenlegi egyenleged `{get_score(ctx.author)}`Ft.")

#economy balance checker(author's wallet)
@bot.command()
async def egyenleg(ctx):
    get_score((ctx.author))
    await ctx.send(f"A jelenlegi egyenleged `{get_score(ctx.author)}`Ft.")
#economy balance checker(another member)   
@bot.command()
async def masegyenleg(ctx, member : discord.Member = None):
    get_score((member))
    await ctx.send(f"{member} jelenlegi egyenlege `{get_score(member)}`Ft.")
#daily money bonus
@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    add_score(ctx.author, 1200)
    await ctx.send(f"Kaptál `1200`Ft-ot a napi bónuszból, a jelenlegi egyenleged `{get_score(ctx.author)}`Ft")
#daily cooldown error
@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = discord.Embed(title="Calm down, this command is on a cooldown.", description="> Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=msg)
    else:
        raise error

#level system
@bot.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await bot.process_commands(message)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'GG!{user.mention} Elérte a(z)**{lvl_end}**.szintet')
        users[f'{user.id}']['level'] = lvl_end

def get_experience(member: discord.Member):
    with open("users.json", "r") as fc:
        data = json.load(fc)
    return data[f"{member.id}"]["experience"]
#how many xp i have?(done)
@bot.command()
async def xp(ctx, member : discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as fc:
            users = json.load(fc)
            exp = users[str(id)]['experience']
            await ctx.send(f"Ennyi XP-d van: **{exp}XP**")  
    else:
        id = member.id
        with open('users.json', 'r') as fc:
            users = json.load(fc)
            exp = users[str(id)]['experience']
            await ctx.send(f"{member} ennyi XP-t birtokol: **{exp}XP**")     
#level checker command
@bot.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'Ezen a szinten vagy: **{lvl}**')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} Ezen a szinten van: **{lvl}**')
        
@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)
        
data = {"foo": "bar"}

with open("warns.json", "w+") as fp:
    json.dump(data, fp, sort_keys=True, indent=4)    
with open("warns.json", "r") as fp:
    data = json.load(fp) # loading json contents into data variable - this will be a dict

data["foo"] = "baz" # updating values
data["bar"] = "foo" # writing new values

with open("ecoBal.json", "w+") as fp:
    json.dump(data, fp, sort_keys=True, indent=4)

def add_warns(member: discord.Member, amount: int):
    if os.path.isfile("warns.json"):
        with open("warns.json", "r") as fp:
            data = json.load(fp)
        try:
            data[f"{member.id}"]["warns"] += amount
        except KeyError: # if the user isn't in the file, do the following
            data[f"{member.id}"] = {"warns": amount} # add other things you want to store
    else:
        data = {f"{member.id}": {"warns": amount}}
    # saving the file outside of the if statements saves us having to write it twice
    with open("warns.json", "w+") as fp:
        json.dump(data, fp, sort_keys=True, indent=4) # kwargs for beautification
   # you can also return the new/updated score here if you want
        

def get_warns(member: discord.Member):
    with open("warns.json", "r") as fp:
        data = json.load(fp)
    return data[f"{member.id}"]["warns"]

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member : discord.Member, *, reason = None):
    add_warns(member, 1)
    await ctx.send(f"{member} figyelmeztetve lett {ctx.author} által. {member} ennyi figyelmeztetést kapott összesen: **{get_warns(member)}**")
        
@bot.command()
async def hwarns(ctx, member : discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('warns.json', 'r') as fc:
            users = json.load(fc)
            wn = users[str(id)]['warns']
            await ctx.send(f"Ennyiszer figyelmeztettek: **{wn}**x")  
    else:
        id = member.id
        with open('warns.json', 'r') as fc:
            users = json.load(fc)
            wn = users[str(id)]['warns']
            await ctx.send(f"{member} Ennyiszer lett figyelmeztetve: **{wn}**x")

    

bot.run(TOKEN)