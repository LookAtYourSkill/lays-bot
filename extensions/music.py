import datetime

import json

import disnake
import wavelink
from disnake.ext import commands
from wavelink.ext import spotify

from checks._check_license import check_license


class Music(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        client: disnake.Client
    ):
        self.client: disnake.Client = client
        self.loop = False
        self.channel = None
        self.QUEUE_COMMAND = "/queue list"
        self.skipping = False
        self.announce = False
        self.provider = "LookAtYourSkill"
        self.avatar = "https://cdn.discordapp.com/avatars/493370963807830016/3240c970a937c1ee28b09d2da76792fe.png?size=1024"

        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        with open("etc/config.json", "r") as config_file:
            config = json.load(config_file)

        await wavelink.NodePool.create_node(
            bot=self.client,
            host=config["lavalink"]["host"],
            port=config["lavalink"]["port"],
            password=config["lavalink"]["password"],
            spotify_client=spotify.SpotifyClient(
                client_id=config["lavalink"]["spotify_client_id"],
                client_secret=config["lavalink"]["spotify_client_secret"]
            )
        )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):

        with open("json/settings.json", "r") as settings_file:
            settings_data = json.load(settings_file)

        if settings_data[str(player.guild.id)]["music_announce"] is True:

            now_playing = disnake.Embed(
                title="Now Playing",
                # track.title is with author
                description=f"``{track.title}``",
                color=0x00ff00
            )
            now_playing.add_field(
                name="Duration",
                value=f"``{str(datetime.timedelta(seconds=track.length))}``"
            )
            now_playing.add_field(
                name="Stream",
                value=f"``{'Yes' if track.is_stream is True else 'No'}``",
                inline=False
            )
            now_playing.add_field(
                name="URL",
                value=f"{track.uri}",
                inline=False
            )
            now_playing.set_footer(
                text=f"Bot provided by {self.provider}",
                icon_url=self.avatar
            )

            if settings_data[str(player.guild.id)]["music_announce_channel"] is not None:
                channel_id = settings_data[str(player.guild.id)]["music_announce_channel"]
                channel = await self.client.fetch_channel(channel_id)
                await channel.send(embed=now_playing)
        else:
            pass

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, vc: wavelink.Player, track: wavelink.Track, reason):

        with open("json/settings.json", "r") as settings_file:
            settings_data = json.load(settings_file)

        print(f"Track {track.title} ended with reason {reason}")

        # ! vc.guild.id is the guild id, where the track ended
        if settings_data[str(vc.guild.id)]["music_loop"]:
            await vc.play(track)

        elif vc.queue.is_empty:
            # await vc.stop()
            empty = disnake.Embed(
                description="There are no more tracks in the queue.\nIf you add a song use ``/music settings shuffle`` to resume the queue!",
                color=disnake.Color.red()
            )
            channel = await self.client.fetch_channel(self.channel)
            await channel.send(embed=empty)

            # await asyncio.sleep(120)
            # await vc.disconnect()

        elif reason == "FINISHED":
            # ! CASE FINISHED
            # finished song
            if vc.queue.is_empty:
                empty = disnake.Embed(
                    description="There are no more tracks in the queue.",
                    color=disnake.Color.red()
                )
                channel = await self.client.fetch_channel(self.channel)
                await channel.send(embed=empty)

            elif track.title == vc.queue[0].title:
                # same song in queue
                vc.queue.__delitem__(0)
                # removed song from queue
                nextSong = vc.queue[0]
                # next song in queue
                await vc.play(nextSong)
                # playing next song
                vc.queue.__delitem__(0)
                # removed song from queue
            # when song names are not the same
            else:
                # get new song
                nextSong = vc.queue.get()
                # play new song
                await vc.play(nextSong)

        # ! DONT TURN THOSE TWO CHECKS ON
        # when song get skipped
        # elif reason == "STOPPED":
            # ! CASE STOPPED
        #     print("[STOPPED] Song wurde gestoppt")
        #     nextSong = vc.queue[0]
        #     print(f"[STOPPED] Next song is {nextSong.title}")
        #     await vc.play(nextSong)
        #     print("[STOPPED] Song wurde abgespielt")

        # else:
            # ! CASE REPLACED
        #     vc.queue.__delitem__(0)
        #     nextSong = vc.queue[0]
        #     await vc.play(nextSong)
            # print(reason)
    @check_license()
    @commands.slash_command(
        name="play",
        description="Play a song"
    )
    async def play(self, interaction: disnake.ApplicationCommandInteraction, *, query: str):
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client if interaction.guild.voice_client else await interaction.author.voice.channel.connect(cls=wavelink.Player)

        """
        if not vc.is_connected:
            await vc.connect(interaction.author.voice.channel)
        if not vc.is_playing:
            try:
                track = await vc.node.get_tracks(f"ytsearch:{query}")
                if not track:
                    await interaction.response.send_message("No tracks found.", ephemeral=True)
                    return

                track = track[0]
                await vc.play(track)
                await interaction.response.send_message(f"Playing {track.title}", ephemeral=True)
            except wavelink.ZeroConnectedNodes:
                await interaction.response.send_message("No nodes available.", ephemeral=True)
        else:
            try:
                track = await vc.node.get_tracks(f"ytsearch:{query}")
                if not track:
                    await interaction.response.send_message("No tracks found.", ephemeral=True)
                    return

                track = track[0]
                vc.queue.put(track)
                await interaction.response.send_message(f"Added {track.title} to the queue.", ephemeral=True)
            except wavelink.ZeroConnectedNodes:
                await interaction.response.send_message("No nodes available.", ephemeral=True)
        """
        source = query
        if not vc.is_playing and vc.queue.is_empty:
            if "youtube" in source or "youtu.be" in source:
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(source, return_first=True)
                play_embed = disnake.Embed(
                    description=f":white_check_mark: | Playing [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}``",
                    color=disnake.Color.green()
                )
                play_embed.set_thumbnail(
                    url=track.thumbnail
                )
                await interaction.edit_original_message(
                    embed=play_embed
                )
                await vc.play(track)

            elif "soundcloud" in source:
                track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=source, return_first=True)

                play_embed = disnake.Embed(
                    description=f":white_check_mark: | Playing [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}``",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=play_embed
                )
                await vc.play(track)

            elif "spotify" in source:
                decoded = spotify.decode_url(source)
                if decoded and decoded['type'] is spotify.SpotifySearchType.track:
                    track = await spotify.SpotifyTrack.search(query=decoded["id"], type=decoded["type"], return_first=True)
                    await vc.play(track)

                elif decoded['type'] is spotify.SpotifySearchType.unusable:
                    bad_embed = disnake.Embed(
                        description="Invalid spotify url!",
                        color=disnake.Color.red()
                    )
                    return await interaction.edit_original_message(
                        embed=bad_embed
                    )
            else:
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(query, return_first=True)
                play_embed = disnake.Embed(
                    description=f":white_check_mark: | Playing [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}``",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=play_embed
                )
                await vc.play(track)

        else:
            if "youtube" in source or "youtu.be" in source:
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(source, return_first=True)
                vc.queue.put(track)
                queue_embed = disnake.Embed(
                    description=f":white_check_mark: | Added [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}`` to the queue",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=queue_embed
                )

            elif "soundcloud" in source:
                track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=source, return_first=True)
                vc.queue.put(track)
                queue_embed = disnake.Embed(
                    description=f":white_check_mark: | Added [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}`` to the queue",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=queue_embed
                )

            elif "spotify" in source:
                decoded = spotify.decode_url(source)
                if decoded and decoded['type'] is spotify.SpotifySearchType.track:
                    track = await spotify.SpotifyTrack.search(query=decoded["id"], type=decoded["type"], return_first=True)
                    vc.queue.put(track)
                    queue_embed = disnake.Embed(
                        description=f":white_check_mark: | Added [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}`` to the queue",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=queue_embed
                    )

                elif decoded['type'] is spotify.SpotifySearchType.unusable:
                    bad_embed = disnake.Embed(
                        description="Invalid spotify url!",
                        color=disnake.Color.red()
                    )
                    return await interaction.edit_original_message(
                        embed=bad_embed
                    )
            else:
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(query, return_first=True)
                vc.queue.put(track)
                queue_embed = disnake.Embed(
                    description=f":white_check_mark: | Added [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}`` to the queue",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=queue_embed
                )


    @check_license()
    @commands.slash_command(
        name="music",
        description="Music commands",
    )
    async def music(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @check_license()
    @music.sub_command_group(
        name="settings",
        description="Settings for the music module"
    )
    async def settings(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @check_license()
    @music.sub_command_group(
        name="modes",
        invoke_without_command=True
    )
    async def modes(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @check_license()
    @music.sub_command_group(
        name="play",
        invoke_without_command=True
    )
    async def play_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @check_license()
    @music.sub_command_group(
        name="playlist",
        invoke_without_command=True
    )
    async def play_playlist_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @check_license()
    @music.sub_command_group(
        name="stream",
        invoke_without_command=True
    )
    async def play_stream_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @check_license()
    @music.sub_command_group(
        name="queue",
        invoke_without_command=True
    )
    async def queue_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @check_license()
    @play_group.sub_command(
        name="youtube",
        description="Play a song from youtube"
    )
    async def play_youtube_song(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer()

        first_embed = disnake.Embed(
            description="Searching for song... Please wait...",
        )
        await interaction.edit_original_message(embed=first_embed)

        if interaction.author.voice is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.response.send_message(
                embed=bad_embed,
                ephemeral=True
            )
        if not interaction.guild.voice_client:
            self.channel = interaction.channel.id
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)

            track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(search, return_first=True)
            play_embed = disnake.Embed(
                description=f":white_check_mark: | Playing [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}``",
                color=disnake.Color.green()
            )
            play_embed.set_thumbnail(
                url=track.thumbnail
            )
            await interaction.edit_original_message(
                embed=play_embed
            )
            await vc.play(track)

            # embed = disnake.Embed(
            #     description="Connected to voice channel and generated voice client!\nUse the command again to play the song",
            #     color=disnake.Color.green()
            # )
            # await interaction.edit_original_message(embed=embed)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

            if vc.queue.is_empty and not vc.is_playing():
                self.channel = interaction.channel.id
                vc: wavelink.Player = interaction.guild.voice_client
                # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(search, return_first=True)
                play_embed = disnake.Embed(
                    description=f":white_check_mark: | Playing [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}``",
                    color=disnake.Color.green()
                )
                play_embed.set_thumbnail(
                    url=track.thumbnail
                )
                await interaction.edit_original_message(
                    embed=play_embed
                )
                await vc.play(track)
            else:
                vc: wavelink.Player = interaction.guild.voice_client
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(search, return_first=True)
                # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                await vc.queue.put_wait(track)

                queue_embed = disnake.Embed(
                    # ! in track.title is author within
                    description=f":white_check_mark: | Added ``{track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue!",
                    # Check queue with ``{self.QUEUE_COMMAND}``",
                    # description=f":white_check_mark: | Queued ``[{track.author} - {track.title}]({track.uri})``",
                    color=disnake.Color.green()
                )
                queue_embed.set_thumbnail(
                    url=track.thumbnail
                )
                await interaction.edit_original_message(
                    embed=queue_embed
                )

    @play_group.sub_command(
        name="soundcloud",
        description="Play a song from soundcloud"
    )
    async def play_soundcloud_song(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer()

        first_embed = disnake.Embed(
            description="Searching for song..."
        )
        await interaction.edit_original_message(embed=first_embed)

        if interaction.author.voice is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        if not interaction.guild.voice_client:
            self.channel = interaction.channel.id
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)

            track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
            # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
            play_embed = disnake.Embed(
                description=f":white_check_mark: | Playing [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}``",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=play_embed
            )
            await vc.play(track)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

            if vc.queue.is_empty and not vc.is_playing():
                self.channel = interaction.channel.id
                vc: wavelink.Player = interaction.guild.voice_client
                track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
                # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                play_embed = disnake.Embed(
                    description=f":white_check_mark: | Playing [{track.title}]({track.uri}) - ``{str(datetime.timedelta(seconds=track.length))}``",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=play_embed
                )
                await vc.play(track)
            else:
                vc: wavelink.Player = interaction.guild.voice_client
                # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
                await vc.queue.put_wait(track)

                queue_embed = disnake.Embed(
                    description=f":white_check_mark: | Added ``{track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue!",
                    # ! OPTIONAL
                    # Check queue with ``{self.QUEUE_COMMAND}``",
                    # description=f":white_check_mark: | Queued ``[{track.author} - {track.title}]({track.uri})``",
                    # description=f":white_check_mark: | Added ``[{track.author} - {track.title}]({track.uri})``",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=queue_embed
                )

    @play_group.sub_command(
        name="spotify",
        description="Play a song from spotify"
    )
    async def play_spotify_song(self, interaction: disnake.ApplicationCommandInteraction, *, url: str):
        await interaction.response.defer()

        first_embed = disnake.Embed(
            description="Searching for song on spotify..."
        )
        await interaction.edit_original_message(embed=first_embed)

        if interaction.author.voice is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        if not interaction.guild.voice_client:
            self.channel = interaction.channel.id
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client

            if vc.queue.is_empty and not vc.is_playing():
                self.channel = interaction.channel.id
                decoded = spotify.decode_url(url)
                if decoded and decoded['type'] is spotify.SpotifySearchType.track:
                    track = await spotify.SpotifyTrack.search(query=decoded["id"], type=decoded["type"], return_first=True)
                    await vc.play(track)

                elif decoded['type'] is spotify.SpotifySearchType.unusable:
                    bad_embed = disnake.Embed(
                        description="Invalid spotify url!",
                        color=disnake.Color.red()
                    )
                    return await interaction.edit_original_message(
                        embed=bad_embed
                    )
            else:
                vc: wavelink.Player = interaction.guild.voice_client
                track = await spotify.SpotifyTrack.search(query=url, return_first=True)
                await vc.queue.put_wait(track)

                queue_embed = disnake.Embed(
                    description=f":white_check_mark: | Added ``{track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue!",
                    # ! OPTIONAL
                    # description=f":white_check_mark: | Added ``[{track.author} - {track.title}]({track.uri})``",
                    # Check queue with ``{self.QUEUE_COMMAND}``",
                    # description=f":white_check_mark: | Queued ``[{track.author} - {track.title}]({track.uri})``",
                    color=disnake.Color.green()
                )
                queue_embed.set_thumbnail(url=track.thumbnail)
                await interaction.edit_original_message(
                    embed=queue_embed
                )

    @play_playlist_group.sub_command(
        name="spotify",
        description="Play a playlist from Spotify"
    )
    async def play_spotify_playlist(self, interaction: disnake.ApplicationCommandInteraction, *, url: str):
        await interaction.response.defer()

        self.channel = interaction.channel.id
        if interaction.author.voice is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        vc: wavelink.Player = interaction.guild.voice_client or await interaction.author.voice.channel.connect(cls=wavelink.Player)
        counter = 0
        async for partial in spotify.SpotifyTrack.iterator(query=url, partial_tracks=True):
            counter = counter + 1
            await vc.queue.put_wait(partial)

        queue_embed = disnake.Embed(
            description=f"Added ``{counter} Tracks`` to queue!",  # Check queue with ``{self.QUEUE_COMMAND}``",
            # description=f":white_check_mark: | Queued ``[{partial.author} - {partial.title}]({partial.uri})``",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=queue_embed
        )

        # vc : wavelink.Player = interaction.guild.voice_client
        # async for track in spotify.SpotifyTrack.iterator(query=query, type=spotify.SpotifySearchType.playlist):
        #     vc.queue.put(track)

    @play_playlist_group.sub_command(
        name="youtube",
        description="Play a playlist from Youtube"
    )
    async def play_youtube_playlist(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer()

        self.channel = interaction.channel.id
        if interaction.author.voice is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        vc: wavelink.Player = interaction.guild.voice_client or await interaction.author.voice.channel.connect(cls=wavelink.Player)
        playlist = await vc.node.get_playlist(wavelink.YouTubePlaylist, search)
        counter = 0
        for track in playlist.tracks:
            counter = counter + 1
            await vc.queue.put_wait(track)

        queue_embed = disnake.Embed(
            description=f":white_check_mark: | Added ``{counter} Tracks`` to queue!",
            # to queue! Check queue with ``{self.QUEUE_COMMAND}``",
            # description=f":white_check_mark: | Queued ``[{track.author} - {track.title}]({track.uri})``",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=queue_embed
        )

    @play_stream_group.sub_command(
        name="youtube",
        description="Play a stream from a youtube channel"
    )
    async def play_stream(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        await interaction.response.defer()

        self.channel = interaction.channel.id
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        track = await vc.node.get_tracks(query=url, cls=wavelink.LocalTrack)
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(track[0])

            embed = disnake.Embed(
                description=f"Playing ``{track[0].author} - {track[0].title}``",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @queue_group.sub_command(
        name="clear",
        description="Clear the queue"
    )
    async def clear_queue(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        vc: wavelink.Player = interaction.guild.voice_client

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )

        elif vc.queue.is_empty:
            empty = disnake.Embed(
                description="There are no tracks in the queue.",
                color=disnake.Color.red()
            )
            channel = await self.client.fetch_channel(self.channel)
            await channel.send(embed=empty)

        else:
            vc: wavelink.Player = interaction.guild.voice_client
            vc.queue.clear()

            clear_embed = disnake.Embed(
                description="Deleted all tracks from the queue!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=clear_embed
            )

    @queue_group.sub_command(
        name="remove",
        description="Remove a track from the queue"
    )
    async def remove_queue(self, interaction: disnake.ApplicationCommandInteraction, index: int):
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client

        track = vc.queue[index - 1]
        vc.queue.__delitem__(index - 1)

        delete_embed = disnake.Embed(
            # title="Removed from queue",
            description=f"Removed track ``{track.title} [{index}]`` from queue",  # {index}`` from the queue",
            color=disnake.Color.green()
        )

        await interaction.edit_original_message(embed=delete_embed)

    @queue_group.sub_command(
        name="add",
        description="Adds a song to queue"
    )
    async def add_queue(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        track: wavelink.Track = await wavelink.YouTubeTrack.search(search, return_first=True)

        if vc.is_playing():
            await vc.queue.put_wait(track)

            queue_embed = disnake.Embed(
                description=f":white_check_mark: | Added [{track.title}]({track.uri})",
                # ! OPTIONAL
                # description=f":white_check_mark: | Queued ``{track.author} - {track.title}``",
                # to queue! Check queue with ``{self.QUEUE_COMMAND}``",
                # description=f":white_check_mark: | Queued ``[{track.author} - {track.title}]({track.uri})``",
                color=disnake.Color.green()
            )
            queue_embed.set_thumbnail(url=track.thumbnail)
            await interaction.edit_original_message(
                embed=queue_embed
            )
        else:
            await vc.play(track)

    @queue_group.sub_command(
        name="list",
        description="List the current queue"
    )
    async def queue_list(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )

        else:
            vc: wavelink.Player = interaction.guild.voice_client
            if vc.queue.is_empty and not vc.source:
                embed = disnake.Embed(
                    description="There are no songs in the queue!",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )

            elif vc.is_playing() and vc.queue.is_empty:
                allSongs = []
                current = vc.source

                allSongs.append(f"⬐ Current Track\n``1`` - ``{current.title[:48]} ...`` - ``{datetime.timedelta(seconds=round(vc.position))}/{datetime.timedelta(seconds=current.length)}``\n⬑ Current Track")

                if allSongs < 1024:
                    embed = disnake.Embed(
                        description="\n".join(allSongs),
                        color=0x00ff00
                    )
                    embed.set_author(
                        name=f"{interaction.guild.name}",
                        icon_url=interaction.guild.icon.url
                    )
                    await interaction.edit_original_message(embed=embed)

                else:
                    embed = disnake.Embed(
                        description="The queue is too long to display!",
                        color=0x00ff00
                    )
                    await interaction.edit_original_message(embed=embed)

            else:
                vc: wavelink.Player = interaction.guild.voice_client

                allSongs = []
                songs = [i.info for i in vc.queue]
                current = vc.source
                if songs > 1024:
                    for i in range(len(songs)):
                        # ! OPTIONAL
                        # if current:
                        #     allSongs.append(f"⬐ Current Track\n``{i + 1} - {current.title} - {datetime.timedelta(milliseconds=round(vc.position)) - datetime.timedelta(milliseconds=current.length)} left``\n⬑ Current Track")
                        # elif i == 1 or i > 1:
                        allSongs.append(f"``{i + 1}`` - ``{songs[i]['title'][:48]} ...`` - ``{datetime.timedelta(milliseconds=songs[i]['length'])}``")

                    embed = disnake.Embed(
                        description="\n".join(allSongs),
                        color=0x00ff00
                    )
                    embed.set_author(
                        name=f"{interaction.guild.name}",
                        icon_url=interaction.guild.icon.url
                    )
                    await interaction.edit_original_message(embed=embed)
                else:
                    half = allSongs[:1024]
                    rest = allSongs[1024:]
                    embed1 = disnake.Embed(
                        description="\n".join(half),
                        color=0x00ff00
                    )
                    embed1.set_author(
                        name=f"{interaction.guild.name}",
                        icon_url=interaction.guild.icon.url
                    )
                    await interaction.edit_original_message(embed=embed1)
                    embed2 = disnake.Embed(
                        description="\n".join(rest),
                        color=0x00ff00
                    )
                    embed2.set_author(
                        name=f"{interaction.guild.name}",
                        icon_url=interaction.guild.icon.url
                    )
                    await interaction.followup.send(embed=embed2)

    @modes.sub_command(
        name="bassboost",
        description="Bassboost the song"
    )
    async def bassboost(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

    @settings.sub_command(
        name="pause",
        description="Pause the current track"
    )
    async def pause(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            # ! OPTIONAL
            if vc.is_paused():
                embed = disnake.Embed(
                    description="The player is already paused",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(embed=embed)
            else:
                embed = disnake.Embed(
                    description="Paused the player",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(embed=embed)
                await vc.pause()

    @settings.sub_command(
        name="resume",
        description="Resume the current track"
    )
    async def resume(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            # ! OPTIONAL
            if not vc.is_paused():
                embed = disnake.Embed(
                    description="The player is already playing",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(embed=embed)
            else:
                embed = disnake.Embed(
                    description="Resuming the player",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(embed=embed)
                await vc.resume()

    @settings.sub_command(
        name="shuffle",
        description="Resume the current track"
    )
    async def shuffle(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            song = await vc.queue.get_wait()
            await vc.play(song)
            embed = disnake.Embed(
                description=f"Now playing `{vc.source.title}`",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(embed=embed)

    @settings.sub_command(
        name="volume",
        description="Changes the volume of the player"
    )
    async def volume(self, interaction: disnake.ApplicationCommandInteraction, volume: int):
        await interaction.response.defer(ephemeral=True)

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            if volume > 100:
                embed = disnake.Embed(
                    description="The volume can't be higher than 100",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                await vc.set_volume(volume)
                embed = disnake.Embed(
                    description=f"The volume has been set to {vc.volume}%",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=embed
                )

    @settings.sub_command(
        name="skip",
        description="Skips the current track"
    )
    async def skip(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            # ! OPTIONAL
            # if vc.is_paused():
            #     embed = disnake.Embed(
            #         description="The player is paused, please resume the player first",
            #         color=disnake.Color.red()
            #     )
            #     await interaction.edit_original_message(
            #         embed=embed
            #     )
            # else:
            if vc.queue.is_empty:
                embed = disnake.Embed(
                    description="The queue is empty",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                if vc.is_playing():
                    skip_embed = disnake.Embed(
                        description="Skipping the current track",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=skip_embed
                    )

                    # check if curret song name is same as with the one in queue
                    if vc.source.title == vc.queue[0].title:
                        # ! await vc.stop()
                        # deletes duplicate track
                        vc.queue.__delitem__(0)
                        # gets new track
                        nextSong = vc.queue[0]
                        # plays new track
                        await vc.play(nextSong)
                    else:
                        # ! await vc.stop()
                        # gets new track
                        nextSong = vc.queue[0]
                        # plays new track
                        await vc.play(nextSong)
                # if player dont play
                else:
                    # gets new track
                    nextSong = vc.queue[0]
                    # plays new track
                    await vc.play(nextSong)
                    # remove playing song from queue
                    vc.queue.__delitem__(0)

    @settings.sub_command(
        name="nowplaying",
        description="Shows the current track"
    )
    async def nowplaying(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        with open("json/settings.json", "r") as settings_file:
            settings_data = json.load(settings_file)

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            # ! OPTIONAL
            current = vc.source
            # if vc.is_paused():
            #     embed = disnake.Embed(
            #         description="The player is paused",
            #         color=disnake.Color.red()
            #     )
            #     await interaction.edit_original_message(
            #         embed=embed
            #     )
            # else:
            channel = self.client.get_channel(self.channel)

            embed = disnake.Embed(
                color=disnake.Color.green()
            )
            embed.add_field(
                name="Now Playing",
                value=f"``{current.title}``",
                # ! - {datetime.timedelta(seconds=round(vc.position))}/{datetime.timedelta(seconds=current.length)}``",
                inline=False
            )
            embed.add_field(
                name="Loop",
                value=f"``{'Yes' if settings_data[str(interaction.guild.id)]['music_loop'] is True else 'No'}``",
                inline=True
            )
            embed.add_field(
                name="Volume",
                value=f"``{vc.volume}%``",
                inline=True
            )
            embed.add_field(
                name="Time",
                value=f"``{datetime.timedelta(seconds=round(vc.position))}/{datetime.timedelta(seconds=current.length)}``",
                inline=True
            )
            embed.add_field(
                name="Link",
                value=current.uri,
                inline=False
            )
            embed.add_field(
                name="Announcement Channel",
                value=f"{channel.mention}",
                inline=True
            )
            embed.add_field(
                name="Announce Status",
                value=f"``{'Yes' if settings_data[str(interaction.guild.id)]['music_announce'] else 'No'}``",
                inline=True
            )
            embed.set_author(
                name=interaction.author.guild.name,
                icon_url=interaction.author.guild.icon.url
            )
            embed.set_footer(
                text=f"Bot provided by {self.provider}",
                icon_url=self.avatar
            )
            embed.set_thumbnail(current.thumbnail)
            await interaction.edit_original_message(
                embed=embed
            )

    @settings.sub_command(
        name="seek",
        description="Seeks to a specific position of the song"
    )
    async def seek(self, interaction: disnake.ApplicationCommandInteraction, time: str):
        await interaction.response.defer(ephemeral=True)

        if interaction.author.voice.channel is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )

        else:
            vc: wavelink.Player = interaction.guild.voice_client
            if vc.is_paused():
                embed = disnake.Embed(
                    description="The player is paused, please resume the player first",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                if vc.is_playing():
                    try:
                        seek_time = int(time)
                        if seek_time > vc.source.length:
                            embed = disnake.Embed(
                                description=f"The seek time is longer than the song length ``({vc.source.length})``",
                                color=disnake.Color.red()
                            )
                            await interaction.edit_original_message(
                                embed=embed
                            )
                        else:
                            embed = disnake.Embed(
                                description=f"Seeking to ``{datetime.timedelta(seconds=seek_time)}``",  # ! /{datetime.timedelta(seconds=vc.source.length)}``",
                                color=disnake.Color.green()
                            )
                            await interaction.edit_original_message(
                                embed=embed
                            )
                            await vc.seek(position=seek_time * 1000)

                    except ValueError:
                        embed = disnake.Embed(
                            description="The seek time is not a valid time",
                            color=disnake.Color.red()
                        )
                        await interaction.edit_original_message(
                            embed=embed
                        )

                else:
                    embed = disnake.Embed(
                        description="The player is not playing",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )

    @settings.sub_command(
        name="loop",
        description="Enables/Disables the loop of the current track"
    )
    async def looping(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        with open("json/settings.json", "r") as settings_file:
            settings_data = json.load(settings_file)

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            # ! OPTIONAL
            # if vc.is_paused():
            #     embed = disnake.Embed(
            #         description="The player is paused",
            #         color=disnake.Color.red()
            #     )
            #     await interaction.edit_original_message(
            #         embed=embed
            #     )
            if settings_data[str(interaction.guild.id)]["music_loop"] is False:
                settings_data[str(interaction.guild.id)]["music_loop"] = True
                with open("json/settings.json", "w") as settings_file:
                    json.dump(settings_data, settings_file, indent=4)

                embed = disnake.Embed(
                    description="Enabled track loop",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                settings_data[str(interaction.guild.id)]["music_loop"] = False
                with open("json/settings.json", "w") as settings_file:
                    json.dump(settings_data, settings_file, indent=4)

                embed = disnake.Embed(
                    description="Disabled track loop",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )

    @settings.sub_command(
        name="announce",
        description="Enables/Disables the announcement of the current track"
    )
    async def announcement(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        with open("json/settings.json", "r") as settings_file:
            settings_data = json.load(settings_file)

        if settings_data[str(interaction.guild.id)]["music_announce"] is False:
            settings_data[str(interaction.guild.id)]["music_announce"] = True
            with open("json/settings.json", "w") as settings_file:
                json.dump(settings_data, settings_file, indent=4)

            embed = disnake.Embed(
                description="Enabled track announcement",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

        else:
            settings_data[str(interaction.guild.id)]["music_announce"] = False
            embed = disnake.Embed(
                description="Disabled track announcement",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @settings.sub_command(
        name="announce_channel",
        description="Enables/Disables the announcement of the current track"
    )
    async def announcement_channel(self, interaction: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        await interaction.response.defer(ephemeral=True)

        with open("json/settings.json", "r") as settings_file:
            settings_data = json.load(settings_file)

        if settings_data[str(interaction.guild.id)]["music_announce_channel"] is None:
            settings_data[str(interaction.guild.id)]["music_announce_channel"] = channel.id
            with open("json/settings.json", "w") as settings_file:
                json.dump(settings_data, settings_file, indent=4)

            embed = disnake.Embed(
                description=f"Track Announcement Channel **set** to {channel.mention}",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

        else:
            settings_data[str(interaction.guild.id)]["music_announce_channel"] = channel.id
            with open("json/settings.json", "w") as settings_file:
                json.dump(settings_data, settings_file, indent=4)

            embed = disnake.Embed(
                description=f"Track Announcement Channel **changed** to {channel.mention}",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @settings.sub_command(
        name="disconnect",
        description="Disconnects the bot from the voice channel"
    )
    async def disconnect(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        if interaction.author.voice.channel is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            embed = disnake.Embed(
                description="Disconnecting from the voice channel",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )
            await vc.disconnect()

    @settings.sub_command(
        name="join",
        description="Joins the voice channel"
    )
    async def join(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        if interaction.author.voice.channel is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.edit_original_message(
                embed=bad_embed
            )
        else:
            embed = disnake.Embed(
                description="Joining your voice channel",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)


def setup(client):
    client.add_cog(Music(client))
