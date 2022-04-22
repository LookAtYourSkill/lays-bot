import disnake
from disnake.ext import commands
from textwrap import dedent
import json
from utils.twitch import get_streams, get_users

class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        description="Adds a streamer to your watchlist"
    )
    @commands.has_permissions(administrator=True)
    async def add(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        streamer
    ):
        try:
            with open("json/guild.json", "r", encoding="UTF-8") as file:
                data = json.load(file)
            with open("json/watchlist.json", "r", encoding="UTF-8") as file2:
                data2 = json.load(file2)

            if streamer in data[str(interaction.guild.id)]["watchlist"]:
                alreday_streamer_error_embed = disnake.Embed(
                    description=f"Der Streamer [`{streamer}`] **ist bereits** in der **Watchlist**!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=alreday_streamer_error_embed,
                    ephemeral=True
                )
            elif streamer not in data[str(interaction.guild.id)]["watchlist"]:
                data[str(interaction.guild.id)]["watchlist"].append(streamer.lower())
                with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                    json.dump(data, dump_file, indent=4)

                data2["overall_watchlist"].append(streamer.lower())
                with open("json/watchlist.json", "w", encoding="UTF-8") as dump_file2:
                    json.dump(data2, dump_file2, indent=4)

                add_embed = disnake.Embed(
                    description=f"Der Streamer [`{streamer}`] wurde zur Watchlist **hinzugefügt**!",
                    color=disnake.Color.blurple()
                )
                await interaction.response.send_message(
                    embed=add_embed,
                    ephemeral=True
                )
        except ValueError:
            pass

    @commands.slash_command(
        description="Removes a streamer from your watchlist"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def remove(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        streamer
    ):
        try:
            with open("json/guild.json", "r", encoding="UTF-8") as file:
                data = json.load(file)

            if streamer not in data[str(interaction.guild.id)]["watchlist"]:
                alreday_streamer_error_embed = disnake.Embed(
                    description=f"Der Streamer [`{streamer}`] **ist nicht** in der **Watchlist**!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=alreday_streamer_error_embed,
                    ephemeral=True
                )
            elif streamer in data[str(interaction.guild.id)]["watchlist"]:
                data[str(interaction.guild.id)]["watchlist"].remove(streamer.lower())
                with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                    json.dump(data, dump_file, indent=4)

                remove_embed = disnake.Embed(
                    description=f"Der Streamer [`{streamer}`] wurde aus der Watchlist **entfernt**!",
                    color=disnake.Color.blurple()
                )
                await interaction.response.send_message(
                    embed=remove_embed,
                    ephemeral=True
                )
        except ValueError:
            pass

    @commands.slash_command(
        description="Checks the twitch stream watchlist from this server"
    )
    async def check(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        users = get_users(guild_data[str(interaction.guild.id)]["watchlist"])
        streams = get_streams(users)

        embed = disnake.Embed(
            color=disnake.Color.purple()
        )
        embed.set_author(
            name="Who is Live?",
            icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png",
            url="https://twitch.tv"
        )
        embed.set_thumbnail(
            url="https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png"
        )
        if streams:
            for stream in streams.values():

                embed.add_field(
                    name=f"Name : {stream['user_name']}",
                    value=dedent(
                        f"""
                            **Title :** __{stream["title"]}__
                            **Viewer :** ``{stream["viewer_count"]}``
                            **Game :** ``{stream["game_name"]}``
                            **Streamt gestartet:** ``{stream["started_at"][11:][:5]} Uhr am {stream["started_at"][8:][:2]}.{stream["started_at"][5:][:2]}.{stream["started_at"][:4]}``
                            **Link :** https://www.twitch.tv/{stream["user_login"]}
                            >-------------------------------------------------------------------------<
                        """
                    ),
                    inline=False
                )
        else:
            embed.add_field(
                name="__Nobody is Live!__",
                value="No streamer from your watchlist is live!",
                inline=False
            )

        if len(streams) == 1:
            await interaction.response.send_message(
                f"{interaction.author.mention} Dein Stream Check. Es ist **1 Streamer Live!**",
                embed=embed
            )
        else:
            await interaction.response.send_message(
                f"{interaction.author.mention} Dein Stream Check. Es sind insgesamt **{len(streams)} Streamer Live!**",
                embed=embed
            )


def setup(bot):
    bot.add_cog(Twitch(bot))
