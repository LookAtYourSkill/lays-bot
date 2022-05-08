import disnake
from disnake.ext import commands
from textwrap import dedent
import json
from datetime import datetime
import time
from utils.twitch import get_streams, get_users
from disnake.ext.tasks import loop


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_streams.start()

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
    @commands.cooldown(1, 3600, commands.BucketType.user)
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

    @commands.slash_command(
        name="list",
        description="Lists all streamers from your watchlist"
    )
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def list(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        loading_embed = disnake.Embed(
            description="Lade Antwort...",
            color=disnake.Color.blurple()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open("json/guild.json", "r", encoding="UTF-8") as file:
            data = json.load(file)

        if data[str(interaction.guild.id)]["watchlist"]:
            embed = disnake.Embed(
                description=f"{interaction.author.mention} the watchlist from {interaction.guild.name}",
                color=disnake.Color.blurple()
            )
            streamer_list = []
            for streamer in data[str(interaction.guild.id)]["watchlist"]:
                streamer_list.append(streamer)

            embed.add_field(
                name="__Streamer__",
                value="\n".join(streamer_list),
                inline=False
            )
            await interaction.edit_original_message(
                embed=embed
            )
        else:
            embed = disnake.Embed(
                description=f"{interaction.author.mention}",
                color=disnake.Color.red()
            )
            embed.add_field(
                name="__Watchlist is empty!__",
                value="There wasnt added a streamer to the watchlist till now!",
                inline=False
            )
            await interaction.edit_original_message(
                embed=embed
            )

    online_users = []

    @loop(seconds=90)
    async def check_streams(self):
        await self.bot.wait_until_ready()

        # load json files and setup local variables
        online_users = []

        with open("json/watchlist.json", "r", encoding="UTF-8") as file:
            watchlist_data = json.load(file)

        with open("json/guild.json", "r", encoding="UTF-8") as file:
            for i in json.load(file).values():

                print(i['watchlist'])
                print("[2] Going through guilds...")
                # get all streamers from watchlist
                users = get_users(watchlist_data["overall_watchlist"])
                streams = get_streams(users)

                # check if any streamer of the watchlist is live
                if streams:
                    print("[3] Check for streams...")

                    # go through all streams
                    for stream in streams.values():
                        print(f"[!] {stream['user_name']} is live!")
                        print("[4] Going through values of streams...")

                        # check if streamer is in not in watchlist, and if so, break and do nothing
                        if stream["user_login"] not in i['watchlist']:
                            print("[5] No stream found for guild...")
                            print()
                            break
                        else:
                            # check if streamer is in watchlist and if so, create embed and send it to channel
                            if stream["user_login"] in i['watchlist']:

                                for user_name in watchlist_data["overall_watchlist"]:
                                    # check if streamer is in streams and in local variable
                                    if user_name in streams and user_name not in online_users:
                                        # convert time to readable format
                                        giga_time = datetime.strptime(streams[user_name]['started_at'], "%Y-%m-%dT%H:%M:%SZ")
                                        # convert time aswell to readable format
                                        started_at = time.mktime(giga_time.timetuple()) + giga_time.microsecond / 1E6
                                        # check if time is in the past
                                        if time.time() - started_at < 4000:
                                            # if so append streamer to list, so its not sent again
                                            streams.append(streams[user_name])
                                            online_users.append(user_name)

                                            print("[5] Stream found")
                                            notify_channel = await self.bot.fetch_channel(i["notify_channel"])

                                            embed = disnake.Embed(
                                                title=f"{stream['title']}",
                                                color=disnake.Color.purple(),
                                                url=f"https://www.twitch.tv/{stream['user_login']}"
                                            )
                                            embed.add_field(
                                                name="Game",
                                                value=f"`{stream['game_name']}`",
                                                inline=True
                                            )
                                            embed.add_field(
                                                name="Viewer",
                                                value=f"`{stream['viewer_count']}`",
                                                inline=True
                                            )
                                            embed.set_author(
                                                name="Notification",
                                                icon_url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fmobile.twitter.com%2Ftwitchsupport&psig=AOvVaw3lBKonaxjmC9OVaff2Y67k&ust=1652057565274000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCNDrtZTYzvcCFQAAAAAdAAAAABAI",
                                            )
                                            embed.set_image(
                                                url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{stream['user_login']}-1920x1080.jpg"
                                            )

                                            # send embed to channel
                                            print("[6] Sending message...")
                                            await notify_channel.send(
                                                embed=embed
                                            )
                                        else:
                                            # if anything else happend, do nothing
                                            print("[5] Time from streamer is too high")
                                            break
                                    else:
                                        # if anything else happend, do nothing
                                        print("[5] Already in list")
                                        print()
                                        break
                else:
                    # if no streamer is live, do nothing
                    print("[3] No streams found...")
                    print()
                    break


def setup(bot):
    bot.add_cog(Twitch(bot))
