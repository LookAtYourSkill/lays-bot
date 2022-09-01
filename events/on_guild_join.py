from binhex import openrsrc
import json
from disnake.ext import commands
import disnake


class on_guild_add(commands.Cog):
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
            "notify_channel": False,
            "ticket_category": False,
            "closed_ticket_category": False,
            "ticket_log_channel": False,
            "ticket_save_channel": False,
            "msg_channel": False,
            "mod_channel": False,
            "welcome_channel": False,
            "join_role": False,
            "license": [],
            "watchlist": [],
            "twitch_with_everyone": "off"
        }

        guild_data[str(guild.id)] = new_server
        with open("json/guild.json", "w") as f:
            json.dump(guild_data, f, indent=4)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        new_ticket = {
            "ticket_counter": 0,
            "support_members": [],
            "support_roles": []
        }

        ticket_data[str(guild.id)] = new_ticket
        with open("json/tickets.json", "w") as f:
            json.dump(ticket_data, f, indent=4)

        with open("json/active_check.json", "r") as f:
            active_data = json.load(f)

        active_data[guild.id] = {
            "about": True,
            "antialt": True,
            "changelog": True,
            "help": True,
            "info": True,
            "license": True,
            "meme": True,
            "moderation": True,
            "owner": False,
            "music": False,
            "roles": True,
            "setup": True,
            "suggestion": True,
            "ticket": True,
            "timer": False,
            "twitter": False,
            "twitch": True
        }

        with open("json/active_check.json", "w") as dumpfile:
            json.dump(active_data, dumpfile, indent=4)

        with open("json/settings.json", "r") as f:
            settings_data = json.load(f)

        settings_data[guild.id] = {
            "anti_alt_days": 7
        }

        with open("json/settings.json", "w") as dumpfile:
            json.dump(settings_data, dumpfile, indent=4)

        embed = disnake.Embed(
            title="I just got added to a server!",
            description=f"Server Name: `{guild.name}`\n"
                        f"Server ID: `{guild.id}`\n"
                        f"Server Owner: `{guild.owner}`\n"
                        f"Server Owner ID: `{guild.owner.id}`\n"
                        f"Server Member Count: `{guild.member_count}`",
            color=disnake.Color.green()
        )

        send_channel = self.bot.get_channel(
            882721258301685790
        )
        await send_channel.send(
            embed=embed
        )


def setup(bot):
    bot.add_cog(on_guild_add(bot))
