#!/usr/bin/python3

import discord
from discord.ext import commands
import datetime, re
import json, asyncio
import copy
import logging
import traceback
import aiohttp
import sys
import json
import subprocess

with open("config.json") as dataf:
    returnconfig = json.load(dataf)

def get_prefix(bot, message):

    prefixes = ['<.']

    if not message.guild:
        return '?'
    

    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.simple',
                      'cogs.admin',
                      'cogs.moderating',
                      'cogs.fortnite']

 # lets configure that Bot prefix, if you want to change this, go ahead! Do note that documentations might not work properly if you do.
bot = commands.Bot(command_prefix=get_prefix, description='A cool bot made with <3 by Tristan Farkas')

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f"Kanelbulle couldn't load: {extension}.", file=sys.stderr)
        traceback.print_exc()

@bot.event
async def on_ready():
    print(bot.user.name)
    print('Signed into bot user.')
    statusdiscord = discord.Game("Kanelbulle v.1.1.0")
    await bot.change_presence(status=discord.Status.online, activity=statusdiscord)
    with open("whitelist.json") as whitelistf:
        server_whitelist = json.load(whitelistf)
    for guild in bot.guilds:
        if not guild.id in server_whitelist:
            print(f"Kanelbulle joined a non-whitelisted server, {guild.name}. Kanelbulle is leaving.")
            await guild.leave()

@bot.event
async def on_guild_join(guild):
    with open("whitelist.json") as whitelistf:
        server_whitelist = json.load(whitelistf)
    if not guild.id in server_whitelist:
        print(f"Kanelbulle joined a non-whitelisted server, {guild.name}. Kanelbulle is leaving.")
        await guild.leave()
    else:
        if guild.system_channel:
            try:
                await guild.system_channel.send("Hi! I'm Kanelbulle, thank you for adding me! My prefix is `<.`")
            except discord.Forbidden:
                pass

@bot.event
async def on_message(ctx):
    context = await bot.get_context(ctx)
    if context.valid:
        if isinstance(ctx.channel, discord.TextChannel):
            if not ctx.channel.permissions_for(ctx.channel.guild.me).send_messages:
                try:
                    await ctx.author.send(f"*Houston, we have a problem!*\nYou tried to use `{ctx.content}` in {ctx.channel.mention}, but I don't have message permissions there.\nGive me perms and try again!")
                except discord.Forbidden:
                    pass # DMs disabled!
            else:
                await bot.invoke(context) # Performance improvement

  # All of the following commands are currently MANDATORY, these commands are part of the MAIN system other commands are added using a seperate file.



@bot.command()
async def info(ctx):
    embedinfo = discord.Embed(title="Kanelbulle Info", description="Some very neat info!", color=0xeee657)
    embedinfo.add_field(name="Author", value="@tristanfarkas#0001")
    embedinfo.add_field(name="Github repository", value="https://github.com/trilleplay/kanelbulle/")
    embedinfo.add_field(name="Guild count", value=f"{len(bot.guilds)}")
    embedinfo.add_field(name="Invite", value="Right now Kanelbulle is private due to resource limitations. If you would like to apply/request access, you may do so over at my discord server: https://discord.gg/FBMrcYM in the #invite-kanelbulle channel. ")
    embedinfo.set_image(url="https://trilleplay.github.io/kanelbulle/Kanelbulle%20Full_Logo.png")

    await ctx.send(embed=embedinfo)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Kanelbulle Docs", description="Made with <3 by Tristan Farkas.", color=0xedab49)

    embed.add_field(name="Docs", value="The docs for Kanelbulle commands is available at: https://kanelbulle.gitbook.io/kanelbulle/useful-commands.", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    latency = bot.latency*1000
    embedping = discord.Embed(title="Ping!", description="Ping the bot!", color=0xedab49)

    embedping.add_field(name="🏓 Latency", value=(latency), inline=False)

    await ctx.send(embed=embedping)

bot.run(returnconfig['token'])
