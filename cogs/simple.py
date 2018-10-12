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

    @commands.command(name='repeat', aliases=['copy', 'mimic'])
    async def do_repeat(self, ctx, *, our_input: str):
        """A simple command which repeats our input.
        In rewrite Context is automatically passed to our commands as the first argument after self."""

        await ctx.send(our_input)

    @commands.command(name='add', aliases=['plus'])
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        """A simple command which does addition on two integer values."""

        total = first + second
        await ctx.send(f'The sum of **{first}** and **{second}**  is  **{total}**')

    @commands.command(name='me')
    @commands.is_owner()
    async def only_me(self, ctx):

        await ctx.send(f'Hello {ctx.author.mention}. This command can only be used by you!!')

    @commands.command(name='embeds')
    @commands.guild_only()
    async def example_embed(self, ctx):

        embed = discord.Embed(title='Embed',
                              description='Showcasing the use of Embeds...\nSee the visualizer for more info.',
                              colour=0x98FB98)
        embed.set_author(name='TristanFarkas',
                         url='https://github.com/trilleplay')
                #         icon_url='http://i.imgur.com/ko5A30P.png')

        embed.add_field(name="Github repository", value="https://github.com/trilleplay/kanelbulle/")
        embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
        embed.add_field(name="Invite", value="Right now Kanelbulle is private due to resource limitations. If you would like to apply/request access, you may do so over at my discord server: https://discord.gg/FBMrcYM in the #invite-kanelbulle channel. ")


        await ctx.send(content='**Kanelbulle**', embed=embed)
 # Eval Command - https://github.com/Rapptz/RoboDanny by Rapptz read credit.md for License
    def insert_returns(body):
        # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].body)
            insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)


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

    @commands.command(hidden=True, name='eval')
    @commands.is_owner()
    async def eval(self, ctx:commands.Context, *, code: str):
        output = None
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }

        env.update(globals())

        if code.startswith('```'):
            code = "\n".join(code.split("\n")[1:-1])

        out = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            output = f'{e.__class__.__name__}: {e}'
        else:
            func = env['func']
            try:
                with contextlib.redirect_stdout(out):
                    ret = await func()
            except Exception as e:
                value = out.getvalue()
                output = f'{value}{traceback.format_exc()}'
            else:
                value = out.getvalue()
                if ret is None:
                    if value:
                        output = value
                else:
                    output = f'{value}{ret}'
        if output is not None:
            await ctx.send(output)
        else:
            await ctx.send("I did a thing!")

    async def init_eval(self, ctx, pages):
        page = pages[0]
        num = len(pages)
        return f"**Eval output 1/{num}**\n```py\n{page}```", None, num > 1, []

    async def update_eval(self, ctx, message, page_num, action, data):
        pages = data["pages"]
        page, page_num = Pages.basic_pages(pages, page_num, action)
        return f"**Eval output {page_num + 1}/{len(pages)}**\n```py\n{page}```", None, page_num

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
