import datetime
from multiprocessing.sharedctypes import Value

import disnake
from pyparsing import col
import wavelink
from disnake.ext import commands
from wavelink.ext import spotify


class Music(commands.Cog):
    def __init__(self, client: disnake.Client):
        self.client = client
        self.loop = False
        self.channel = None
        self.QUEUE_COMMAND = "/queue list"
        self.skipping = False

        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(
            bot=self.client,
            host='127.0.0.1',
            port=2334,
            password='youshallnotpass',
            spotify_client=spotify.SpotifyClient(
                client_id="1dbe1627767f40d3b242ea6a77aecf8f",
                client_secret="ebac778486ed49958f182df9273947fd"
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

        channel = await self.client.fetch_channel(self.channel)
        await channel.send(embed=now_playing)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, vc: wavelink.Player, track: wavelink.Track, reason):
        print(f"Track {track.title} ended with reason {reason}")
        if self.skipping:
            vc.queue.__delitem__(0)
            self.skipping = False

        elif self.loop:
            await vc.play(track)

        elif vc.queue.is_empty:
            await vc.stop()
            empty = disnake.Embed(
                description="There are no more tracks in the queue.",
                color=disnake.Color.red()
            )
            channel = await self.client.fetch_channel(self.channel)
            await channel.send(embed=empty)

            # await asyncio.sleep(120)
            # await vc.disconnect()

        elif reason == "FINISHED":
            if track == vc.queue[0]:
                vc.queue.__delitem__(0)
                nextSong = vc.queue[0]
                await vc.play(nextSong)
            # print("skipping")
            # nextSong = vc.queue.get()
            # await vc.play(nextSong)

        # when song get skipped
        elif reason == "STOPPED":
            nextSong = vc.queue[0]
            await vc.play(nextSong)
            vc.queue.__delitem__(0)

        else:
            print(reason)

    @commands.slash_command(name="play")
    async def play_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @play_group.sub_command(name="youtube_scuffed", description="Play a song from youtube")
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
        else:
            vc: wavelink.Player = interaction.guild.voice_client

            if vc.queue.is_empty and not vc.is_playing:
                self.channel = interaction.channel.id
                vc: wavelink.Player = interaction.guild.voice_client
                # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(search, return_first=True)
                play_embed = disnake.Embed(
                    description=f":white_check_mark: | Playing ({track.author} - {track.title})[{track.uri}] - ``{str(datetime.timedelta(seconds=track.length))}``",
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
                    description=f":white_check_mark: | Added ``{track.author} - {track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue!",
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

    @play_group.sub_command(name="soundcloud", description="Play a song from soundcloud")
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
        else:
            vc: wavelink.Player = interaction.guild.voice_client

            if vc.queue.is_empty and not vc.is_playing:
                self.channel = interaction.channel.id
                vc: wavelink.Player = interaction.guild.voice_client
                track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
                # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                play_embed = disnake.Embed(
                    description=f":white_check_mark: | Playing ({track.author} - {track.title})[{track.uri}] - ``{str(datetime.timedelta(seconds=track.length))}``",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=play_embed
                )
                await vc.play(track[0])
            else:
                vc: wavelink.Player = interaction.guild.voice_client
                # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
                await vc.queue.put_wait(track[0])

                queue_embed = disnake.Embed(
                    description=f":white_check_mark: | Added ``{track.author} - {track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue!",
                    # ! OPTIONAL
                    # Check queue with ``{self.QUEUE_COMMAND}``",
                    # description=f":white_check_mark: | Queued ``[{track.author} - {track.title}]({track.uri})``",
                    # description=f":white_check_mark: | Added ``[{track.author} - {track.title}]({track.uri})``",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=queue_embed
                )

    @play_group.sub_command(name="youtube", description="Play a song from a youtube url")
    async def play_local_song(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer(ephemeral=True)

        self.channel = interaction.channel.id
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
        if vc.queue.is_empty and not vc.is_playing:
            await vc.play(track[0])

            embed = disnake.Embed(
                description=f"Playing ``{track[0].author} - {track[0].title}``",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @play_group.sub_command(name="spotify", description="Play a song from spotify")
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

            if vc.queue.is_empty and not vc.is_playing:
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
                    description=f":white_check_mark: | Added ``{track.author} - {track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue!",
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

    @play_group.sub_command_group(name="playlist")
    async def play_playlist_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @play_playlist_group.sub_command(name="spotify", description="Play a playlist from Spotify")
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

    @play_playlist_group.sub_command(name="youtube", description="Play a playlist from Youtube")
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
                description=f":white_check_mark: | Added ``{track.author} - {track.title}`` to queue! | All Tracks: /",
                # to queue! Check queue with ``{self.QUEUE_COMMAND}``",
                # description=f":white_check_mark: | Queued ``[{track.author} - {track.title}]({track.uri})``",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=queue_embed
            )
            await vc.queue.put_wait(track)

    @play_group.sub_command_group(name="stream")
    async def play_stream_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @play_stream_group.sub_command(name="youtube", description="Play a stream from a youtube channel")
    async def play_stream(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        await interaction.response.defer(ephemeral=True)

        self.channel = interaction.channel.id
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        track = await vc.node.get_tracks(query=url, cls=wavelink.LocalTrack)
        if vc.queue.is_empty and not vc.is_playing:
            await vc.play(track[0])

            embed = disnake.Embed(
                description=f"Playing ``{track[0].author} - {track[0].title}``",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @commands.slash_command(name="queue")
    async def queue_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @queue_group.sub_command(name="clear", description="Clear the queue")
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

            # for i in vc.queue:
            #    vc.queue.__delitem__(i)

    @queue_group.sub_command(name="remove", description="Remove a track from the queue")
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

    @queue_group.sub_command(name="add", description="Adds a song to queue")
    async def add_queue(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer(ephemeral=True)

        vc: wavelink.Player = interaction.guild.voice_client
        track: wavelink.Track = await wavelink.YouTubeTrack.search(search, return_first=True)

        if vc.is_playing:
            await vc.queue.put_wait(track)

            queue_embed = disnake.Embed(
                description=f":white_check_mark: | Added [{track.author} - {track.title}]({track.uri})",
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

    @queue_group.sub_command(name="list", description="List the current queue")
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
            if vc.queue.is_empty:
                embed = disnake.Embed(
                    description="There are no songs in the queue!",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )

            else:
                vc: wavelink.Player = interaction.guild.voice_client

                allSongs = []
                songs = [i.info for i in vc.queue]
                # current = vc.queue[-1]

                for i in range(len(songs)):
                    # ! OPTIONAL
                    # if current:
                    #     allSongs.append(f"⬐ Current Track\n``{i + 1} - {current.title[:48]} - {str(datetime.timedelta(seconds=current.length))}``\n⬑ Current Track")
                    # elif i == 0 or i > -1:
                    allSongs.append(f"``{i + 1}`` - ``{songs[i]['title'][:48]} ... - {str(datetime.timedelta(milliseconds=songs[i]['length']))}``")

                embed = disnake.Embed(
                    description="\n".join(allSongs),
                    color=0x00ff00
                )
                embed.set_author(
                    name=f"{interaction.guild.name}",
                    icon_url=interaction.guild.icon.url
                )
                await interaction.edit_original_message(embed=embed)

    @commands.slash_command(name="modes")
    async def modes(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @modes.sub_command(name="bassboost", description="Bassboost")
    async def bassboost(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

    @commands.slash_command(name="pause", description="Pause the current track")
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
            # if vc.is_paused:
            #     embed = disnake.Embed(
            #         description="The player is already paused",
            #         color=disnake.Color.red()
            #     )
            #     await interaction.edit_original_message(embed=embed)
            # else:
            embed = disnake.Embed(
                description="Paused the player",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(embed=embed)
            await vc.pause()

    @commands.slash_command(name="resume", description="Resume the current track")
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
            # if not vc.is_paused:
            #     embed = disnake.Embed(
            #         description="The player is already playing",
            #        color=disnake.Color.red()
            #     )
            #     await vc.resume()
            #     await interaction.edit_original_message(embed=embed)
            # else:
            embed = disnake.Embed(
                description="Resuming the player",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(embed=embed)
            await vc.resume()

    @commands.slash_command(name="volume", description="Changes the volume of the player")
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

    @commands.slash_command(name="skip", description="Skips the current track")
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
            # if vc.is_paused:
            #     embed = disnake.Embed(
            #         description="The player is paused, please resume the player first",
            #         color=disnake.Color.red()
            #     )
            #     await interaction.edit_original_message(
            #         embed=embed
            #     )
            # else:
            skip_embed = disnake.Embed(
                description="Skipping the current track",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=skip_embed
            )
            track: wavelink.Track = vc.queue[0]

            if vc.queue[-1] == track:
            # self.skipping = True
                await vc.stop()
                vc.queue.__delitem__(0)
                nextSong = vc.queue[0]
                await vc.play(nextSong)
            else:
                await vc.stop()
                nextSong = vc.queue[0]
                await vc.play(nextSong)
            # await vc.play(await vc.queue.get_wait())

    @commands.slash_command(name="nowplaying", description="Shows the current track")
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
            current = vc.queue[0]
            # if vc.is_paused:
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
                value=f"``{current.title} - {str(datetime.timedelta(seconds=current.length))}``",
                inline=False
            )
            embed.add_field(
                name="Loop",
                value=f"``{'Yes' if self.loop else 'No'}``",
                inline=False
            )
            embed.add_field(
                name="Volume",
                value=f"``{vc.volume}%``",
                inline=False
            )
            embed.add_field(
                name="Announcement Channel",
                value=f"{channel.mention}",
                inline=False
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @commands.slash_command(name="loop", description="Loops the current track")
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
            # if vc.is_paused:
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

    @commands.slash_command(name="disconnect", description="Disconnects the bot from the voice channel")
    async def disconnect(self, interaction: disnake.ApplicationCommandInteraction):
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
            embed = disnake.Embed(
                description="Disconnecting from the voice channel",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )
            await vc.disconnect()

    @commands.slash_command(name="join", description="Joins the voice channel")
    async def join(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        # if interaction.guild.voice_client is None:
        #     bad_embed = disnake.Embed(
        #         description="You are not connected to a voice channel!",
        #         color=disnake.Color.red()
        #     )
        #     return await interaction.edit_original_message(
        #         embed=bad_embed
        #     )
        # else:
        embed = disnake.Embed(
            description="Joining the voice channel",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=embed
        )
        await interaction.author.voice.channel.connect()

    @commands.slash_command(name="among_us")
    async def among_us(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @among_us.sub_command(name="ruhe", description="Ruhe")
    async def among_us_ruhe(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        muted = []
        for i in interaction.author.voice.channel.members:
            if i.top_role < interaction.author.top_role:
                await i.edit(mute=True)
                muted.append(i)

        embed = disnake.Embed(
            description=f"{muted}\n",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=embed
        )

    @among_us.sub_command(name="meeting", description="Ruhe abbrechen")
    async def among_us_meeting(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        unmuted = []
        for i in interaction.author.voice.channel.members:
            if i.top_role < interaction.author.top_role:
                await i.edit(mute=False)
                unmuted.append(i)

        embed = disnake.Embed(
            description=f"{unmuted}\n",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=embed
        )


def setup(client):
    client.add_cog(Music(client))
