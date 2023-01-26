import json
from datetime import datetime
import codecs
import colorama

import disnake
from disnake.ext import commands
from disnake.ext.tasks import loop

from utils.youtube import (check_title, convert_usernamne_to_id,
                           get_latest_videos, is_short)


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot: disnake.Client = bot

        self.check_videos.start()

    @loop(seconds=1800)
    async def check_videos(self):
        await self.bot.wait_until_ready()

        print(f"{colorama.Fore.LIGHTMAGENTA_EX} [YOUTUBE NOTIFICATION] [TASK] Checking youtube videos...{colorama.Fore.RESET}")

        # open json file
        with codecs.open("json/youtube.json", "r", encoding="utf-8") as data_file:
            data: dict = json.load(data_file)

        with open("json/guild.json", "r", encoding="utf-8") as data_file:
            guild: dict = json.load(data_file)
        
        # catch all errors
        try:
            # check if data is not empty
            if data:
                # get every entry
                for youtuberName in data:
                    # check if entry is not empty
                    if youtuberName:
                        # get every guild in data
                        for discordServer in data[youtuberName]:
                            print(discordServer)
                            # check if data is in the guild
                            if discordServer:
                                if youtuberName in guild[str(discordServer)]["youtubeWatchlist"]:
                                    print('youtuber is in guild')
                                    if youtuberName in data[youtuberName][str(discordServer)]:
                                        print('youtuber is in data for guild')
                                        # define basic variables
                                        phrase = data[youtuberName][discordServer]["phrase"]
                                        checkTime = data[youtuberName][discordServer]["checkTime"]
                                        
                                        # define other variables
                                        publishedAt = data[youtuberName][discordServer][youtuberName]["publishedAt"]
                                        # title = data[youtuber][discordServer]["videoTitle"]
                                        # thumbnail = data[youtuber][discordServer]["thumbnail"]
                                        # videoId = data[youtuber][discordServer]["videoId"]
                                        channelId = convert_usernamne_to_id(data[youtuberName][discordServer][youtuberName]["channelName"])

                                        # get latest video
                                        newVideo = get_latest_videos(channelId)
                                        newVideoId = newVideo[0]["id"]["videoId"]
                                        newPublishedAt = newVideo[0]["snippet"]["publishedAt"]

                                        # check if video is short and if the title contains the phrase
                                        if is_short(newVideoId, checkTime) or check_title(newVideoId, phrase):
                                            # video is short or the title contains the phrase
                                            # therefore there is no new video
                                            pass
                                        else:
                                            # video is not short and the title doesnt contain the phrase
                                            # therefore there is a new video
                                            
                                            # check if video is already in the json file
                                            if newVideoId not in data:
                                                # video is not in the json file
                                                # therefore there is a new video
                                                # to double check if there is a new video -> compare the publishedAt date

                                                timestamp1 = publishedAt
                                                timestamp2 = newPublishedAt

                                                oldTimeStamp = datetime.strptime(timestamp1, "%Y-%m-%dT%H:%M:%SZ")
                                                newTimeStamp = datetime.strptime(timestamp2, "%Y-%m-%dT%H:%M:%SZ")

                                                # check if the publishedAt date is the same
                                                if oldTimeStamp != newTimeStamp:
                                                    if oldTimeStamp < newTimeStamp:
                                                        # oldTimeStamp is older than newTimeStamp
                                                        # therefore there is a new video

                                                        # clear the json file
                                                        data[youtuberName][discordServer][youtuberName] = {}

                                                        # write to json file
                                                        with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                                                            json.dump(data, data_file, indent=4)

                                                        # define variables
                                                        data: dict = data

                                                        # add video to json file
                                                        data[youtuberName][discordServer][youtuberName] = {}
                                                        data[youtuberName][discordServer][youtuberName]["publishedAt"] = newVideo[0]["snippet"]["publishedAt"]
                                                        data[youtuberName][discordServer][youtuberName]["videoTitle"] = newVideo[0]["snippet"]["title"]
                                                        data[youtuberName][discordServer][youtuberName]["thumbnail"] = f"https://i3.ytimg.com/vi/{newVideoId}/maxresdefault.jpg "
                                                        data[youtuberName][discordServer][youtuberName]["videoId"] = newVideoId
                                                        data[youtuberName][discordServer][youtuberName]["channelName"] = youtuberName

                                                        # write to json file
                                                        with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                                                            json.dump(data, data_file, indent=4)

                                                        date_string = data[youtuberName][discordServer][youtuberName]["publishedAt"]
                                                        # make timestamp readable with datetime
                                                        published = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ").timestamp()

                                                        notifyEmbed = disnake.Embed(
                                                            title=data[youtuberName][discordServer][youtuberName]["videoTitle"],
                                                            url=f"https://www.youtube.com/watch?v={data[youtuberName][discordServer][youtuberName]['videoId']}",
                                                            color=disnake.Color.red()
                                                        )
                                                        notifyEmbed.add_field(
                                                            name="Uploaded",
                                                            value=disnake.utils.format_dt(datetime.fromtimestamp(published), style="F"),
                                                            inline=False
                                                        )
                                                        notifyEmbed.set_image(url=f"https://i3.ytimg.com/vi/{newVideoId}/maxresdefault.jpg")
                                                        notifyEmbed.set_author(name=f"{youtuberName} hat ein neues Video", url=f"https://www.youtube.com/channel/{channelId}")

                                                        # send notification
                                                        notificationChannel: disnake.TextChannel = await self.bot.fetch_channel(int(guild[str(discordServer)]["youtube-notificationChannel"]))

                                                        if notificationChannel:
                                                            await notificationChannel.send(content=f"@everyone {data[youtuberName][discordServer]['message']}", embed=notifyEmbed)
                                                        else:
                                                            pass
                                                    else:
                                                        # oldTimeStamp is newer than newTimeStamp
                                                        # therefore there is no new video
                                                        pass
                                                else:
                                                    # oldTimeStamp is the same as newTimeStamp
                                                    # therefore there is no new video
                                                    pass
                                            else:
                                                # video is in the json file
                                                # there is no new video
                                                pass
                                    else:
                                        print(f"Youtuber {youtuberName} is not in the json file")
                                        # add youtuber to json file
                                        # beacuse there is no data in the json file

                                        # define variables
                                        data: dict = data

                                        # add youtuber to json file
                                        data[youtuberName][discordServer] = {}
                                        data[youtuberName][discordServer]["phrase"] = ""
                                        data[youtuberName][discordServer]["checkTime"] = 60
                                        data[youtuberName][discordServer]["message"] = f"Neues Video von **{youtuberName}**"

                                        # add video to json file of youtuber and guild
                                        data[youtuberName][discordServer][youtuberName] = {}
                                        data[youtuberName][discordServer][youtuberName]["publishedAt"] = newVideo[0]["snippet"]["publishedAt"]
                                        data[youtuberName][discordServer][youtuberName]["videoTitle"] = newVideo[0]["snippet"]["title"]
                                        data[youtuberName][discordServer][youtuberName]["thumbnail"] = f"https://i3.ytimg.com/vi/{newVideoId}/maxresdefault.jpg "
                                        data[youtuberName][discordServer][youtuberName]["videoId"] = newVideoId
                                        data[youtuberName][discordServer][youtuberName]["channelName"] = youtuberName

                                        # write to json file
                                        with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                                            json.dump(data, data_file, indent=4)
                                else:
                                    # youtuber is not in the guild youtube watchlist
                                    pass
                        else:
                            # there is no data in the guild
                            pass
                else:
                    # there is no entry
                    pass
            else:
                # there is no data
                pass
        # catch error if there is no entry
        except KeyError as e:
            print(e)
        
        print(f"{colorama.Fore.LIGHTMAGENTA_EX} [YOUTUBE NOTIFICATION] [DONE] Finished checking videos! {colorama.Fore.RESET}")

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="youtube", description="Zeigt dir die neuesten Videos von einem Youtuber an")
    async def youtube(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @youtube.sub_command("add", description="Fügt einen Youtuber zur Watchlist hinzu")
    async def youtube_add(self, interaction: disnake.ApplicationCommandInteraction, youtuber: str, phrase: str = "", checktime: int = 60, message: str = ""):
        await interaction.response.defer(ephemeral=True)

        # define variables
        with open("json/youtube.json", "r", encoding="utf-8") as data_file:
            data: dict = json.load(data_file)

        with open("json/guild.json", "r", encoding="utf-8") as data_file:
            guild: dict = json.load(data_file)

        youtuber = youtuber.lower()

        try:
            # check if the youtuber is already in the guild
            if youtuber in guild[interaction.guild.id]["youtubeWatchlist"]:
                # youtuber is already in the guild
                # create embed
                embed = disnake.Embed(
                    description=f"**{youtuber}** ist bereits in der Watchlist!",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                # youtuber is not in the guild

                if youtuber in data:
                    # youtuber is in the json file
                    # add youtuber to the guild
                    guild[str(interaction.guild.id)]["youtubeWatchlist"].append(youtuber)

                    # write to json file
                    with open("json/guild.json", "w", encoding="utf-8") as data_file:
                        json.dump(guild, data_file, indent=4)

                    data[youtuber][str(interaction.guild.id)] = {}
                    data[youtuber][guild[str(interaction.guild.id)]['server_id']] = {
                        "phrase": phrase,
                        "checkTime": checktime,
                        "message": message,
                        youtuber: {
                            "publishedAt": "2000-01-01T00:00:00Z",
                            "videoTitle": "No title",
                            "thumbnail": "no thumbnail",
                            "videoId": "asdfghjkl",
                            "channelName": youtuber
                        }
                    }

                    # write to json file
                    with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                        json.dump(data, data_file, indent=4)

                    # create embed
                    embed = disnake.Embed(
                        description=f"**{youtuber}** wurde zur Watchlist hinzugefügt!",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
                else:
                    print(guild[str(interaction.guild.id)]['server_id'])
                    # make youtuber dict type
                    data[youtuber] = {}

                    data[youtuber][str(interaction.guild.id)] = {}
                    data[youtuber][guild[str(interaction.guild.id)]['server_id']] = {
                        "phrase": phrase,
                        "checkTime": checktime,
                        "message": message,
                        youtuber: {
                            "publishedAt": "2000-01-01T00:00:00Z",
                            "videoTitle": "No title",
                            "thumbnail": "no thumbnail",
                            "videoId": "asdfghjkl",
                            "channelName": youtuber
                        }
                    }

                    # write to json file
                    with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                        json.dump(data, data_file, indent=4)

                    # add youtuber to the guild
                    guild[str(interaction.guild.id)]["youtubeWatchlist"].append(youtuber)

                    #write to json file
                    with open("json/guild.json", "w", encoding="utf-8") as data_file:
                        json.dump(guild, data_file, indent=4)

                    # create embed
                    embed = disnake.Embed(
                        description=f"**{youtuber}** wurde erfolgreich zur Watchlist hinzugefügt!",
                        color=disnake.Color.green()
                    )

                    # send embed
                    await interaction.edit_original_message(
                        embed=embed
                    )
        except KeyError as _:
            embed = disnake.Embed(
                description=f"**{youtuber}** wurde nicht gefunden!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @youtube.sub_command("remove", description="Entfernt einen Youtuber zur Watchlist hinzu")
    async def youtube_remove(self, interaction: disnake.ApplicationCommandInteraction, youtuber: str):
        await interaction.response.defer(ephemeral=True)

        # define variables
        with open("json/youtube.json", "r", encoding="utf-8") as data_file:
            data: dict = json.load(data_file)

        with open("json/guild.json", "r", encoding="utf-8") as data_file:
            guild: dict = json.load(data_file)

            # check if the youtuber is already in the guild
            if str(interaction.guild.id) in data[youtuber] and youtuber in guild[str(interaction.guild.id)]["youtubeWatchlist"]:
                try:
                    # youtuber is not in the guild
                    # add youtuber to the guild
                    del data[youtuber][interaction.guild.id]

                    # write to json file
                    with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                        json.dump(data, data_file, indent=4)

                    # delete youtuber from the guild
                    guild[str(interaction.guild.id)]["youtubeWatchlist"].remove(youtuber)

                    #write to json file
                    with open("json/guild.json", "w", encoding="utf-8") as data_file:
                        json.dump(guild, data_file, indent=4)

                    # create embed
                    embed = disnake.Embed(
                        description=f"**{youtuber}** wurde erfolgreich aus der Watchlist entfernt!",
                        color=disnake.Color.green()
                    )

                    await interaction.edit_original_message(
                        embed=embed
                    )
                except KeyError as e:
                    print(e)
            else:
                # youtuber is not in the guild
                # create embed
                embed = disnake.Embed(
                    description=f"**{youtuber}** ist nicht in der Watchlist!",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )

    @youtube.sub_command("list", description="Zeigt dir die Youtuber in der Watchlist an")
    async def youtube_list(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        # define variables
        with open("json/guild.json", "r", encoding="utf-8") as data_file:
            guild: dict = json.load(data_file)

        try:
            # check if the youtuber is already in the guild
            if guild[interaction.guild.id]["youtubeWatchlist"] != []:
                # youtuber is in the guild

                youtuber_list = []
                for streamer in guild[str(interaction.guild.id)]["youtubeWatchlist"]:
                    youtuber_list.append(streamer)

                # create embed
                embed = disnake.Embed(
                    description=f"**Watchlist von {interaction.guild.name}**",
                    color=disnake.Color.green()
                )
                embed.add_field(
                    name="__Streamer__",
                    value="\n".join(youtuber_list),
                    inline=False
                )

                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                # youtuber is not in the guild
                # create embed
                embed = disnake.Embed(
                    description=f"Es sind **keine Youtuber** in der Watchlist!",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
        except KeyError as _:
            # youtuber is not in the guild
            embed = disnake.Embed(
                description=f"Es sind **keine Youtuber** in der Watchlist!",
                color=disnake.Color.red()
            )
            
            # send embed
            await interaction.edit_original_message(
                embed=embed
            )
    
    @commands.has_permissions(administrator=True)
    @youtube.sub_command_group("set", description="Überkategorie für die Einstellungen der Watchlist")
    async def youtube_set(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @youtube_set.sub_command("phrase", description="Ändert die Phrase für einen Streamer")
    async def youtube_set_phrase(self, interaction: disnake.ApplicationCommandInteraction, youtuber: str, phrase: str = None):
        await interaction.response.defer(ephemeral=True)

        # define variables
        with open("json/youtube.json", "r", encoding="utf-8") as data_file:
            data: dict = json.load(data_file)
        with open("json/guild.json", "r", encoding="utf-8") as data_file:
            guild: dict = json.load(data_file)

        youtuber = youtuber.lower()
        
        try:
            if youtuber in guild[str(interaction.guild.id)]["youtubeWatchlist"]:
                if not phrase:
                    embed = disnake.Embed(
                        description=f"Der aktuelle `Phrase` für den Youtuber `{youtuber}` ist: `{data[youtuber][str(interaction.guild.id)]['phrase']}`",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
                else:
                    data[youtuber][str(interaction.guild.id)]["phrase"] = phrase

                    # write to json file
                    with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                        json.dump(data, data_file, indent=4)

                    # create embed
                    embed = disnake.Embed(
                        description=f"Die `Phrase` für den Youtuber `{youtuber}` wurde erfolgreich geändert!",
                        color=disnake.Color.green()
                    )

                    await interaction.edit_original_message(
                        embed=embed
                    )
        except KeyError as e:
            embed = disnake.Embed(
                description=f"Der Youtuber `{youtuber}` ist nicht in der Watchlist!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )


    @youtube_set.sub_command("checktime", description="Ändert die checkTime für einen Streamer")
    async def youtube_set_phrase(self, interaction: disnake.ApplicationCommandInteraction, youtuber: str, checktime: str = None):
        await interaction.response.defer(ephemeral=True)

        # define variables
        with open("json/youtube.json", "r", encoding="utf-8") as data_file:
            data: dict = json.load(data_file)
        with open("json/guild.json", "r", encoding="utf-8") as data_file:
            guild: dict = json.load(data_file)

        youtuber = youtuber.lower()
        
        try:
            if youtuber in guild[str(interaction.guild.id)]["youtubeWatchlist"]:
                if not checktime:
                    embed = disnake.Embed(
                        description=f"Die aktuelle `checkTime` für den Youtuber `{youtuber}` sind: `{data[youtuber][str(interaction.guild.id)]['checkTime']}` Sekunden",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
                else:
                    data[youtuber][str(interaction.guild.id)]["checkTime"] = int(checktime)

                    # write to json file
                    with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                        json.dump(data, data_file, indent=4)

                    # create embed
                    embed = disnake.Embed(
                        description=f"Die `checkTime` für den Youtuber `{youtuber}` wurde erfolgreich geändert!",
                        color=disnake.Color.green()
                    )

                    await interaction.edit_original_message(
                        embed=embed
                    )
        except KeyError as e:
            embed = disnake.Embed(
                description=f"Der Youtuber `{youtuber}` ist nicht in der Watchlist!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @youtube_set.sub_command("message", description="Ändert die Nachricht für einen Streamer")
    async def youtube_set_phrase(self, interaction: disnake.ApplicationCommandInteraction, youtuber: str, message: str = None):
        await interaction.response.defer(ephemeral=True)

        # define variables
        with open("json/youtube.json", "r", encoding="utf-8") as data_file:
            data: dict = json.load(data_file)
        with open("json/guild.json", "r", encoding="utf-8") as data_file:
            guild: dict = json.load(data_file)

        youtuber = youtuber.lower()
        
        try:
            if youtuber in guild[str(interaction.guild.id)]["youtubeWatchlist"]:
                if not message:
                    embed = disnake.Embed(
                        description=f"Die aktuelle `Message` für den Youtuber `{youtuber}` ist: `{data[youtuber][str(interaction.guild.id)]['message']}`",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
                else:
                    data[youtuber][str(interaction.guild.id)]["message"] = message

                    # write to json file
                    with open("json/youtube.json", "w", encoding="utf-8") as data_file:
                        json.dump(data, data_file, indent=4)

                    # create embed
                    embed = disnake.Embed(
                        description=f"Die `Message` für den Youtuber `{youtuber}` wurde erfolgreich geändert!",
                        color=disnake.Color.green()
                    )

                    await interaction.edit_original_message(
                        embed=embed
                    )
        except KeyError as e:
            embed = disnake.Embed(
                description=f"Der Youtuber `{youtuber}` ist nicht in der Watchlist!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

def setup(bot):
    bot.add_cog(Youtube(bot))
