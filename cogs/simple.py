import discord
from discord.ext import commands
import ast
import contextlib
import traceback
import textwrap
import io
import wikipedia

class SimpleCog:
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='add', aliases=['plus'])
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        """A simple command which does addition on two integer values."""

        total = first + second
        await ctx.send(f'The sum of **{first}** and **{second}**  is  **{total}**')



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


    async def on_member_ban(self, guild, user):
        """Event Listener which is called when a user is banned from the guild.
        For this example I will keep things simple and just print some info.
        Notice how because we are in a cog class we do not need to use @bot.event
        For more information:
        http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_member_ban
        Check above for a list of events.
        """

        print(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(SimpleCog(bot))
