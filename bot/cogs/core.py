import discord
from discord.ext import commands
import ast
import redis
import contextlib
import traceback
import textwrap
import io
import asyncpg
import asyncio
import wikipedia
from shutil import copyfile

class CoreCog:
    """CoreCog"""

    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    @commands.guild_only()
    async def serverstats(self, ctx, *, guildid: int = None):
        if guildid == None:
            serverstats = discord.Embed()
            serverstats.set_thumbnail(url=ctx.guild.icon_url)
            serverstats.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
            serverstats.add_field(name="Server Location", value=ctx.guild.region, inline=False)
            serverstats.add_field(name="ID", value=ctx.guild.id, inline=False)
            serverstats.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
            await ctx.send(content="", embed=serverstats)
        else:
            try:
                selectedguildserverstats = self.bot.get_guild(guildid)
                serverstats = discord.Embed()
                serverstats.set_thumbnail(url=selectedguildserverstats.icon_url)
                serverstats.add_field(name="Guild Name", value=selectedguildserverstats.name, inline=False)
                serverstats.add_field(name="Server Location", value=selectedguildserverstats.region, inline=False)
                serverstats.add_field(name="ID", value=selectedguildserverstats.id, inline=False)
                serverstats.add_field(name="Member count", value=selectedguildserverstats.member_count, inline=False)
                await ctx.send(content="", embed=serverstats)
            except:
                raise commands.BadArgument(message=f"Server/Guild {guildid} could not be found.")
                
    @commands.command()
    @commands.guild_only()
    async def userinfo(self, ctx, *, userid: int = None):
        if userid == None:
            userinfo = discord.Embed()
            userinfo.set_thumbnail(url=ctx.author.avatar_url)
            userinfo.add_field(name="Username", value=ctx.author, inline=False)
            userinfo.add_field(name="User ID", value=ctx.author.id, inline=False)
            if ctx.author.status == discord.Status("dnd"):
                status = "DND <:KanelbulleDnD:528992490003496962>"
            else:
                if ctx.author.status == discord.Status("online"):
                    status = "Online <:KanelbulleOnline:528991869217013762>"
                else:
                    if ctx.author.status == discord.Status("idle"):
                        status = "AFK <:KanelbulleAFK:528992291285630986>"
                    else:
                        status = "Offline <:KanelbulleOffline:528992410261258270>"
                        
            userinfo.add_field(name="Nickname", value=ctx.author.nick, inline=False)
            userinfo.add_field(name="Status", value=status, inline=False)
            await ctx.send(content="", embed=userinfo)
        else:
            try:
                selecteduserinfostats = self.bot.get_guild(userid)
                userinfo = discord.Embed()
                userinfo.set_thumbnail(url=selecteduserinfostats.avatar_url)
                usernameforselected = selecteduserinfostats.name + selecteduserinfostats.discriminator
                userinfo.add_field(name="Username", value=usernameforselected, inline=False)
                userinfo.add_field(name="User ID", value=userid, inline=False)
                if selecteduserinfostats.status == discord.Status("dnd"):
                    status = "DND <:KanelbulleDnD:528992490003496962>"
                else:
                    if selecteduserinfostats.status == discord.Status("online"):
                        status = "Online <:KanelbulleOnline:528991869217013762>"
                    else:
                        if selecteduserinfostats.status == discord.Status("idle"):
                            status = "AFK <:KanelbulleAFK:528992291285630986>"
                        else:
                            status = "Offline <:KanelbulleOffline:528992410261258270>"
                        
                userinfo.add_field(name="Nickname", value=ctx.author.nick, inline=False)
                userinfo.add_field(name="Status", value=status, inline=False)
                await ctx.send(content="", embed=userinfo)
            except:
                    raise commands.BadArgument(message=f"User {userid} could not be found.")
                
    @commands.command()
    async def hug (self, ctx, tohug = None, *, message = None):
        if not isinstance(ctx.channel, discord.DMChannel):
            if tohug != None:
                try:
                    member = await commands.MemberConverter().convert(ctx=ctx, argument=tohug)
                except:
                    await ctx.send(f"You try hugging ``{tohug}`` but I can't find them. *smh*\nAre you sure you typed it correctly? Or is ``{tohug}`` hiding from you?")
                else:
                    if member.bot:
                        if member == self.bot.user:
                            await ctx.send(f"You want to hug me? Thanks fren <:blobheart:466609019050524673>")
                    if message:
                        await ctx.send(f'{member.mention} was successfully hugged! "{message}"')
                    else:
                        await ctx.send(f'{member.mention} was successfully hugged!')
            else:
                await ctx.send("You hug the air. *smh*")
        else:
            if tohug != None:
                await ctx.send(f"You find yourself in a strange place. You search for something, a {tohug}, unsure what it is even.\nYou search far and wide, and, suddenly, you find {self.client.user.mention}, warning you that this command can't be used in DMs.\nThat was an unexpected ending, wasn't it?")
            else:
                await ctx.send("First, you haven't specified what to hug. Second, this command can't be used in DMs.\nWhat about if we move to a *real server*? duh.")


    @commands.command(name='add', aliases=['plus'])
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        """A simple command which does addition on two integer values."""

        total = first + second
        await ctx.send(f'The sum of **{first}** and **{second}**  is  **{total}**')

    @commands.command(name='setup')
    @commands.guild_only()
    async def setup_config(self, ctx):
        """Create a initial setup file for your server."""
        if ctx.author == ctx.guild.owner:
            setupmsg = await ctx.send("Setup initiated. :ok_hand:")
            copyfile("configs/standard.yml", f"configs/{ctx.guild.id}.yml")
            await setupmsg.edit(content="Setup done :white_check_mark:")
        else:
            await ctx.send("Only the server owner can run the setup command.")

    @commands.command(name="wiki", aliases=["wikipedia"])
    async def search_wiki(self, ctx, *, tosearch: str):
        await ctx.trigger_typing()
        numbers_stringed = {"one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5}
        async def genlist(results, type, pagename = None):
            result_list = ""
            for timeslooped, item in enumerate(results):
                result_list += f"{timeslooped+1} - {item}\n"
            if type == 1:
                await ctx.send(f"This page is a disambiguation.\n{pagename} may refer to:\n\n```{result_list}```")
            else:
                await ctx.send(f"Say the number of a result of the above\n\n```{result_list}```")
            def check(m):
                return m.author == ctx.author
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            lowered = msg.content.lower()
            if msg == None:
                await ctx.send("Timeout reached, aborting...")
            else:
                try:
                    integered = int(msg.content)
                    try:
                        if results[integered - 1] and integered > 0:
                            await genwiki(results[integered - 1], ctx)
                        else:
                            await ctx.send("That result isn't in the list, aborting...")
                            print("Was 1")
                    except UnboundLocalError as error:
                        pass
                    except:
                        await ctx.send("That result isn't in the list, aborting...")
                except:
                    try:
                        if results[numbers_stringed[msg.content] - 1]:
                            await genwiki(results[numbers_stringed[msg.content] - 1], ctx)
                    except:
                        await ctx.send("That result isn't in the list, aborting...\nYou must provide a number.")
        async def genwiki(pagename, ctx):
            await ctx.trigger_typing()
            try:
                page = wikipedia.page(pagename)
            except wikipedia.exceptions.DisambiguationError as error:
                await genlist(error.options[:5], 1, pagename)
                return
            except wikipedia.exceptions.PageError:
                linkname = pagename.replace(" ", "_")
                await ctx.send(f"That page doesn't exist.\nYou are referencing a page that is referenced in the wiki, but Wikipedia is returning a 404 error (Page doesn't exist).\n\nYou could, anyway, create one: https://en.wikipedia.org/wiki/{linkname}")
            except wikipedia.exceptions.HTTPTimeoutError:
                await ctx.send("Wikipedia took too long to respond.\nWikipedia could be experiencing connectivity issues.")
            if len(page.summary) > 300:
                summary = page.summary[:300]+"..."
            else:
                summary = page.summary
            linkname = pagename.replace(" ", "_")
            wikiembed = discord.Embed(title=f'{pagename} - Wikipedia',
                            description=f"{summary}\n\n[Read more](https://en.wikipedia.org/wiki/{linkname})",
                            colour=0x98FB98)
            wikiembed.set_thumbnail(url=page.images[0])
            await ctx.send(embed=wikiembed)
        results = wikipedia.search(tosearch, 5)
        if results:
            if len(results) == 1 or tosearch.lower() == results[0].lower():
                await genwiki(results[0], ctx)
            else:
                await genlist(results, 2)
        else:
            await ctx.send(f"I found nothing about `{tosearch}` on Wikipedia, did you commit a typo?")



def setup(bot):
    bot.add_cog(CoreCog(bot))
