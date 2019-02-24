import discord
from discord.ext import commands
import random
import yaml

class RandomCog(commands.Cog):
    """RandomCog"""


    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='coinflip')
    async def coinflip(self, ctx):
        try:
            with open(f"configs/{ctx.guild.id}.yml") as gconfig:
                guildsettings = yaml.safe_load(gconfig)
        except:
            await ctx.send("Uh oh, something probably went **entirely wrong** but it seems like your server is lacking a configuration, type ``<.setup`` to create a default config.")
            return
        if guildsettings["commands"]["random"]["enabled"] == True:
            side = random.randint(1,2)
            if side == 1:
                await ctx.send("heads")
            else:
                await ctx.send("tails")
        else:
            await ctx.send("That command is not enabled for this server! (If you are the server owner you can change enabled/disabled commands by contacting a global admin.")


    @commands.command(name='randomnum')
    async def randomnum(self, ctx, val1: int, val2: int):
        try:
            with open(f"configs/{ctx.guild.id}.yml") as gconfig:
                guildsettings = yaml.safe_load(gconfig)
        except:
            await ctx.send("Uh oh, something probably went **entirely wrong** but it seems like your server is lacking a configuration, type ``<.setup`` to create a default config.")
            return
        if guildsettings["commands"]["random"]["enabled"] == True:
            try:
                randomval = random.randint(val1,val2)
                await ctx.send(randomval)
            except:
                raise commands.BadArgument(message=f"Value(s) specified are invalid.")
        else:
            await ctx.send("That command is not enabled for this server! (If you are the server owner you can change enabled/disabled commands by contacting a global admin.")


# Add random cog to main instance.
def setup(bot):
    bot.add_cog(RandomCog(bot))
