import json
from datetime import datetime

import disnake
from disnake.ext import commands
from disnake.ext.tasks import loop

from utils.youtube import (check_title, convert_usernamne_to_id,
                           get_latest_videos, is_short)


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot: disnake.Client = bot
        self.youtube.start()

    @loop(seconds=1800)
    async def youtube(self):
        # open json file
        with open("json/youtube.json", "r") as data_file:
            data: dict = json.load(data_file)

        with open("json/guild.json", "r") as data_file:
            guild: dict = json.load(data_file)
        
        # catch all errors
        try:
            # check if data is not empty
            if data:
                print(data)
                # get every entry
                for youtuberName in data:
                    print(youtuberName)
                    # check if entry is not empty
                    if youtuberName:
                        # get every guild in data
                        for discordServer in data[youtuberName]:
                            print(discordServer)
                            # check if data is in the guild
                            if discordServer:
                                if youtuberName in guild[discordServer]["youtube-watchlist"]:
                                    print(f"{youtuberName} is in {discordServer} watchlist")
                                    # define basic variables
                                    phrase = data[youtuberName][discordServer]["phrase"]
                                    checkTime = data[youtuberName][discordServer]["checkTime"]
                                    
                                    # define other variables
                                    publishedAt = data[youtuberName][discordServer][youtuberName]["publishedAt"]
                                    # title = data[youtuberName][discordServer]["videoTitle"]
                                    # thumbnail = data[youtuberName][discordServer]["thumbnail"]
                                    # videoId = data[youtuberName][discordServer]["videoId"]
                                    channelId = convert_usernamne_to_id(data[youtuberName][discordServer][youtuberName]["channelName"])

                                    # get latest video
                                    newVideo = get_latest_videos(channelId)
                                    newVideoId = newVideo[0]["id"]["videoId"]
                                    newPublishedAt = newVideo[0]["snippet"]["publishedAt"]

                                    # check if video is short and if the title contains the phrase
                                    if is_short(newVideoId, checkTime) or check_title(newVideoId, phrase):
                                        print("video is short or the title contains the phrase")
                                        # video is short or the title contains the phrase
                                        # therefore there is no new video
                                        pass
                                    else:
                                        print("video is not short and the title doesnt contain the phrase")
                                        # video is not short and the title doesnt contain the phrase
                                        # therefore there is a new video
                                        
                                        # check if video is already in the json file
                                        if newVideoId not in data:
                                            print("video is not in the json file")
                                            # video is not in the json file
                                            # therefore there is a new video
                                            # to double check if there is a new video -> compare the publishedAt date

                                            timestamp1 = publishedAt
                                            timestamp2 = newPublishedAt

                                            oldTimeStamp = datetime.strptime(timestamp1, "%Y-%m-%dT%H:%M:%SZ")
                                            newTimeStamp = datetime.strptime(timestamp2, "%Y-%m-%dT%H:%M:%SZ")

                                            # check if the publishedAt date is the same
                                            if oldTimeStamp != newTimeStamp:
                                                print("oldTimeStamp is not the same as newTimeStamp")
                                                if oldTimeStamp < newTimeStamp:
                                                    print("oldTimeStamp is older than newTimeStamp")
                                                    # oldTimeStamp is older than newTimeStamp
                                                    # therefore there is a new video

                                                    # clear the json file
                                                    data[youtuberName][discordServer][youtuberName] = {}

                                                    # write to json file
                                                    with open("json/youtube.json", "w") as data_file:
                                                        json.dump(data, data_file, indent=4)

                                                    # define variables
                                                    data: dict = data

                                                    # add video to json file
                                                    data[youtuberName][discordServer][youtuberName] = {}
                                                    data[youtuberName][discordServer][youtuberName]["publishedAt"] = newVideo[0]["snippet"]["publishedAt"]
                                                    data[youtuberName][discordServer][youtuberName]["videoTitle"] = newVideo[0]["snippet"]["title"]
                                                    data[youtuberName][discordServer][youtuberName]["thumbnail"] = newVideo[0]["snippet"]["thumbnails"]["high"]["url"]
                                                    data[youtuberName][discordServer][youtuberName]["videoId"] = newVideoId
                                                    data[youtuberName][discordServer][youtuberName]["channelName"] = data[youtuberName][discordServer]["channelName"]

                                                    # write to json file
                                                    with open("json/youtube.json", "w") as data_file:
                                                        json.dump(data, data_file, indent=4)
                                                else:
                                                    print("oldTimeStamp is newer than newTimeStamp")
                                                    # oldTimeStamp is newer than newTimeStamp
                                                    # therefore there is no new video
                                                    pass
                                            else:
                                                print("oldTimeStamp is the same as newTimeStamp")
                                                # oldTimeStamp is the same as newTimeStamp
                                                # therefore there is no new video
                                                pass
                                        else:
                                            print("video is in the json file")
                                            # video is in the json file
                                            # there is no new video
                                            pass
                                else:
                                    print(f"{youtuberName} is not in the guild youtube watchlist")
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

def setup(bot):
    bot.add_cog(Youtube(bot))
