#!/usr/bin/python3

import discord
from discord.ext import commands
import datetime, re
from datadog import initialize
from datadog import api
from datadog import statsd
import json, asyncio
import copy
import logging
import traceback
import aiohttp
import sys
import json
import subprocess
import requests
from utilities import translate, returncfg
import sys

with open("config.json") as dataf:
    returnconfig = json.load(dataf)

options = {
    'api_key':returnconfig['datadog_api_key'],
    'app_key':returnconfig['datadog_app_key']
}

initialize(**options)

global aiohttpsession
aiohttpsession = aiohttp.ClientSession()

def get_prefix(bot, message):

    prefixes = ['<.']

    if not message.guild:
        return '?'


    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.core',
                      'cogs.admin',
                      'cogs.moderating',
                      'cogs.fortnite',
                      'cogs.random',
                      'cogs.apex']

log_channel = None

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
    print('READY event received.')
    title = "READY event received - Kanelbulle"
    text = 'The bot received a READY event from Discords API.'
    tags = ['version:1', 'application:bot']
    api.Event.create(title=title, text=text, tags=tags)
    statusdiscord = discord.Game("Kanelbulle v.1.1.0")
    await bot.change_presence(status=discord.Status.online, activity=statusdiscord)
    url = "https://discord.bots.gg/api/v1/bots/" + returnconfig['bot_id'] + "/stats"
    headers = {"Authorization": returnconfig['discord_bots_token']}
    payload = {'guildCount': (len(bot.guilds))}
    await aiohttpsession.post(url, data=payload, headers=headers)
    global log_channel
    log_channel = bot.get_channel(returnconfig["log_channel"])
    setattr(bot, "log_channel", log_channel)

@bot.event
async def on_guild_join(guild):
    url = "https://discord.bots.gg/api/v1/bots/" + returnconfig['bot_id'] + "/stats"
    headers = {"Authorization": returnconfig['discord_bots_token']}
    payload = {'guildCount': (len(bot.guilds))}
    await aiohttpsession.post(url, data=payload, headers=headers)
    title = f"New guild added: {guild.name}"
    text = f"Guild ID: {guild.id}, Guild Region: {guild.region}, Member Count: {guild.member_count} and the server owners ID: {guild.owner_id}"
    tags = ['version:1', 'application:bot']
    serverjoinembed = discord.Embed(title="A new server has added Kanelbulle!", description="YAAAAAAAAAAY!", color=0xedab49)
    serverjoinembed.add_field(name="Server name", value=(guild.name), inline=False)
    serverjoinembed.add_field(name="Server region", value=(guild.region), inline=False)
    serverjoinembed.add_field(name="Server ID", value=(guild.id), inline=False)
    serverjoinembed.add_field(name="Servers member count", value=(guild.member_count), inline=False)
    serverjoinembed.add_field(name="Server owners ID", value=(guild.owner_id), inline=False)
    await log_channel.send(embed=serverjoinembed)
    if guild.system_channel:
        try:
            await guild.system_channel.send("Hi! I'm Kanelbulle, thank you for adding me! My prefix is `<.`")
        except discord.Forbidden:
            pass

@bot.event
async def on_guild_remove(guild):
    url = "https://discord.bots.gg/api/v1/bots/" + returnconfig['bot_id'] + "/stats"
    headers = {"Authorization": returnconfig['discord_bots_token']}
    payload = {'guildCount': (len(bot.guilds))}
    await aiohttpsession.post(url, data=payload, headers=headers)

@bot.event
async def on_message(ctx):
    if ctx.author.bot:
        if ctx.channel.id == returnconfig["webhook_channel"]  and ctx.author.id == returnconfig["webhook_id"]:
            ctx = await bot.get_context(ctx)
            loaded = json.loads(ctx.message.clean_content.replace("\\", ""))
            result = requests.get(f"https://api.giphy.com/v1/gifs/random?api_key={returnconfig['giphy_token']}&tag=cat,%20cute,%20kitten&rating=G").json()
            if loaded["isWeekend"]:
                try:
                    usr = await commands.UserConverter().convert(argument = loaded["user"], ctx = ctx)
                    await usr.send("***:heart: Thank you! :heart:***\n\nThanks for *voting me on DiscordBots*.\nThe Kanelbulle Team has put great effort into making Kanelbulle, and we appreciate a lot you appreciate our work!\nPlus, you voted on a weekend, meaning your vote counted x2. Awesome!\n\nAs a thank you, here's a cute cat gif we hope you enjoy. If you want more, you can just vote us again in 12 hours!  \n\nhttps://kanelbulle.herokuapp.com/serve/Poweredby_100px-White_VertLogo.png\n"+result["data"]["images"]["original"]["url"])
                except discord.Forbidden:
                    pass
            else:
                try:
                    usr = await commands.UserConverter().convert(argument = loaded["user"], ctx = ctx)
                    await usr.send("***:heart: Thank you! :heart:***\n\nThanks for *voting me on DiscordBots*.\nThe Kanelbulle Team has put great effort into making Kanelbulle, and we appreciate a lot you appreciate our work!\n\nAs a thank you, here's a cute cat gif we hope you enjoy. If you want more, you can just vote us again in 12 hours! \n\nhttps://kanelbulle.herokuapp.com/serve/Poweredby_100px-White_VertLogo.png\n"+result["data"]["images"]["original"]["url"])
                except discord.Forbidden:
                    pass
        return False
    context = await bot.get_context(ctx)
    if context.valid:
        if isinstance(ctx.channel, discord.TextChannel):
            if not ctx.channel.permissions_for(ctx.channel.guild.me).send_messages:
                pass
            else:
                await bot.invoke(context) # Performance improvement

@bot.event
async def on_command_error(ctx: commands.Context, error):
    guildlang = "en"
    guildsettings = await returncfg.fetchguildconfig(ctx.guild.id)
    try:
        guildlang = guildsettings["lang"]
    except:
        pass
    if isinstance(error, commands.NoPrivateMessage):
        error_string = translate.translate(lang=guildlang, string="fail_noprivatemessage")
        await ctx.send(error_string)
        statsd.increment('bot.errorNoPrivateMessage')
    elif isinstance(error, commands.BotMissingPermissions):
        error_string = translate.translate(lang=guildlang, string="fail_MissingPermissions", ctx=ctx)
        await ctx.send(f"Welp, this is awkward.\nI do not have enough permissions to run {ctx.command}!```error```")
        statsd.increment('bot.errorBotMissingPermissions')
    elif isinstance(error, commands.DisabledCommand):
        error_string = translate.translate(lang=guildlang, string="fail_DisabledCommand")
        await ctx.send(error_string)
        statsd.increment('bot.errorDisabledCommand')
    elif isinstance(error, commands.CheckFailure):
        error_string = translate.translate(lang=guildlang, string="fail_CheckFailure")
        await ctx.send(error_string)
        statsd.increment('bot.errorCheckFailure')
    elif isinstance(error, commands.CommandOnCooldown):
        error_string = translate.translate(lang=guildlang, string="fail_CommandOnCooldown", error=error)
        await ctx.send(error_string)
        statsd.increment('bot.errorCommandOnCooldown')
    elif isinstance(error, commands.MissingRequiredArgument):
        error_string = translate.translate(lang=guildlang, string="fail_MissingRequiredArgument", error=error, ctx=ctx)
        await ctx.send(error_string)
        statsd.increment('bot.errorCommandOnCooldown')
    elif isinstance(error, commands.BadArgument):
        error_string = translate.translate(lang=guildlang, string="fail_BadArgument", error=error, ctx=ctx)
        await ctx.send(error_string)
        statsd.increment('bot.errorBadArgument')
    elif isinstance(error, commands.CommandNotFound):
        return

    else:
        await ctx.send(f":rotating_light: Uh-Oh! An error just ocurred! The devs are already on it. Sorry my fren! :rotating_light:")
        if isinstance(ctx.channel, discord.DMChannel):
            used_in = f"DM {ctx.channel.id}"
        else:
            used_in = f"{ctx.channel.name}({ctx.channel.id}), guild {ctx.guild.name}({ctx.guild.id})"
        traceback_embed = discord.Embed(title = "Traceback", description = "```"+"".join(traceback.format_tb(error.__traceback__))+"```", timestamp = ctx.message.created_at)
        await log_channel.send(f"""
***ERROR ALERT, <@&{returnconfig['dev_role']}>s!***

An error ocurred during the execution of a command:
`{error}`

Command: `{ctx.invoked_with}`
Command arguments: `{ctx.args} - {ctx.kwargs}` (Could be wrong, please refer to `Message contents`)
Command used by: {ctx.author.mention} `{ctx.author.name}#{ctx.author.discriminator} {ctx.author.id}`
Command used in: `{used_in}`
Message id: `{ctx.message.id}`
Message link: {ctx.message.jump_url}
Message timestamp (UTC): `{ctx.message.created_at}`
Message contents: `{ctx.message.content}`""", embed = traceback_embed)
        print("".join(traceback.format_tb(error.__traceback__)))

@bot.event
async def on_error(event, args, kwargs):
    t, error, info = sys.exc_info()
    traceback_embed = discord.Embed(title = "Traceback", description = "```"+"".join(traceback.format_tb(error.__traceback__))+"```", timestamp = datetime.datetime.utcnow())
    await log_channel.send(f"""
***ERROR ALERT, <@&{returnconfig['dev_role']}>s!***

An error ocurred during the execution of an event:
`{error}`

Event: `{event}`
Event arguments: `{args} - {kwargs}`
Event timestamp (UTC): `{datetime.datetime.utcnow()}`""", embed = traceback_embed)
    print("".join(traceback.format_tb(error.__traceback__)))

  # All of the following commands are currently MANDATORY, these commands are part of the MAIN system other commands are added using a seperate file.

@bot.event
async def on_socket_response(resp):
    # READY or RESUMED?
    if resp.get("t") == "READY":
        data = resp.get("d")
        ws_url = data["_trace"][0]
        sessions = data["_trace"][1]
        url = returnconfig["webhook_url"]
        payload = {'content': "Bot resumed connection with gateway **{}** (utilising session server **{}**).".format(ws_url, sessions)}
        await aiohttpsession.post(url, data=payload)
    elif resp.get("t") == "RESUMED":
        data = resp.get("d")
        ws_url = data["_trace"][0]
        sessions = data["_trace"][1]
        # Post to log
        url = returnconfig["webhook_url"]
        payload = {'content': "Bot resumed connection with gateway **{}** (utilising session server **{}**).".format(ws_url, sessions)}
        await aiohttpsession.post(url, data=payload)

@bot.command()
async def info(ctx):
    guildlang = "en"
    guildsettings = await returncfg.fetchguildconfig(ctx.guild.id)
    try:
        guildlang = guildsettings["lang"]
    except:
        pass
    embedinfo = discord.Embed(title="Kanelbulle Info", description="Some very neat info!", color=0xeee657)
    author_string = translate.translate(lang=guildlang, string="author")
    embedinfo.add_field(name=author_string, value="@tristanfarkas#0001")
    repo_string = translate.translate(lang=guildlang, string="repo")
    embedinfo.add_field(name=repo_string, value="https://github.com/trilleplay/kanelbulle/")
    guildcount_string = translate.translate(lang=guildlang, string="guild_count")
    embedinfo.add_field(name=guildcount_string, value=f"{len(bot.guilds)}")
    invite_string = translate.translate(lang=guildlang, string="invite")
    embedinfo.add_field(name=invite_string, value="Right now Kanelbulle is private due to resource limitations. If you would like to apply/request access, you may do so over at my discord server: https://discord.gg/FBMrcYM in the #invite-kanelbulle channel. ")
    embedinfo.set_image(url="https://trilleplay.github.io/kanelbulle/Kanelbulle%20Full_Logo.png")

    await ctx.send(embed=embedinfo)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    guildlang = "en"
    guildsettings = await returncfg.fetchguildconfig(ctx.guild.id)
    try:
        guildlang = guildsettings["lang"]
    except:
        pass
    madewith_string = translate.translate(lang=guildlang, string="helpc_headerdesc")
    embed = discord.Embed(title="Kanelbulle Docs", description=madewith_string, color=0xedab49)

    embed.add_field(name="Docs", value="The docs for Kanelbulle commands is available at: https://docs.kanelbulle.farkasdev.com/commands", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    guildlang = "en"
    guildsettings = await returncfg.fetchguildconfig(ctx.guild.id)
    try:
        guildlang = guildsettings["lang"]
    except:
        pass
    ping_description = translate.translate(lang=guildlang, string="ping_desc")
    latency = bot.latency*1000
    embedping = discord.Embed(title="Ping!", description=ping_description, color=0xedab49)

    embedping.add_field(name="🏓 Latency", value=(latency), inline=False)

    await ctx.send(embed=embedping)

bot.run(returnconfig['token'])
