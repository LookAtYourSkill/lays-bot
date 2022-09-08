from disnake.ext import commands
import json
from disnake.ext.tasks import loop


class twitchCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_twitch.start()

    @commands.Cog.listener()
    async def on_ready(self):
        with open("json/guild.json", "r") as guild_info:
            guild_data = json.load(guild_info)

        for i in guild_data:
            if guild_data[i]["twitch_notifications"] == "on":
                continue
            else:
                if guild_data[i]["notification_channel"] is False:
                    print(f"{i} has no notification channel")

                if guild_data[i]["watchlist"] is None:
                    print(f"{i} has no watchlist")
                else:
                    guild_data[i]["twitch_notifications"] = "on"
                    with open("json/guild.json", "w") as dumpfile:
                        json.dump(guild_data, dumpfile, indent=4)

    @loop(seconds=10)
    async def check_twitch(self):
        print("checking twitch")
        with open("json/guild.json", "r") as guild_info:
            guild_data = json.load(guild_info)

        for i in guild_data:
            if guild_data[i]["twitch_notifications"] == "on":
                continue
            else:
                if guild_data[i]["notification_channel"] is False:
                    print(f"{i} has no notification channel")

                if guild_data[i]["watchlist"] is None:
                    print(f"{i} has no watchlist")
                else:
                    guild_data[i]["twitch_notifications"] = "on"
                    with open("json/guild.json", "w") as dumpfile:
                        json.dump(guild_data, dumpfile, indent=4)


def setup(bot):
    bot.add_cog(twitchCheck(bot))
