from discord.ext import commands
import subprocess

 # Declase bash scripts to run here.
bashgitpull = "git pull"

class AdminCog:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='hotreload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx):
        """We get the latest updates to the whitelisted cogs from Git."""

        try:
            process = subprocess.Popen(bashgitpull.split(), stdout=subprocess.PIPE)
            self.bot.unload_extension('cogs.simple')
            self.bot.load_extension('cogs.simple')
            self.bot.unload_extension('cogs.moderating')
            self.bot.load_extension('cogs.moderating')
            self.bot.unload_extension('cogs.admin')
            self.bot.load_extension('cogs.admin')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`Kanelbulle has successfully updated with NO Downtime! Wowee!`**')


def setup(bot):
    bot.add_cog(AdminCog(bot))
