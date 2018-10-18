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
import os


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

# Load in those cogs.
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Kanelbulle couldn not load: {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print(bot.user.name)
    print('Signed into bot user.')
    statusdiscord = discord.Game("Kanelbulle Testing")
    await bot.change_presence(status=discord.Status.online, activity=statusdiscord)

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
                await bot.process_commands(ctx)

  # All of the following commands are currently MANDATORY, these commands are part of the MAIN system other commands are added using a seperate file.



bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Kanelbulle Test", description="Made with testing by Tristan Farkas.", color=0xedab49)

    embed.add_field(name="test", value="This is a **awesome** test!", inline=False)

    await ctx.send(embed=embed)

citoken = os.environ['discordbottoken']
bot.run(citoken)
