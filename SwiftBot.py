import os
import random
import re
import base64
import aiohttp 
import brawlstars
import asynctest
import signal
import sys
import googlesearch
from googlesearch import search
import datetime
import requests
import random
import traceback
import time


import discord
from discord.ext.commands import cooldown, BucketType
from discord.ext import commands
from discord.utils import get
from discord import Color

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    activity = discord.Game(name="Parancsokért -help/ Swift by 0nyx", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command(
	help="Ugy tunik segitsegre van szukseged",

	brief="Törli az összes üzenetet az adott csatornán."
)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount = 10000):
    embed = discord.Embed(description="Üzenetek törölve:gear:.",color=discord.Color.from_rgb(0, 255, 0))
    await ctx.channel.send(embed=embed)
    await ctx.channel.purge(limit=amount)


@bot.command(
    help=".",

    brief="Visszaküldi azt,amit megadtál neki."
)
async def print(ctx, *args):
	response = ""

	
	for arg in args:
		response = response + "   " + arg

	await ctx.channel.send(response)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
@commands.has_permissions(send_messages=True)
async def smile(ctx):
   embed = discord.Embed(title="`Smile.`", description=f"> :sunglasses:",colour=discord.Colour.dark_orange())
   await ctx.send(embed=embed)

@smile.error
async def smile_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = discord.Embed(description="> Calm down, this command is on a cooldown. Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
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
        msg = discord.Embed(description="> Calm down, this command is on a cooldown. Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
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
    embed = discord.Embed(description="> Sikeresen bannoltad {member}-t:greentick:",colour=discord.Colour.from_rgb(0, 255, 0))
    await ctx.channel.send(embed=embed)
    await ctx.author.send(embed=embed)

class HelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.dark_red(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

bot.help_command = HelpCommand()

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
    embed = discord.Embed(description=f"{member.mention}**némitva**", colour=discord.Colour.from_rgb(0, 255, 0))
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" lenémitott: {guild.name} reason: {reason}")

@bot.command(
	help="Ugy tunik segitsegre van szukseged.",

	brief="Unmute-olja az adott embert,ha megfelelő személy használja."
)
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f"Némitást feloldotta: - {ctx.guild.name}")
   embed = discord.Embed(description=f"> Némitás feloldva,** {member.mention}",colour=discord.Colour.from_rgb(0, 255, 0))
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
	help="Ugy tunik segitsegre van szukseged.",

	brief="Figyelmezteti az adott embert.")
@commands.has_permissions(administrator=True)
async def warn(ctx, member : discord.Member, *, reason = None):
   embed = discord.Embed(description=f"{member.mention} `figyelmeztetve lett.`:gear:",colour=discord.Colour.from_rgb(0, 255, 0))
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
        msg = discord.Embed(description="> Calm down, this command is on a cooldown. Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
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
        msg = discord.Embed(description="> Calm down, this command is on a cooldown. Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
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
        msg = discord.Embed(description="> Calm down, this command is on a cooldown. Try again in: {:.2f}s".format(error.retry_after),colour=discord.Colour.from_rgb(255, 0, 0))
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

bot.run('ODA2OTQ0MzQyNjUxNjk5Mjgy.YBwzew.6Nmx3CchjMsIPLxPcrmhkhfqevA')