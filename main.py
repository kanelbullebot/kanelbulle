import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='<')

@bot.event
async def on_ready():
    print(bot.user.name)
    print('Signed into bot user.')

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)



@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Kanelbulle", description="Made with <3 by Tristan Farkas.", color=0xeee657)
    embed.add_field(name="Author", value="@tristanfarkas#0001")
    embed.add_field(name="Github repository", value="https://github.com/trilleplay/kanelbulle/")
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Invite", value="Right now Kanelbulle is private due to resource limitations. If you would like to apply/request access, you may do so over at my discord server: https://discord.gg/FBMrcYM in the #invite-kanelbulle channel. ")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Kanelbulle", description="Made with <3 by Tristan Farkas.", color=0xedab49)

    embed.add_field(name="<add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="<multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="<info", value="Gives some helpful stats about Kanelbulle.", inline=False)
    embed.add_field(name="<help", value="Prints out information/docs on how to use Kanelbulle.", inline=False)

    await ctx.send(embed=embed)

bot.run('BOT_TOKEN')
