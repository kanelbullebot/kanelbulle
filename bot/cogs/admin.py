from discord.ext import commands
import subprocess
import discord
import traceback
import textwrap
import io
import contextlib

 # Declase bash scripts to run here.
bashgitpull = "git pull"

class AdminCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def system_cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`An error has occured:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`The cog has been successfully reloaded.`**')

    @commands.command(name='hotreload', hidden=True)
    @commands.is_owner()
    async def system_cog_hotreload(self, ctx):
        """We get the latest updates to the whitelisted cogs from Git."""

        try:
            process = subprocess.Popen(bashgitpull.split(), stdout=subprocess.PIPE)
            self.bot.unload_extension('cogs.core')
            self.bot.load_extension('cogs.core')
            self.bot.unload_extension('cogs.fortnite')
            self.bot.load_extension('cogs.fortnite')
            self.bot.unload_extension('cogs.moderating')
            self.bot.load_extension('cogs.moderating')
            self.bot.unload_extension('cogs.random')
            self.bot.load_extension('cogs.random')
            self.bot.unload_extension('cogs.apex')
            self.bot.load_extension('cogs.apex')
            self.bot.unload_extension('cogs.admin')
            self.bot.load_extension('cogs.admin')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`Kanelbulle has successfully updated with NO Downtime! Wowee!`**')

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

    @commands.command(name='KanelbulleAdminID')
    @commands.is_owner()
    async def only_me(self, ctx):
        await ctx.send(f' {ctx.author.mention} is an authorized Kanelbulle Global Admin.')

    @commands.command(name='depart')
    @commands.is_owner()
    async def server_depart(self, ctx, *, guildtoleave: int):
        leaveguild = self.bot.get_guild(guildtoleave)
        await leaveguild.leave()
        await ctx.send(f'Kanelbulle has now left that server. ')


def setup(bot):
    bot.add_cog(AdminCog(bot))
