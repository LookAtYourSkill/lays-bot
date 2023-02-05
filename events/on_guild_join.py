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


        with open("json/settings.json", "r") as f:
            settings_data = json.load(f)

        settings_data[guild.id] = {
            "anti_alt_days": 7,
            "standard_avatar_check": False,
            "twitch_with_viewer": True,
            "twitch_with_game": True,
            "twitch_with_streamer": True,
            "twitch_with_avatar": True,
            "twitch_with_thumbnail": True
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
            1014844750584614962
        )
        await send_channel.send(
            embed=embed
        )


def setup(bot):
    bot.add_cog(on_guild_add(bot))
