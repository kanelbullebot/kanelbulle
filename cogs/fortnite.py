import discord
from discord.ext import commands
import requests
import json


class FortniteCog:
    """FortniteCog"""


    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='fstatssquad')
    async def fortnitestatssquad(self, ctx, *, username: str):
        """Gets a players squad Fortnite stats."""
        url = "https://api.fortnitetracker.com/v1/profile/pc/" + "/" + (username)

        headerssquad = {
            'TRN-Api-Key': "FortniteTrackerApiKey",
            'Cache-Control': "no-cache",
        }

        responsesquad = requests.get(url, headers=headerssquad)
        print(responsesquad.text)
        jsfstatssolo = responsesquad.json()

        fortnitestatsembedsquad = discord.Embed(title='Squad Fortnite Stats',
                              description='Showing Squad Fortnite stats! Through the magic of Kanelbulle.',
                              colour=0x98FB98)

        fortnitestatsembedsquad.add_field(name="Username", value=(username))
        fortnitestatsembedsquad.add_field(name="Lifetime K/D", value=(jsfstatssolo["stats"]["p9"]["kd"]["value"]))
        fortnitestatsembedsquad.add_field(name="Lifetime Kills", value=(jsfstatssolo["stats"]["p9"]["kills"]["value"]))
        fortnitestatsembedsquad.add_field(name="Matches Played", value=(jsfstatssolo["stats"]["p9"]["matches"]["value"]))

        fstatssquad = "Showing Fortnite Squad Stats for: " + (username)
        await ctx.send(content=fstatssquad, embed=fortnitestatsembedsquad)

    @commands.command(name='fstatssolo')
    async def fortnitestatssolo(self, ctx, *, username: str):
        """Gets a players solo Fortnite stats."""
        url = "https://api.fortnitetracker.com/v1/profile/pc/" + "/" + (username)

        headerssolo = {
            'TRN-Api-Key': "FortniteTrackerApiKey",
            'Cache-Control': "no-cache",
        }

        responsesolo = requests.get(url, headers=headerssolo)
        print(responsesolo.text)
        jsfstatssolo = responsesolo.json()

        fortnitestatsembedsolo = discord.Embed(title='Solo Fortnite Stats',
                              description='Showing Solo Fortnite stats! Through the magic of Kanelbulle.',
                              colour=0x98FB98)

        fortnitestatsembedsolo.add_field(name="Username", value=(username))
        fortnitestatsembedsolo.add_field(name="Lifetime K/D", value=(jsfstatssolo["stats"]["p2"]["kd"]["value"]))
        fortnitestatsembedsolo.add_field(name="Lifetime Kills", value=(jsfstatssolo["stats"]["p2"]["kills"]["value"]))
        fortnitestatsembedsolo.add_field(name="Matches Played", value=(jsfstatssolo["stats"]["p2"]["matches"]["value"]))

        fstatssolo = "Showing Fortnite Solo Stats for: " + (username)
        await ctx.send(content=fstatssolo, embed=fortnitestatsembedsolo)

    @commands.command(name='fstatsduo')
    async def fortnitestatsduo(self, ctx, *, username: str):
        """Gets a players duo Fortnite stats."""
        url = "https://api.fortnitetracker.com/v1/profile/pc/" + "/" + (username)

        headersduo = {
            'TRN-Api-Key': "FortniteTrackerApiKey",
            'Cache-Control': "no-cache",
        }

        responseduo = requests.get(url, headers=headersduo)
        print(responseduo.text)
        jsfstatsduo = responseduo.json()

        fortnitestatsembedduo = discord.Embed(title='Duo Fortnite Stats',
                              description='Showing Duo Fortnite stats! Through the magic of Kanelbulle.',
                              colour=0x98FB98)

        fortnitestatsembedduo.add_field(name="Username", value=(username))
        fortnitestatsembedduo.add_field(name="Lifetime K/D", value=(jsfstatsduo["stats"]["p10"]["kd"]["value"]))
        fortnitestatsembedduo.add_field(name="Lifetime Kills", value=(jsfstatsduo["stats"]["p10"]["kills"]["value"]))
        fortnitestatsembedduo.add_field(name="Matches Played", value=(jsfstatsduo["stats"]["p10"]["matches"]["value"]))

        fstatsduo = "Showing Fortnite Duo Stats for: " + (username)
        await ctx.send(content=fstatsduo, embed=fortnitestatsembedduo)


        # await ctx.send(f"{len(fstats.decode("json"))}")


# Add Fortnite cog to main instance.
def setup(bot):
    bot.add_cog(FortniteCog(bot))
