import discord
from discord.ext import commands

class ModCog:
    """ModCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='modtest')
    @commands.has_role('Moderator')
    async def only_me(self, ctx):

        await ctx.send(f'Hello Moderator This command can only be used by you!!')

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def banusr(self, ctx, member: discord.Member, reason: str):
        await ctx.message.guild.ban(member)
        await ctx.send("User has been banned. oof.")




# Add moderating cog to main instance.
def setup(bot):
    bot.add_cog(ModCog(bot))
