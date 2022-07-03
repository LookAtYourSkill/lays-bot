from disnake.ext import commands
import json


class GuildCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # print([g.id for g in self.bot.guilds])
        with open("json/guild.json", "r") as guild_info:
            guild_data = json.load(guild_info)

        with open("json/tickets.json", "r") as ticket_info:
            ticket_data = json.load(ticket_info)

        for guild in self.bot.guilds:
            if str(guild.id) in guild_data:
                pass
            else:
                print(f"{guild.name} has been added to the guild list")
                guild_data[guild.id] = {
                    "server_name": f"{str(guild.name)}",
                    "notify_channel": (),
                    "ticket_category": (),
                    "closed_ticket_category": (),
                    "ticket_log_channel": (),
                    "ticket_save_channel": (),
                    "msg_channel": (),
                    "mod_channel": (),
                    "welcome_channel": (),
                    "join_role": (),
                    "license": [],
                    "watchlist": []
                }

                with open("json/guild.json", "w") as dumpfile:
                    json.dump(guild_data, dumpfile, indent=4)

        for _guild in self.bot.guilds:
            if str(guild.id) in ticket_data:
                pass
            else:
                print(f"{_guild.name} has been added to the ticket list")
                ticket_data[_guild.id] = {
                    "ticket_counter": 0
                }

                with open("json/tickets.json", "w") as dumpfile:
                    json.dump(ticket_data, dumpfile, indent=4)


def setup(bot):
    bot.add_cog(GuildCheck(bot))
