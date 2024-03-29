from disnake.ext import commands
import json


class guildCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # print([g.id for g in self.bot.guilds])
        with open("json/guild.json", "r") as guild_info:
            guild_data = json.load(guild_info)

        with open("json/tickets.json", "r") as ticket_info:
            ticket_data = json.load(ticket_info)

        with open("json/settings.json", "r") as settings_info:
            settings_data = json.load(settings_info)

        # going through all guilds, the bot is in
        for guild in self.bot.guilds:
            # check if the guild is in the json file
            if str(guild.id) in guild_data:
                pass
            else:
                # if not add it to the json file
                # !! print(f"{guild.name} has been added to the guild list")
                guild_data[guild.id] = {
                    "server_name": f"{str(guild.name)}",
                    "server_id": f"{str(guild.id)}",
                    "notify_channel": False,
                    "youtube-notificationChannel": False,
                    "ticket_category": False,
                    "closed_ticket_category": False,
                    "ticket_log_channel": False,
                    "ticket_save_channel": False,
                    "join_to_create_channel": False,
                    "join_to_create_category": False,
                    "msg_channel": False,
                    "mod_channel": False,
                    "welcome_channel": False,
                    "join_role": False,
                    "watchlist": [],
                    "youtubeWatchlist": [],
                    "youtube_notifications": "off",
                    "twitch_with_everyone_or_pingrole": "off",
                    "twitch_notifications": "off",
                    "twitch_ping_role": []
                }

                with open("json/guild.json", "w") as dumpfile:
                    json.dump(guild_data, dumpfile, indent=4)

        # same here, going through all guilds the bot is in
        for _guild in self.bot.guilds:
            # check if the guild is in the json file
            if str(_guild.id) in ticket_data:
                pass
            else:
                # if not add it to the json file
                # !! print(f"{_guild.name} has been added to the ticket list")
                ticket_data[_guild.id] = {
                    "ticket_counter": 0,
                    "support_members": [],
                    "support_roles": []
                }

                with open("json/tickets.json", "w") as dumpfile:
                    json.dump(ticket_data, dumpfile, indent=4)

        for ___guild in self.bot.guilds:
            # check if the guild is in the json file
            if str(___guild.id) in settings_data:
                pass
            else:
                # if not add it to the json file
                # !! print(f"{___guild.name} has been added to the settings list")
                settings_data[___guild.id] = {
                    "anti_alt_days": 0,
                    "standard_avatar_check": False,
                    "twitch_with_viewer": True,
                    "twitch_with_game": True,
                    "twitch_with_streamer": True,
                    "twitch_with_avatar": True,
                    "twitch_with_thumbnail": True
                }

                with open("json/settings.json", "w") as dumpfile:
                    json.dump(settings_data, dumpfile, indent=4)


def setup(bot):
    bot.add_cog(guildCheck(bot))
