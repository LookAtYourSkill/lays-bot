import json
import os
import time
import copy
from typing import Optional
import datetime
from datetime import datetime
from textwrap import dedent

import colorama
import disnake
from disnake.ext import commands
from disnake.ext.tasks import loop
from utils.twitch import get_streams, get_users, get_all_user_info, get_followers, update_streams, averageCalculation


class Twitch(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot
        self.error_channel = 882721258301685790
        self.check_streams.start()
        self.update.start()
        self.bot_png = "https://cdn.discordapp.com/avatars/947634210657681478/5b9dd998fbec81dcaf58340de0b98d9b.png?size=1024"

    @commands.slash_command(
        name="twitch",
        description="Group for twitch commands"
    )
    async def twitch(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @twitch.sub_command(
        description="Adds a streamer to your watchlist"
    )
    @commands.has_permissions(administrator=True)
    async def add(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        streamer
    ):
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            description="Füge Streamer zur Watchlist hinzu...",
            color=disnake.Color.blurple()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )

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
                await interaction.edit_original_message(
                    embed=alreday_streamer_error_embed
                )
            elif streamer not in data[str(interaction.guild.id)]["watchlist"]:
                data[str(interaction.guild.id)]["watchlist"].append(streamer.lower())
                with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                    json.dump(data, dump_file, indent=4)

                if streamer in data2["overall_watchlist"]:
                    pass

                else:
                    data2["overall_watchlist"].append(streamer.lower())

                    with open("json/watchlist.json", "w", encoding="UTF-8") as dump_file2:
                        json.dump(data2, dump_file2, indent=4)

                add_embed = disnake.Embed(
                    description=f"Der Streamer [`{streamer}`] wurde zur Watchlist **hinzugefügt**!",
                    color=disnake.Color.blurple()
                )
                await interaction.edit_original_message(
                    embed=add_embed
                )
        except ValueError:
            pass

    @twitch.sub_command(
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
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            description="Entferne Steramer von Watchlist...",
            color=disnake.Color.blurple()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )

        try:
            with open("json/guild.json", "r", encoding="UTF-8") as file:
                data = json.load(file)

            if streamer not in data[str(interaction.guild.id)]["watchlist"]:
                alreday_streamer_error_embed = disnake.Embed(
                    description=f"Der Streamer [`{streamer}`] **ist nicht** in der **Watchlist**!",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=alreday_streamer_error_embed
                )
            elif streamer in data[str(interaction.guild.id)]["watchlist"]:
                data[str(interaction.guild.id)]["watchlist"].remove(streamer.lower())
                with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                    json.dump(data, dump_file, indent=4)

                remove_embed = disnake.Embed(
                    description=f"Der Streamer [`{streamer}`] wurde aus der Watchlist **entfernt**!",
                    color=disnake.Color.blurple()
                )
                await interaction.edit_original_message(
                    embed=remove_embed
                )
        except ValueError:
            pass

    @twitch.sub_command(
        description="Checks the twitch stream watchlist from this server"
    )
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def check(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            description="Erhalte Daten von Twitch...",
            color=disnake.Color.blurple()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )

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

            await interaction.edit_original_message(
                embed=embed
            )

        else:
            embed.add_field(
                name="__Nobody is Live!__",
                value="No streamer from your watchlist is live!",
                inline=False
            )

            await interaction.edit_original_message(
                embed=embed
            )

    @twitch.sub_command(
        description="Get information about twitch channel"
    )
    async def info(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        streamer: str
    ):
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            description="Erhalte Daten von Twitch...",
            color=disnake.Color.blurple()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )

        try:
            userData = get_all_user_info(streamer)
            followUser = get_users(streamer)
            followData = get_followers(followUser[streamer])

            twitchTime = userData[0]['created_at']
            # format twitch date to timestamp
            finalTime = datetime.strptime(twitchTime, '%Y-%m-%dT%H:%M:%SZ').timestamp()

            embed = disnake.Embed(
                color=disnake.Color.purple()
            )
            embed.set_author(
                name="Twitch Channel Info",
                icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png",
                url="https://twitch.tv"
            )
            embed.add_field(
                name="__Information__",
                value=f"**Name :** `{userData[0]['display_name']}`\n"
                    f"**Login :** `{userData[0]['login']}`\n"
                    f"**ID :** `{userData[0]['id']}`\n"
                    f"**Follower :** `{followData['total']}`\n"
                    f"**Channel Views :** `{userData[0]['view_count']}`\n"
                    f"**Link :** [Click here](https://www.twitch.tv/{userData[0]['login']})\n"
                    f"**Broadcaster Type :** `{'None' if userData[0]['broadcaster_type'] == '' else userData[0]['broadcaster_type']}`\n"
                    f"**Created At :** <t:{int(finalTime)}:f>",
                inline=False
            )
            embed.set_thumbnail(
                url=userData[0]['profile_image_url']
            )
            embed.set_image(userData[0]['offline_image_url'])
            await interaction.edit_original_message(
                embed=embed
            )
        except Exception as _:
            embed = disnake.Embed(
                title="Error :x:",
                description=f"Streamer [`{streamer}`] not found!\n"
                            "Please **try it again later** or **check the spelling** of the username!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    choices = ["off", "everyone", "pingrole", "pingrole_and_everyone"]

    @twitch.sub_command(
        name="with_everyone",
        description="Get choice if live message should get sent with everyone or without"
    )
    # ! NEUE MODIS: OFF, EVERYONE, PINGROLE AND PINGROLE + EVERYONE
    async def live_message(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        choice: (Optional[str]) = commands.Param(
            None,
            name="option",
            description="Select the option you want",
            choices=[i for i in choices]
        )
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/guild.json", "r", encoding="UTF-8") as guild_file:
            guild_data = json.load(guild_file)

        loading_embed = disnake.Embed(
            description="Overriting settings...",
            color=disnake.Color.blurple()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )

        if choice.lower() == guild_data[str(interaction.guild.id)]["twitch_with_everyone_or_pingrole"]:
            embed = disnake.Embed(
                title="Error :x:",
                description=f"**{choice}** is already the current setting!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

        else:
            guild_data[str(interaction.guild.id)]["twitch_with_everyone_or_pingrole"] = choice

            with open("json/guild.json", "w", encoding="UTF-8") as guild_file:
                json.dump(guild_data, guild_file, indent=4)

            embed = disnake.Embed(
                title="Success :white_check_mark:",
                description=f"**{choice}** is now the current setting!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @twitch.sub_command(
        name="list",
        description="Lists all streamers from your watchlist"
    )
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def list(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            description="Loading answer...",
            color=disnake.Color.blurple()
        )
        await interaction.edit_original_message(
            embed=loading_embed
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

    @twitch.sub_command_group(
        name="pingrole",
        description="Set the role which should get pinged when a streamer goes live"
    )
    async def pingrole(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        pass

    @pingrole.sub_command(
        name="add",
        description="Set the role which should get pinged when a streamer goes live"
    )
    async def _add(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        role: disnake.Role
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/guild.json", "r", encoding="UTF-8") as file:
            guild_data = json.load(file)

        if role.id in guild_data[str(interaction.guild.id)]["twitch_ping_role"]:
            embed = disnake.Embed(
                description=f"{interaction.author.mention}",
                color=disnake.Color.red()
            )
            embed.add_field(
                name="__Role already in list!__",
                value="This role is already in the list!",
                inline=False
            )
            await interaction.edit_original_message(
                embed=embed
            )
        else:
            guild_data[str(interaction.guild.id)]["twitch_ping_role"].append(role.id)

            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            embed = disnake.Embed(
                description=f"{interaction.author.mention} the role `{role.name}` is now set as ping role!",
                color=disnake.Color.blurple()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @pingrole.sub_command(
        name="remove",
        description="Remove the role which should get pinged when a streamer goes live"
    )
    async def _remove(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        role: disnake.Role
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/guild.json", "r", encoding="UTF-8") as file:
            guild_data = json.load(file)

        if role.id in guild_data[str(interaction.guild.id)]["twitch_ping_role"]:

            guild_data[str(interaction.guild.id)]["twitch_ping_role"].remove(role.id)

            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            embed = disnake.Embed(
                description=f"{interaction.author.mention} the role `{role.name}` is now removed as ping role!",
                color=disnake.Color.blurple()
            )
            await interaction.edit_original_message(
                embed=embed
            )
        else:
            embed = disnake.Embed(
                description=f"{interaction.author.mention} the role `{role.name}` is not set as ping role!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @pingrole.sub_command(
        name="list",
        description="Lists all roles which should get pinged when a streamer goes live"
    )
    async def _list(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/guild.json", "r", encoding="UTF-8") as file:
            guild_data = json.load(file)

        if guild_data[str(interaction.guild.id)]["twitch_ping_role"]:
            embed = disnake.Embed(
                description=f"{interaction.author.mention} the ping role from {interaction.guild.name}",
                color=disnake.Color.blurple()
            )
            role_list = []
            for role in guild_data[str(interaction.guild.id)]["twitch_ping_role"]:
                role_list.append(f"<@&{role}>")

            embed.add_field(
                name="__Role__",
                value="\n".join(role_list),
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
                name="__Ping role is empty!__",
                value="There wasnt added a ping role till now!",
                inline=False
            )
            await interaction.edit_original_message(
                embed=embed
            )

    # TODO: add options to get only a few part of the embed such as viewers, game, title, etc.
    # TODO: add commands to add those options
    @loop(seconds=300)
    async def check_streams(self):
        await self.bot.wait_until_ready()

        print(f"{colorama.Fore.BLUE} [TWITCH UPDATE] [TASK] Starting file update... {colorama.Fore.RESET}")
        update_streams()
        print(f"{colorama.Fore.BLUE} [TWITCH UPDATE] [DONE] Finished updating files! {colorama.Fore.RESET}")

        print(f"{colorama.Fore.LIGHTMAGENTA_EX} [TWITCH NOTIFICATION] [TASK] Checking twitch streams...{colorama.Fore.RESET}")

        online_users = []
        notifications = 0

        # load json files and setup local variables=

        with open("json/watchlist.json", "r", encoding="UTF-8") as file:
            watchlist_data: dict = json.load(file)

        with open("json/twitch_updates.json", "r", encoding="UTF-8") as twitch_file:
            twitch_data: dict = json.load(twitch_file)

        with open("json/settings.json", "r", encoding="UTF-8") as settings_file:
            settings_data: dict = json.load(settings_file)

        with open("json/guild.json", "r", encoding="UTF-8") as file:
            for guild in json.load(file).values():
                # ! print(f"{colorama.Fore.MAGENTA} -----------------------------------------------------: {i['server_name']} [{i['notify_channel']}] {colorama.Fore.RESET}")
                if guild["twitch_notifications"] == "on":

                    # with open("json/settings.json", "r", encoding="UTF-8") as file:
                    # for o in json.load(file).values():

                    # !! print(f"{colorama.Fore.MAGENTA} {i['watchlist']} {colorama.Fore.RESET}")
                    # !! print(f"{colorama.Fore.BLUE} [TWITCH] [PENDING] [2] Going through guilds... {colorama.Fore.RESET}")

                    # get all streamers from watchlist
                    users = get_users(watchlist_data["overall_watchlist"])
                    streams = get_streams(users)

                    # check if any streamer of the watchlist is live
                    if streams:
                        # !! print(f"{colorama.Fore.BLUE} [TWITCH] [PENDING] [3] Check for streams... {colorama.Fore.RESET}")

                        # for logging purposes
                        # !! print('---------------------------------------------------------------------------------')
                        # !! print(f"Online User List: {online_users}")
                        # !! print('---------------------------------------------------------------------------------')

                        # go through all streams
                        for stream in streams.values():
                            # !! print(f"{colorama.Fore.LIGHTYELLOW_EX} [TWITCH] [DATA] [!] {stream['user_login']} is live! {colorama.Fore.RESET}")
                            # !! print(f"{colorama.Fore.BLUE} [TWITCH] [PENDING] [4] Check if streamer is in watchlist... , '{stream['user_login']}' {colorama.Fore.RESET}")

                            # check if streamer is in not in watchlist, and if so, break and do nothing
                            if stream["user_login"] not in guild['watchlist']:
                                continue
                                # !! print(f"{colorama.Fore.LIGHTRED_EX} [TWITCH] [ERROR] [5] Streamer not in watchlist... , '{stream['user_login']}' {colorama.Fore.RESET}")
                                # print()
                            else:
                                # check if streamer is in watchlist and if so, create embed and send it to channel
                                if stream["user_login"] in guild['watchlist']:

                                    notification = []
                                    for user_name in watchlist_data["overall_watchlist"]:

                                        # for logging purposes
                                        # ! print(stream["user_login"])
                                        # ! print(user_name)

                                        # check if streamer is in streams and in local variable
                                        if user_name in streams:  # ! and user_name not in online_users:
                                            # convert time to readable format
                                            giga_time = datetime.strptime(streams[user_name]['started_at'], "%Y-%m-%dT%H:%M:%SZ")
                                            # convert time aswell to readable format
                                            started_at = time.mktime(giga_time.timetuple()) + giga_time.microsecond / 1E6
                                            # check if username is the streamer, which get asked for
                                            print(f"{colorama.Fore.LIGHTGREEN_EX} [TWITCH NOTIFICATION] [CHECK] {time.time() - started_at, user_name} {colorama.Fore.RESET}")
                                            if user_name == stream["user_login"]:
                                                # check if stream is too long in past !LIMTIT MIGHT BE 7800 but not sure
                                                if time.time() - started_at < 9000:

                                                    # ! if not bool(twitch_data[user_name][str(guild)]["sended"]):
                                                    # if so append streamer to list, so its not sent again
                                                    notification.append(streams[user_name])
                                                    online_users.append(user_name)

                                                    print(f"{colorama.Fore.GREEN} [TWITCH] [SUCCESS] [5] Stream found... , {user_name} {colorama.Fore.RESET}")
                                                    # catch exception if channel is not found
                                                    try:
                                                        # check if channel is set
                                                        if guild["notify_channel"]:
                                                            # check if streamer is in twitch_updates.json
                                                            if twitch_data[stream['user_login']]:
                                                                # get the channel
                                                                notify_channel = await self.bot.fetch_channel(guild["notify_channel"])

                                                                # create the structure from the embed
                                                                embed = disnake.Embed(
                                                                    title=f"{stream['title']}",
                                                                    color=disnake.Color.purple(),
                                                                    url=f"https://www.twitch.tv/{stream['user_login']}"
                                                                )
                                                                # add a field for basic information for the stream
                                                                embed.add_field(
                                                                    name="__Information__",
                                                                    value=f"**Streamer**: `{stream['user_name']}`\n"
                                                                        f"**Game**: `{stream['game_name']}`\n",
                                                                        inline=False
                                                                )

                                                                if settings_data[guild['server_id']]["twitch_with_viewer"]:
                                                                    embed.add_field(
                                                                        name="__Viewer__",
                                                                        value=f"**Viewer**: `{stream['viewer_count']}`",
                                                                        inline=False
                                                                    )
                                                                # add a field for the times which get displayed

                                                                embed.add_field(
                                                                    name="__Durations__",
                                                                    value=f"`Started`: {disnake.utils.format_dt(twitch_data[stream['user_login']][guild['server_id']]['started_at'], style='R')}",
                                                                    inline=False
                                                                )
                                                                # set the author a twitch icon and url for twitch streamer
                                                                embed.set_author(
                                                                    name=stream["user_name"],
                                                                    icon_url=twitch_data[stream['user_login']][guild['server_id']]["profile_pic"],
                                                                    url=f"https://www.twitch.tv/{stream['user_login']}"
                                                                )
                                                                # set the thumbnail to the streamer profile picture
                                                                embed.set_thumbnail(
                                                                    url=f"https://static-cdn.jtvnw.net/ttv-boxart/{stream['game_id']}-120x120.jpg"
                                                                )
                                                                
                                                                # set the image to the stream thumbnail
                                                                # ?state={datetime.datetime.now(tz=None).timestamp()} is used to get the preview image from the stream in real time
                                                                # so there will be displayed the newest thumbnail
                                                                embed.set_image(
                                                                    url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{stream['user_login']}-1920x1080.jpg?state={datetime.now(tz=None).timestamp()}"
                                                                )
                                                                # a little advertisement for my bot
                                                                embed.set_footer(
                                                                    text="Live Notifications by Lays Bot",
                                                                    icon_url=self.bot_png
                                                                )

                                                                # send embed to channel
                                                                # !! print(f"{colorama.Fore.GREEN} [TWITCH] [SUCCESS] [6] Sending message... , '{user_name}' {colorama.Fore.RESET}")
                                                                try:
                                                                    if bool(twitch_data[stream['user_login']][guild['server_id']]['sended']) is False:
                                                                        role_list = []
                                                                        for role in guild["twitch_ping_role"]:
                                                                            role_list.append(f"<@&{role}>")
                                                                        notifications += 1
                                                                        message: disnake.Message = await notify_channel.send(
                                                                            f"{' '.join(role_list)} " if guild["twitch_with_everyone_or_pingrole"] == "pingrole" else f"@everyone \n{' '.join(role_list)}" if guild["twitch_with_everyone_or_pingrole"] == "everyone_and_pingrole" else "@everyone" if guild["twitch_with_everyone_or_pingrole"] == "everyone" else "",
                                                                            embed=embed
                                                                        )

                                                                        twitch_data[stream["user_login"]][guild["server_id"]]["message_id"] = message.id
                                                                        twitch_data[stream["user_login"]][guild["server_id"]]["sended"] = True
                                                                        with open("json/twitch_updates.json", "w", encoding='UTF-8') as f:
                                                                            json.dump(twitch_data, f, indent=4)
                                                                    else:
                                                                        continue

                                                                except Exception as e:
                                                                    # !! print(f"{colorama.Fore.RED} [TWITCH] [ERROR] [7] Error while sending : {e} {colorama.Fore.RESET}")
                                                                    error_embed = disnake.Embed(
                                                                        title=f"Error while sending {user_name} stream notification",
                                                                        description=f"{e}",
                                                                        color=disnake.Color.red()
                                                                    )
                                                                    error_channel = await self.bot.fetch_channel(self.error_channel)
                                                                    await error_channel.send(
                                                                        embed=error_embed
                                                                    )
                                                            else:
                                                                print(f"{colorama.Fore.RED} [TWITCH] [ERROR] [8] No data for {user_name} {colorama.Fore.RESET}")
                                                        else:
                                                            continue
                                                            # if there's not a channel, do nothing
                                                            # !! print(f"{colorama.Fore.RED} [TWITCH] [ERROR] [7] No channel found... , '{i['server_name']}' {colorama.Fore.RESET}")
                                                    except KeyError as e:
                                                        print("KeyError: ", e)
                                                        continue
                                                    # !else:
                                                        # ! continue
                                                        # if the stream already have been sended, -> value sended is True
                                                else:
                                                    continue
                                                    # if stream is too long inthe past, do nothing
                                                    # !! print(f"{colorama.Fore.RED} [TWITCH] [ERROR] [6] Timeout: Stream started too long ago... , '{user_name}' {colorama.Fore.RESET}")
                                            else:
                                                continue
                                                # !! print(f"{colorama.Fore.RED} [TWITCH] [ERROR] [6] Wrong streamer name... [given: '{user_name}' | required: '{stream['user_login']}'] {colorama.Fore.RESET}")
                                                # if anything else happend, do nothing
                                        else:
                                            continue
                                            # !! print(f"{colorama.Fore.RED} [TWITCH] [ERROR] [5] Not in streams... , '{user_name}' {colorama.Fore.RESET}")
                                else:
                                    continue
                    else:
                        continue
                        # if no streamer is live, do nothing
                        # !! print(f"{colorama.Fore.RED} [TWITCH] [ERROR] [3] No streams found... {colorama.Fore.RESET}")
                else:
                    continue
                    # if there's no streamer, do nothing
                    # !! print(f"{colorama.Fore.RED} [TWITCH] [ERROR] [2] Server hasn't set notification channel or watchlist ... {colorama.Fore.RESET}")

        print(f"{colorama.Fore.LIGHTMAGENTA_EX} [TWITCH NOTIFICATION] [DONE] Finished with [{notifications}] notifications! {colorama.Fore.RESET}")

    @loop(minutes=15)
    async def update(self):
        await self.bot.wait_until_ready()

        print(f"{colorama.Fore.BLUE} [TWITCH UPDATE] [TASK] Starting message update... {colorama.Fore.RESET}")

        with open("json/twitch_updates.json", "r", encoding='UTF-8') as f:
            twitch_data = json.load(f)
        with open("json/guild.json", "r", encoding='UTF-8') as f:
            guild_data = json.load(f)
        with open("json/settings.json", "r", encoding='UTF-8') as f:
            settings_data = json.load(f)

        # create copy to use data from file and make changes
        twitch_data_copy = copy.copy(twitch_data)

        # loop through all streamer in the json file
        for streamer in twitch_data_copy:
            # ! print("Streamer: ", streamer)
            # loop through all servers in the json file from the streamer
            for server in twitch_data_copy[streamer]:
                # ! print("Server: ", server)
                # check if the server has twitch notification enabled
                if guild_data[server]["twitch_notifications"] == "on":
                    # ! print(f"{server} has twitch notifications enabled")
                    # check if a message_id and a notificaion channel are set
                    if twitch_data_copy[streamer][server]["message_id"] is not None and guild_data[server]["notify_channel"] is not None:
                        # ! print(f"{server} has a message_id and a notification channel set")
                        twitch_data_copy[streamer][server]["last_update"] = datetime.now(tz=None).timestamp()

                        # check if status from the streamer is live or offline
                        if twitch_data_copy[streamer][server]["status"] == "offline":

                            # get the message as object
                            channel: disnake.TextChannel = await self.bot.fetch_channel(twitch_data_copy[streamer][server]["channel_id"])
                            message: disnake.Message = channel.get_partial_message(twitch_data_copy[streamer][server]["message_id"])
                            newline = '\n'
                            gamelist = []

                            started_date = datetime.fromtimestamp(twitch_data_copy[streamer][server]["started_at"])
                            ended_date = datetime.fromtimestamp(twitch_data_copy[streamer][server]["ended_at"])

                            # create time differnce between start and end
                            raw_time_difference = ended_date - started_date
                            # convert time difference to string
                            without_end_time_difference = str(raw_time_difference).split('.')[0]
                            # split time difference into days, hours, minutes and seconds
                            # ! EXAMPLE : 5 days, 7:22:48
                            # check if there are days in the time difference
                            hours = without_end_time_difference.split(":")[0]
                            minutes = without_end_time_difference.split(":")[1]
                            seconds = without_end_time_difference.split(":")[2]

                            # check if there are days in the time difference
                            # if so split it into days, hours, minutes and seconds
                            if "days" in without_end_time_difference or "day" in without_end_time_difference:
                                days = without_end_time_difference.split(",")[0].split(" ")[0]
                                hours = without_end_time_difference.split(",")[1].split(":")[0].strip()
                                minutes = without_end_time_difference.split(":")[1]
                                seconds = without_end_time_difference.split(":")[2]
                                day_string = f"{days}d {hours}h {minutes}m {seconds}s"
                            else:
                                day_string = f"{hours}h {minutes}m {seconds}s"

                            # loop through all games which were played and add them to a list
                            for game in twitch_data_copy[streamer][server]["game_list"]:
                                gamelist.append(f"- `{game}`")

                            # create embed
                            embed = disnake.Embed(
                                title="Stream is offline",
                                # !! url=f"https://www.twitch.tv/{streamer}",
                                color=disnake.Color.purple()
                            )

                            # set author to the streamer and add a link to the streamer aswell as a profile picture
                            embed.set_author(
                                name=streamer,
                                icon_url=twitch_data_copy[streamer][server]["profile_pic"],
                                url=f"https://www.twitch.tv/{streamer}"
                            )

                            # add a field for the streams information
                            embed.add_field(
                                name="__Information__",
                                value=f"**Streamer**: `{twitch_data_copy[streamer][server]['user_name']}`\n"
                                      f"**Games played**: {newline}{f'{newline}'.join(gamelist)}\n",
                                      # !! f"**Games played**: {newline}`{f'{newline}- '.join(twitch_data_copy[streamer][server]['game_list'] if twitch_data_copy[streamer][server]['game_list'] else twitch_data_copy[streamer][server]['game_name'])}`\n",
                                inline=False
                            )
                            if settings_data[server]["twitch_with_viewer"]:
                                embed.add_field(
                                    name="__Viewer__",
                                    value=f"**Average Viewer**: `{averageCalculation(twitch_data_copy[streamer][server]['viewer_count_list'])}`",
                                    inline=False
                                )

                            # add a field for the streams duration
                            embed.add_field(
                                name="__Durations__",
                                value=f"`Started`: {disnake.utils.format_dt(twitch_data_copy[streamer][server]['started_at'], style='F')}\n"
                                      f"`Ended`: {disnake.utils.format_dt(twitch_data_copy[streamer][server]['ended_at'], style='F')}\n"
                                      f"`Duration`: `{day_string}`",
                                inline=False
                            )
                            embed.set_thumbnail(
                                url=twitch_data_copy[streamer][server]["profile_pic"]
                            )
                            embed.set_footer(
                                text="Live Notifications by Lays Bot",
                                icon_url=self.bot_png
                            )

                            await message.edit(
                                embed=embed
                            )

                            # only to set the settings back (is more data traffic)
                            # !! twitch_data[streamer][server]["message_id"] = None
                            # !! twitch_data[streamer][server]["game_list"] = []

                            # to delete the data -> less data traffic
                            try:
                                print(f"Deleting data for {streamer} in {server} (offline)")
                                del twitch_data[streamer]
                                with open("json/twitch_updates.json", "w", encoding='UTF-8') as f:
                                    json.dump(twitch_data, f, indent=4)
                                print(f"Deleting data for {streamer} in {server} (offline) - DONE")
                                
                            except KeyError:
                                print("KeyError, there is no file to delete")
                        else:
                            # ! print(f"{colorama.Fore.GREEN} [TWITCH UPDATE] [SUCCESS] Updating message for {streamer} in {server}! {colorama.Fore.RESET}")
                            try:
                                
                                # define variables
                                channel: disnake.TextChannel = await self.bot.fetch_channel(twitch_data[streamer][server]["channel_id"])
                                message: disnake.Message = channel.get_partial_message(twitch_data[streamer][server]["message_id"])

                                newline = "\n"

                                # ! print(f"{colorama.Fore.GREEN} [TWITCH UPDATE] [SUCCESS] Creating embed for {streamer}! {colorama.Fore.RESET}")
                                # create the structure from the embed
                                embed = disnake.Embed(
                                    title=f"{twitch_data[streamer][server]['title']}",
                                    color=disnake.Color.purple(),
                                    url=f"https://www.twitch.tv/{streamer}"
                                )
                                # add a field for basic information for the stream
                                embed.add_field(
                                    name="__Information__",
                                    value=f"**Streamer**: `{twitch_data_copy[streamer][server]['user_name']}`\n"
                                            # f"**Viewer**: `{twitch_data_copy[streamer][server]['viewer_count']}`{newline}" if settings_data[server]['twitch_with_viewer'] else ''
                                          f"**Game**: `{twitch_data[streamer][server]['game_name']}`\n",
                                        inline=False
                                )

                                if settings_data[server]["twitch_with_viewer"]:
                                    embed.add_field(
                                        name="__Viewer__",
                                        value=f"**Viewer**: `{twitch_data_copy[streamer][server]['viewer_count']}`",
                                        inline=False
                                    )
                                # add a field for the times which get displayed
                                embed.add_field(
                                    name="__Durations__",
                                    value=f"`Started`: {disnake.utils.format_dt(twitch_data[streamer][server]['started_at'], style='R')}\n"
                                          f"`Last Update`: {disnake.utils.format_dt(twitch_data[streamer][server]['last_update'], style='R')}",
                                    inline=False
                                )
                                # set the author a twitch icon and url for twitch streamer
                                embed.set_author(
                                    name=streamer,
                                    icon_url=twitch_data_copy[streamer][server]["profile_pic"],
                                    url=f"https://www.twitch.tv/{streamer}"
                                )
                                # set the thumbnail to the streamer profile picture
                                embed.set_thumbnail(
                                    url=f"https://static-cdn.jtvnw.net/ttv-boxart/{twitch_data_copy[streamer][server]['game_id']}-120x120.jpg"
                                )
                                
                                # set the image to the stream thumbnail
                                # ?state={datetime.datetime.now(tz=None).timestamp()} is used to get the preview image from the stream in real time
                                # so there will be displayed the newest thumbnail
                                embed.set_image(
                                    url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{streamer}-1920x1080.jpg?state={datetime.now(tz=None).timestamp()}"
                                )
                                # a little advertisement for my bot
                                embed.set_footer(
                                    text="Live Notifications by Lays Bot",
                                    icon_url=self.bot_png
                                )
                                # and at its final edit the message
                                await message.edit(
                                    embed=embed
                                )
                                # ! print(f"{colorama.Fore.GREEN} [TWITCH UPDATE] [SUCCESS] Message updated for {streamer}! {colorama.Fore.RESET}")

                            except Exception as e:

                                print(f"{colorama.Fore.RED} [TWITCH UPDATE] [ERROR] Error while updating : {e} {colorama.Fore.RESET}")
                                error_embed = disnake.Embed(
                                    title=f"Error while updating {streamer} stream notification",
                                    description=f"{e}",
                                    color=disnake.Color.red()
                                )
                                error_channel = await self.bot.fetch_channel(self.error_channel)
                                await error_channel.send(
                                    embed=error_embed
                                )
                    else:
                        # remove the data from the json file
                        try:
                            # delete streamer from the json file
                            # ! print(f"Deleting data for {streamer} in {server} (offline)")
                            del twitch_data[streamer]
                            # save the json file
                            with open("json/twitch_updates.json", "w", encoding='UTF-8') as f:
                                json.dump(twitch_data, f, indent=4)
                            # ! print(f"Deleting data for {streamer} in {server} (offline) - DONE")

                            # check if the server is a beta server and has the viewer graph enabled
                            if guild_data[server]["beta_server"]:
                                # delete the viewer graph if it has
                                os.remove(f"viewerGraph-{twitch_data_copy[streamer][server]['user_name']}.png")
                            
                        except KeyError:
                            print("KeyError, there is no file to delete")
                        # ! print(f"{colorama.Fore.RED} [TWITCH UPDATE] [ERROR] No message and no channel found... , '{streamer}' {colorama.Fore.RESET}")
                else:
                    continue
        print(f"{colorama.Fore.BLUE} [TWITCH UPDATE] [DONE] Finished updating messages! {colorama.Fore.RESET}")

        # TODO create function, that updates the embed as long as the streamer is live
        # TODO store the message in a json file, so it can be used later (for every streamer and server)
        # ! EXAMPLE:
        # streamer_name = {
        #     guild_id: {
        #         message_id: message_id
        #     },
        #     guild_id: {
        #         message_id: message_id
        #     }
        # TODO what to update? - title, viewer count, game name, time

        # Idea 1 [WhILE LIVE]
        """
        embed = disnake.Embed(
            title=f"{twitch_data[streamer][server]['title']}",
            color=disnake.Color.purple(),
            url=f"https://www.twitch.tv/{streamer}"
        )
        embed.add_field(
            name="Stream Information",
            value=f"**Streamer**: `{twitch_data[streamer][server]['user_name']}`\n"
                    f"**Viewer**: `{twitch_data[streamer][server]['viewer_count']}`\n"
                    f"**Game**: `{twitch_data[streamer][server]['game_name']}`\n",
            inline=False
        )
        embed.add_field(
            name="Durations",
            value=f"`Started`: {disnake.utils.format_dt(twitch_data[streamer][server]['started_at'], style='R')}\n"
                    f"`Last Update`: {disnake.utils.format_dt(twitch_data[streamer][server]['last_update'], style='R')}",
            inline=False
        )
        embed.set_author(
            name="Twitch Notification",
            icon_url=twitch_data_copy[streamer][server]["profile_pic"],
        )
        embed.set_thumbnail(url=twitch_data_copy[streamer][server]["profile_pic"])
        embed.set_image(
            url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{streamer}-1920x1080.jpg"
        )
        embed.set_footer(
            text="Live Notifications by Lays Bot"
        )
        """
        # Idea 2 [WHILE LIVE]
        """
        embed = disnake.Embed(
            title=f"{twitch_data[streamer][server]['title']}",
            color=disnake.Color.purple(),
            url=f"https://www.twitch.tv/{streamer}"
        )
        embed.add_field(
            name="Stream Information",
            value=f"**Streamer**: `{twitch_data[streamer][server]['user_name']}`\n"
                    f"**Viewer**: `{twitch_data[streamer][server]['viewer_count']}`\n"
                    f"**Game**: `{twitch_data[streamer][server]['game_name']}`\n",
            inline=False
        )
        embed.add_field(
            name="Durations",
            value=f"`Started`: {disnake.utils.format_dt(twitch_data[streamer][server]['started_at'], style='R')}\n"
                    f"`Last Update`: {disnake.utils.format_dt(twitch_data[streamer][server]['last_update'], style='R')}",
            inline=False
        )
        embed.set_author(
            name="Twitch Notification",
            icon_url="https://cdn.discordapp.com/attachments/920072174247751690/972897521745682472/unknown.png",
        )
        embed.set_image(
            url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{streamer}-1920x1080.jpg"
        )
        embed.set_footer(
            text="Live Notifications by Lays Bot"
        )
        """


def setup(bot: commands.Bot):
    bot.add_cog(Twitch(bot))
