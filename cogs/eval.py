import discord
from discord.ext import commands

class EvalCog:
    """EvalCog"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='eval')
    @commands.is_owner()
    async def debug(self, ctx, *, code : str):
        """Evaluates code."""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
           return

        await self.bot.say(python.format(result))


# Add Eval cog to the bot.
def setup(bot):
    bot.add_cog(EvalCog(bot))
