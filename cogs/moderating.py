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
    async def banusr(self, ctx, member, reason: str = "No reason provided"):
        try:
            toban = await commands.MemberConverter().convert(ctx, argument=member)
        except:
            try:
                toban = await commands.UserConverter().convert(ctx, argument=member)
            except:
                raise commands.BadArgument(message=ctx)
        await ctx.message.guild.ban(toban, delete_message_days = 7, reason = f"{ctx.author} - {reason}")
        await ctx.send(f":eyes: {str(toban)} has been banned. oof.")

    @commands.has_permissions(ban_members=True)
    @commands.command(name='unban')
    async def unbanusr(self, ctx, member, reason: str = "No reason provided"):
        try:
            tounban = await commands.MemberConverter().convert(ctx, argument=member)
        except:
            try:
                tounban = await commands.UserConverter().convert(ctx, argument=member)
            except:
                raise commands.BadArgument(message=ctx)
        await ctx.message.guild.unban(tounban, reason = f"{ctx.author} (Unban) - {reason}")
        await ctx.send(f":eyes: {str(toban)} has been unbanned. ")
        
    @commands.has_permissions(ban_members=True)
    @commands.command(name='softban')
    async def softbanusr(self, ctx, member, reason: str = "No reason provided"):
        try:
            toban = await commands.MemberConverter().convert(ctx, argument=member)
        except:
            try:
                toban = await commands.UserConverter().convert(ctx, argument=member)
            except:
                raise commands.BadArgument(message=ctx)
        await ctx.message.guild.ban(toban, delete_message_days = 7, reason = f"{ctx.author} (Softban) - {reason}")
        await ctx.message.guild.unban(toban, reason = f"{ctx.author} (Softban) - {reason}")
        await ctx.send(f":eyes: {str(toban)} has been soft banned.\nThis means they have been kicked, with messages less than 7 days old deleted.")

    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick')
    async def kickusr(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        await ctx.message.guild.kick(member, reason=f"{ctx.author} (Softban) - {reason}")
        await ctx.send(f":eyes: {str(member)} has been kicked. oof.")


# Add moderating cog to main instance.
def setup(bot):
    bot.add_cog(ModCog(bot))
