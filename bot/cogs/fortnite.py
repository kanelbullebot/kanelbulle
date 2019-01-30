import discord
from discord.ext import commands
import requests
import json
import yaml

class FortniteCog:
    """FortniteCog"""


    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='fstats')
    async def fstats(self, ctx, *, username: str):
        try:
            with open(f"configs/{ctx.guild.id}.yml") as gconfig:
                guildsettings = yaml.safe_load(gconfig)
        except:
            await ctx.send("Uh oh, something probably went **entirely wrong** but it seems like your server is lacking a configuration, type ``<.setup`` to create a default config.")
            return
        if guildsettings["commands"]["fortnite"]["enabled"] == True:
            url = "https://api.scoutsdk.com/graph"
            headers = {
                'Accept': "application/com.scoutsdk.graph+json; version=1.1.0; charset=utf8",
                'Content-Type': "application/json",
                'Scout-App': "Scout token here",
                'cache-control': "no-cache"
                }

            idlookup = "{\"query\":\"{\\n  players(title: \\\"fortnite\\\", platform: \\\"epic\\\", identifier: \\\"" + (username) + "\\\", exact: true) {\\n    results {\\n      player {\\n        playerId\\n        handle\\n      }\\n    }\\n  }\\n}\"}"
            responseid = requests.request("POST", url, data=idlookup, headers=headers)
            responseidparsed = responseid.json()
            userid = responseidparsed["data"]["players"]["results"][0]["player"]["playerId"]
            data = "{\"query\":\"{\\n  player(title: \\\"fortnite\\\", id: \\\"" + (userid) + "\\\", segment: \\\"*\\\") {\\n    id\\n    metadata {\\n      key\\n      name\\n      value\\n      displayValue\\n    }\\n    stats {\\n      metadata {\\n        key\\n        name\\n        isReversed\\n      }\\n      value\\n      displayValue\\n    }\\n  }\\n}\"}"

            responsestats = requests.post(url, headers=headers, data=data)
            responsestatsparsed = responsestats.json()

            fstatsembed = discord.Embed(title='Fortnite Stats',
                                description='Showing Fortnite stats! Through the magic of Kanelbulle.',
                                colour=0x98FB98)

            fstatsembed.add_field(name="Username", value=(username))
            fstatsembed.add_field(name="Lifetime K/D", value=(responsestatsparsed["data"]["player"]["stats"][8]["displayValue"]))
            fstatsembed.add_field(name="Lifetime Kills", value=(responsestatsparsed["data"]["player"]["stats"][0]["displayValue"]))
            fstatsembed.add_field(name="Matches Played", value=(responsestatsparsed["data"]["player"]["stats"][2]["displayValue"]))
            fstatsembed.add_field(name="Lifetime Wins", value=(responsestatsparsed["data"]["player"]["stats"][3]["displayValue"]))

            message = "Showing Stats for: " + (username)
            await ctx.send(content=message, embed=fstatsembed)
        else:
            await ctx.send("That command is not enabled for this server! (If you are the server owner you can change enabled/disabled commands by contacting a global admin.")


# Add Fortnite cog to main instance.
def setup(bot):
    bot.add_cog(FortniteCog(bot))
