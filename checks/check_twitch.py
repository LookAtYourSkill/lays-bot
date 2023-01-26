import json

import colorama
from disnake.ext import commands
from disnake.ext.tasks import loop


class twitchCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_twitch.start()

    '''
    @commands.Cog.listener()
    async def on_ready(self):
        with open("json/guild.json", "r") as guild_info:
            guild_data = json.load(guild_info)

        for i in guild_data:
            if guild_data[i]["twitch_notifications"] == "on":
                continue
            else:
                if guild_data[i]["notify_channel"] is False:
                    print(f"{i} has no notification channel")

                if guild_data[i]["watchlist"] is None:
                    print(f"{i} has no watchlist")
                else:
                    guild_data[i]["twitch_notifications"] = "on"
                    with open("json/guild.json", "w") as dumpfile:
                        json.dump(guild_data, dumpfile, indent=4)
    '''

    @loop(hours=1)
    async def check_twitch(self):
        await self.bot.wait_until_ready()

        print(f"{colorama.Fore.CYAN} [TWITCH CHECK] [TASK] Checking guilds...{colorama.Fore.RESET}")

        # !! print(f"{colorama.Fore.LIGHTWHITE_EX} [TWITCH CHECK] [TASK] Checking guilds... {colorama.Fore.RESET}")

        with open("json/guild.json", "r") as guild_info:
            guild_data = json.load(guild_info)

        # i = guild id
        for i in guild_data:
            if guild_data[i]["twitch_notifications"] == "on":
                # !! print(f"{colorama.Fore.GREEN} [TWITCH CHECK] [SUCCESS] {i} is already on. {colorama.Fore.RESET}")
                continue
            else:
                if guild_data[str(i)]["notify_channel"] is False:
                    continue
                    # !! print(f"{colorama.Fore.RED} [TWITCH CHECK] [ERROR] {i} has no notification channel. {colorama.Fore.RESET}")

                if not guild_data[str(i)]["watchlist"]:
                    continue
                    # !! print(f"{colorama.Fore.RED} [TWITCH CHECK] [ERROR] {i} has no watchlist. {colorama.Fore.RESET}")

                else:
                    if guild_data[str(i)]["notify_channel"] and guild_data[str(i)]["watchlist"]:
                        # !! print(f"{colorama.Fore.GREEN} [TWITCH CHECK] [SUCCESS] {i} is now on. {colorama.Fore.RESET}")
                        guild_data[str(i)]["twitch_notifications"] = "on"
                        with open("json/guild.json", "w") as dumpfile:
                            json.dump(guild_data, dumpfile, indent=4)

        print(f"{colorama.Fore.CYAN} [TWITCH CHECK] [DONE] Finished checking guilds. {colorama.Fore.RESET}")


def setup(bot):
    bot.add_cog(twitchCheck(bot))
