import json
from disnake.ext import commands
import disnake


class on_guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(
        self,
        guild
    ):
        on_join_embed = disnake.Embed(
            title="Successful invite!",
            description="You sccessfully invited me to your server!\n"
                        "To set me perfectly up, use all of the `/setup` commands!"
        )
        await guild.owner.send(
            embed=on_join_embed
        )

        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        new_server = {
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

        guild_data[str(guild.id)] = new_server
        with open("json/guild.json", "w") as f:
            json.dump(guild_data, f, indent=4)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        new_ticket = {
            "ticket_counter": 0,
        }

        ticket_data[str(guild.id)] = new_ticket
        with open("json/tickets.json", "w") as f:
            json.dump(ticket_data, f, indent=4)


def setup(bot):
    bot.add_cog(on_guild(bot))
