import json
from disnake.ext import commands


class on_guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('json/guild.json', 'r') as f:
            data = json.load(f)

        new_server = {
            "server_name": f"{str(guild.name)}",
            "notify_channel": (),
            "msg_channel": (),
            "mod_channel": (),
            "welcome_channel": (),
            "join_role": (),
            "watchlist": []
        }

        data[str(guild.id)] = new_server
        with open('json/guild.json', 'w') as f:
            json.dump(data, f, indent=4)


def setup(bot):
    bot.add_cog(on_guild(bot))
