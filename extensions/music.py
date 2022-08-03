import datetime

import json

import disnake
import wavelink
from disnake.ext import commands
from wavelink.ext import spotify


class Music(commands.Cog):
    '''
    Music commands for more fun in a voice channel
    '''
    def __init__(self, client: disnake.Client):
        self.client = client
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
            value=f"``{'Yes' if track.is_stream else 'No'}``",
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
        if self.announce:
            pass
            # channel = await self.client.fetch_channel(self.channel)
            # await channel.send(embed=now_playing)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, vc: wavelink.Player, track: wavelink.Track, reason):

        print(f"Track {track.title} ended with reason {reason}")
        # if not self.loop:
            # vc.queue.__delitem__(0)
            # self.skipping = False

        # elif self.loop:
            # await vc.play(track)

        if vc.queue.is_empty:
            # await vc.stop()
            empty = disnake.Embed(
                description="There are no more tracks in the queue.\nIf you add a song use ``/queue resume`` to resume the queue!",
                color=disnake.Color.red()
            )
            channel = await self.client.fetch_channel(self.channel)
            await channel.send(embed=empty)

            # await asyncio.sleep(120)
            # await vc.disconnect()

        elif reason == "FINISHED":
            # ! CASE FINISHED
            print("[FINISHED] Song wurde fertig abgespielt")
            if vc.queue.is_empty:
                empty = disnake.Embed(
                    description="There are no more tracks in the queue.",
                    color=disnake.Color.red()
                )
                channel = await self.client.fetch_channel(self.channel)
                await channel.send(embed=empty)

            elif track.title == vc.queue[0].title:
                print("[FINISHED] Gleicher Song nochmal in queue")
                vc.queue.__delitem__(0)
                print("[FINISHED] Song wurde aus queue entfernt")
                nextSong = vc.queue[0]
                print("[FINISHED] Song wird gegettet")
                await vc.play(nextSong)
                print("[FINISHED] Song wird abgespielt")
                vc.queue.__delitem__(0)
                print("[FINISHED] Aktueller Song wurde aus queue entfernt")
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

    @commands.slash_command(
        name="music",
        description="Music commands",
    )
    async def music(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @music.sub_command_group(
        name="settings",
        description="Settings for the music module"
    )
    async def settings(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @music.sub_command_group(
        name="modes",
        invoke_without_command=True
    )
    async def modes(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @music.sub_command_group(
        name="play",
        invoke_without_command=True
    )
    async def play_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @music.sub_command_group(
        name="playlist",
        invoke_without_command=True
    )
    async def play_playlist_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @music.sub_command_group(
        name="stream",
        invoke_without_command=True
    )
    async def play_stream_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @music.sub_command_group(
        name="queue",
        invoke_without_command=True
    )
    async def queue_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @play_group.sub_command(
        name="youtube",
        description="Play a song from youtube"
    )
    async def play_youtube_song(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer(ephemeral=True)

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
        await interaction.response.defer(ephemeral=True)

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
        await interaction.response.defer(ephemeral=True)

        first_embed = disnake.Embed(
            description="Searching for song on spotify..."
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
        await interaction.response.defer(ephemeral=True)

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
        async for partial in spotify.SpotifyTrack.iterator(query=url, partial_tracks=True):
            queue_embed = disnake.Embed(
                description=f"Added ``{partial.title}`` to queue! | All tracks: /",  # Check queue with ``{self.QUEUE_COMMAND}``",
                # description=f":white_check_mark: | Queued ``[{partial.author} - {partial.title}]({partial.uri})``",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=queue_embed
            )
            await vc.queue.put_wait(partial)

        # vc : wavelink.Player = interaction.guild.voice_client
        # async for track in spotify.SpotifyTrack.iterator(query=query, type=spotify.SpotifySearchType.playlist):
        #     vc.queue.put(track)

    @play_playlist_group.sub_command(
        name="youtube",
        description="Play a playlist from Youtube"
    )
    async def play_youtube_playlist(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer(ephemeral=True)

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
        for track in playlist.tracks:
            queue_embed = disnake.Embed(
                description=f":white_check_mark: | Added ``{track.title}`` to queue! | All Tracks: /",
                # to queue! Check queue with ``{self.QUEUE_COMMAND}``",
                # description=f":white_check_mark: | Queued ``[{track.author} - {track.title}]({track.uri})``",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=queue_embed
            )
            await vc.queue.put_wait(track)

    @play_stream_group.sub_command(
        name="youtube",
        description="Play a stream from a youtube channel"
    )
    async def play_stream(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        await interaction.response.defer(ephemeral=True)

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
        vc: wavelink.Player = interaction.guild.voice_client

        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.response.send_message(
                embed=bad_embed,
                ephemeral=True
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
            await interaction.response.send_message(
                embed=clear_embed,
                ephemeral=True
            )

    @queue_group.sub_command(
        name="remove",
        description="Remove a track from the queue"
    )
    async def remove_queue(self, interaction: disnake.ApplicationCommandInteraction, index: int):
        await interaction.response.defer(ephemeral=True)

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
        await interaction.response.defer(ephemeral=True)

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
                vc: wavelink.Player = interaction.guild.voice_client

                allSongs = []
                songs = [i.info for i in vc.queue]
                current = vc.source

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

    @queue_group.sub_command(
        name="resume",
        description="Resumes the queue"
    )
    async def resume_queue(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        vc: wavelink.Player = interaction.guild.voice_client
        # if not vc.queue.is_empty and not vc.is_playing():

        if vc.is_playing():
            return

        else:
            getNextSong = vc.queue[0]  # ! vc.queue.get()
            await vc.play(getNextSong)

            embed = disnake.Embed(
                description=f"Resumed the queue! Playing: ``{getNextSong.title}``",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

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
                value=f"``{'Yes' if self.loop else 'No'}``",
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
                value=f"``{'Yes' if self.announce else 'No'}``",
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
            if self.loop is False:
                self.loop = True
                embed = disnake.Embed(
                    description="Enabled track loop",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                self.loop = False
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

        if self.announce:
            self.announce = False
            embed = disnake.Embed(
                description="Disabled track announcement",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

        else:
            self.announce = True
            embed = disnake.Embed(
                description="Enabled track announcement",
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
