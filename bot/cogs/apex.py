import discord
from discord.ext import commands
import random
import yaml
import aiohttp
import json

with open("config.json") as dataf:
    returnconfig = json.load(dataf)

class ApexCog:
    """ApexCog"""


    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='apexstats')
    async def apexstatslookup(self, ctx, username, platform: str = None):
        if platform == None:
            apexplatform = "5"
        elif platform == "pc":
            apexplatform = "5"
        elif platform == "psn":
            apexplatform = "2"
        elif platform == "xbox":
            apexplatform = "1"
        else:
            await ctx.send("I dont have access to stats from that platform yet. I'm only able to retrive stats from ``pc``, ``psn`` and ``xbox``")
            return

        httpsession = aiohttp.ClientSession()
        url = "https://public-api.tracker.gg/apex/v1/standard/profile/" + apexplatform + "/" + (username)
        headers = {"TRN-Api-Key": returnconfig['Apex-Api-Key']}
        async with httpsession.get(url, headers=headers) as resp:
            if resp.status == 404:
                await ctx.send("That user could not be found for the selected platform.")
                await httpsession.close()
                return
            responsejsondecoded = await resp.json()

        apexstatsembed = discord.Embed(title='Apex Stats',
                            description='Showing Apex stats! Through the magic of Kanelbulle.',
                            colour=0x98FB98)

        apexstatsembed.add_field(name="Username", value=(responsejsondecoded["data"]["metadata"]["platformUserHandle"]))
        apexstatsembed.add_field(name="Level", value=(responsejsondecoded["data"]["stats"][0]["value"]))
        apexstatsembed.add_field(name="Kills", value=(responsejsondecoded["data"]["stats"][1]["value"]))
        apexstatsembed.add_field(name="Games Played", value="Games Played is currently unavailable while our stats provider is fixing their issues.)

        message = "Showing Apex Stats for: " + (responsejsondecoded["data"]["metadata"]["platformUserHandle"])
        await ctx.send(content=message, embed=apexstatsembed)
        await httpsession.close()


# Add random cog to main instance.
def setup(bot):
    bot.add_cog(ApexCog(bot))
