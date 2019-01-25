import discord
from discord.ext import commands
import random


class RandomCog:
    """RandomCog"""


    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='coinflip')
    async def fstats(self, ctx):
        side = random.randint(1,2)
        if side == 1:
            await ctx.send("heads")
        else:
            await ctx.send("tails")

    @commands.command(name='randomnum')
    async def fstats(self, ctx, val1: int, val2: int):
        try:
            randomval = random.randint(val1,val2)
            await ctx.send(randomval)
        except:
            raise commands.BadArgument(message=f"Value(s) specified are invalid.")

# Add random cog to main instance.
def setup(bot):
    bot.add_cog(RandomCog(bot))
