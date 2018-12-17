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
import sentry_sdk
import json
import subprocess
import requests
import sys

with open("config.json") as dataf:
    returnconfig = json.load(dataf)

sentry_sdk.init(returnconfig['sentry_dsn'])

def get_prefix(bot, message):

    prefixes = ['<.']

    if not message.guild:
        return '?'


    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.simple',
                      'cogs.admin',
                      'cogs.moderating',
                      'cogs.fortnite']

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
    print('Signed into bot user.')
    statusdiscord = discord.Game("Kanelbulle v.1.1.0")
    await bot.change_presence(status=discord.Status.online, activity=statusdiscord)
    global log_channel
    log_channel = bot.get_channel(returnconfig["log_channel"])
    setattr(bot, "log_channel", log_channel)
    with open("whitelist.json") as whitelistf:
        server_whitelist = json.load(whitelistf)
    for guild in bot.guilds:
        if not guild.id in server_whitelist:
            print(f"Kanelbulle joined a non-whitelisted server, {guild.name} ({guild.id}). Kanelbulle is leaving.")
            await log_channel.send(f"Kanelbulle joined a non-whitelisted server, {guild.name} ({guild.id}). Kanelbulle is leaving.")
            await guild.leave()

@bot.event
async def on_guild_join(guild):
    with open("whitelist.json") as whitelistf:
        server_whitelist = json.load(whitelistf)
    if not guild.id in server_whitelist:
        print(f"Kanelbulle joined a non-whitelisted server, {guild.name} ({guild.id}). Kanelbulle is leaving.")
        await log_channel.send(f"Kanelbulle joined a non-whitelisted server, {guild.name} ({guild.id}). Kanelbulle is leaving.")
        await guild.leave()
    else:
        if guild.system_channel:
            try:
                await guild.system_channel.send("Hi! I'm Kanelbulle, thank you for adding me! My prefix is `<.`")
            except discord.Forbidden:
                pass


class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = returnconfig['dbltoken']
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            logger.info('Sending server count of to DBL Weeeeee!')
            try:
                await self.dblpy.post_server_count()
                logger.info('posted server count ({})'.format(len(self.bot.guilds)))
            except Exception as e:
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

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
                try:
                    await ctx.author.send(f"*Houston, we have a problem!*\nYou tried to use `{ctx.content}` in {ctx.channel.mention}, but I don't have message permissions there.\nGive me perms and try again!")
                except discord.Forbidden:
                    pass # DMs disabled!
            else:
                await bot.invoke(context) # Performance improvement

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command can not be used through DMs!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f"Welp, this is awkward.\nI do not have enough permissions to run {ctx.command}!```error```")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("This command is currently disabled and can not be used.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(":lock: You don't have enough permissions to run this command!")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Woah there, you're too *hyped!*\nYou're on a cooldown.```{error}```")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You are missing required arguments!\n{error}`\n\nCommand usage: `<.{ctx.command.signature}`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"One of your arguments is incorrect!\n`{error}`\n\nCommand usage: <.{ctx.command.signature}`")
    elif isinstance(error, commands.CommandNotFound):
        return

    else:
        await ctx.send(":rotating_light: Uh-Oh! An error just ocurred! The devs are already on it. Sorry my fren! :rotating_light:")
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
