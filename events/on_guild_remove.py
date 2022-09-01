import json
from disnake.ext import commands
import disnake


class on_guild_rmv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(
        self,
        guild: disnake.Guild
    ):
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        del guild_data[str(guild.id)]
        with open("json/guild.json", "w") as f:
            json.dump(guild_data, f, indent=4)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        del ticket_data[str(guild.id)]
        with open("json/tickets.json", "w") as f:
            json.dump(ticket_data, f, indent=4)


def setup(bot):
    bot.add_cog(on_guild_rmv(bot))
