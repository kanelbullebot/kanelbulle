import discord
from discord.ext import commands
from utilities import translate, returncfg

class ModCog(commands.Cog):
    """ModCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def banusr(self, ctx, user: discord.Member, *, reason: str = "No reason provided"):
        if user.top_role > ctx.guild.me.top_role:
            raise commands.BadArgument(message = f"{user} Has a higher role then me, I'm unable to ban {user} without having a higher role than them.")
        elif user.top_role > ctx.author.top_role:
            raise commands.BadArgument(message = f"User/Member {user} has a higher role then you, you need to have a higher role then {user} to be able to ban them.")
        else:
            await ctx.message.guild.ban(user, delete_message_days = 7, reason = f"{ctx.author} - {reason}")
            await ctx.send(f":eyes: {str(user)} has been banned. oof.")

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name='unban')
    async def unbanusr(self, ctx, user:discord.User, reason: str = "No reason provided"):
        await ctx.message.guild.unban(tounban, reason = f"{ctx.author} (Unban) - {reason}")
        await ctx.send(f":eyes: {str(toban)} has been unbanned. ")

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name='softban')
    async def softbanusr(self, ctx, user, reason: str = "No reason provided"):
        try:
            toban = await commands.MemberConverter().convert(ctx, argument=member)
        except:
            try:
                toban = await commands.UserConverter().convert(ctx, argument=member)
            except:
                raise commands.BadArgument(message=f"User/Member {user} not found.")
        await ctx.message.guild.ban(toban, delete_message_days = 7, reason = f"{ctx.author} (Softban) - {reason}")
        await ctx.message.guild.unban(toban, reason = f"{ctx.author} (Softban) - {reason}")
        await ctx.send(f":eyes: {str(toban)} has been soft banned.\nThis means they have been kicked, with messages less than 7 days old deleted.")

    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(name='kick')
    async def kickusr(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        guildlang = "en"
        guildsettings = await returncfg.fetchguildconfig(ctx.guild.id)
        try:
            guildlang = guildsettings["lang"]
        except:
            pass
        await ctx.message.guild.kick(member, reason=f"{ctx.author} (Softban) - {reason}")
        returntousr = translate.translate(lang=guildlang, string="kick", user=member)
        await ctx.send(returntousr)

    @commands.command(name='lock')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def lock_channel(self, ctx, *, reason:str = "No reason provided"):
        owrites = ctx.channel.overwrites_for(ctx.guild.default_role)
        if owrites.send_messages == False:
            await ctx.send("This channel is already locked!")
        else:
            owrites.send_messages = False
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=owrites, reason = f"{ctx.author} (Lock) - {reason}")
            owrites = discord.PermissionOverwrite(send_messages = True)
            await ctx.channel.set_permissions(ctx.guild.me, overwrite = owrites, reason = f"{ctx.author} (Lock) - {reason} - This action has been done so that Kanelbulle can later unlock the channel.")
            await ctx.send(f"Channel locked! Now people without a role can not send messages.\n\nReason:```{reason}```")

    @commands.command(name='unlock')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unlock_channel(self, ctx, *, reason:str = "No reason provided"):
        owrites = ctx.channel.overwrites_for(ctx.guild.default_role)
        if owrites.send_messages == True or owrites.send_messages == None:
            await ctx.send("This channel isn't locked!")
        else:
            owrites.send_messages = True
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=owrites, reason = f"{ctx.author} (Unlock) - {reason}")
            await ctx.send("Channel unlocked! Now people without a role can send messages.")
            owrites = ctx.channel.overwrites_for(ctx.guild.me)
            owrites.send_messages = None
            if owrites.is_empty():
                await ctx.channel.set_permissions(ctx.guild.me, overwrite=None, reason = f"{ctx.author} (Lock) - {reason} - This action was done so that Kanelbulle can later unlock the channel, switching it back to normal.")
            else:
                await ctx.channel.set_permissions(ctx.guild.me, overwrite=owrites, reason = f"{ctx.author} (Lock) - {reason} - This action was done so that Kanelbulle can later unlock the channel, switching it back to normal.")

    @commands.group(pass_context=True)
    async def clean(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('⚠️ Thats not a valid command! ⚠️')

    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @clean.command()
    async def all(self, ctx, mcount: int):
        await ctx.channel.purge(limit=mcount)
        await ctx.send(f"🚨 {int(mcount)} messages have been deleted.🚨")

# Add moderating cog to main instance.
def setup(bot):
    bot.add_cog(ModCog(bot))
