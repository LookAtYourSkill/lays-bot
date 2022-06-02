import disnake
import wavelink
from wavelink.ext import spotify
from disnake.ext import commands
import datetime


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loop = False
        self.channel = None
        self.QUEUE_COMMAND = "/queue list"

        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.client,
                                            host='127.0.0.1',
                                            port=2334,
                                            password='youshallnotpass',
                                            spotify_client=spotify.SpotifyClient(client_id="1dbe1627767f40d3b242ea6a77aecf8f", client_secret="ebac778486ed49958f182df9273947fd")
                                            )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        now_playing = disnake.Embed(
            title="Now Playing",
            description=f"``{track.author} - {track.title}``",
            color=0x00ff00
        )
        now_playing.add_field(
            name="Duration", value=f"``{str(datetime.timedelta(seconds=track.length))}``"
        )
        now_playing.add_field(
            name="URL",
            value=f"{track.uri}",
            inline=False
        )
        # now_playing.set_thumbnail(url=track.thumbnail)

        channel = await self.client.fetch_channel(self.channel)

        await channel.send(embed=now_playing)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, vc: wavelink.Player, track: wavelink.Track, reason):
        print(f"Track {track.title} ended with reason {reason}")

        if self.loop:
            await vc.play(track)

        elif vc.queue.is_empty():
            await vc.stop()
            empty = disnake.Embed(
                description="There are no more tracks in the queue.",
                color=disnake.Color.red()
            )
            channel = await self.client.fetch_channel(self.channel)
            await channel.send(embed=empty)
            await vc.disconnect()

        else:
            nextSong = vc.queue.get()
            await vc.play(nextSong)

    @commands.slash_command(name="play")
    async def play_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @play_group.sub_command(name="youtube", description="Play a song from youtube")
    async def play_youtube_song(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
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
                await vc.play(track)
            else:
                vc: wavelink.Player = interaction.guild.voice_client
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(search, return_first=True)
                # track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                await vc.queue.put_wait(track)

                queue_embed = disnake.Embed(
                    description=f"Added ``{track.author} - {track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue! Check queue with ``{self.QUEUE_COMMAND}``",
                    color=disnake.Color.green()
                )
                queue_embed.set_thumbnail(url=track.thumbnail)
                await interaction.edit_original_message(
                    embed=queue_embed
                )

    @play_group.sub_command(name="soundcloud", description="Play a song from soundcloud")
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
                # track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
                track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                await vc.play(track[0])
            else:
                vc: wavelink.Player = interaction.guild.voice_client
                track = await vc.node.get_tracks(query=search, cls=wavelink.LocalTrack)
                # track: wavelink.SoundCloudTrack = await wavelink.SoundCloudTrack.search(query=search, return_first=True)
                await vc.queue.put_wait(track[0])

                queue_embed = disnake.Embed(
                    description=f"Added ``{track.author} - {track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue! Check queue with ``{self.QUEUE_COMMAND}``",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=queue_embed
                )

    @play_group.sub_command(name="spotify", description="Play a song from spotify")
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
                    description=f"Added ``{track.author} - {track.title}`` - ``{str(datetime.timedelta(seconds=track.length))}`` to queue! Check queue with ``{self.QUEUE_COMMAND}``",
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
        if interaction.author.voice is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.response.send_message(
                embed=bad_embed, ephemeral=True
            )
        vc: wavelink.Player = interaction.guild.voice_client or await interaction.author.voice.channel.connect(cls=wavelink.Player)
        async for partial in spotify.SpotifyTrack.iterator(query=url, partial_tracks=True):
            queue_embed = disnake.Embed(
                description=f"Added ``{partial.author} - {partial.title}`` to queue! Check queue with ``{self.QUEUE_COMMAND}``",
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
        if interaction.author.voice is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.response.send_message(
                embed=bad_embed, ephemeral=True
            )
        vc: wavelink.Player = interaction.guild.voice_client or await interaction.author.voice.channel.connect(cls=wavelink.Player)
        playlist = await vc.node.get_playlist(wavelink.YouTubePlaylist, search)
        for track in playlist.tracks:
            queue_embed = disnake.Embed(
                description=f"Added ``{track.author} - {track.title}`` to queue! Check queue with ``{self.QUEUE_COMMAND}``",
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
            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
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
                description="Cleared the queue!",
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
        await interaction.response.defer()

        vc: wavelink.Player = interaction.guild.voice_client
        vc.queue.__delitem__(index - 1)

        delete_embed = disnake.Embed(
            title="Removed from queue",
            description=f"Removed track ``{index}`` from the queue",
            color=disnake.Color.green()
        )

        await interaction.edit_original_message(embed=delete_embed)

    @queue_group.sub_command(name="add", description="Adds a song to queue")
    async def add_queue(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        vc: wavelink.Player = interaction.guild.voice_client
        track: wavelink.Track = await wavelink.YouTubeTrack.search(search, return_first=True)
        await vc.queue.put_wait(track)

        queue_embed = disnake.Embed(
            description=f"Added ``{track.author} - {track.title}`` to queue! Check queue with ``{self.QUEUE_COMMAND}``",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=queue_embed,
            ephemeral=True
        )

    @queue_group.sub_command(name="list", description="List the current queue")
    async def queue_list(self, interaction: disnake.ApplicationCommandInteraction):
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
            if vc.queue.is_empty:
                embed = disnake.Embed(
                    description="Queue is empty!",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                vc: wavelink.Player = interaction.guild.voice_client

                # allSongs = []
                # songs = [i.title for i in vc.queue]
                # for song, i in songs:
                #    allSongs.append(f"{i + 1} - {song}")

                tracks = vc.queue
                embed = disnake.Embed(
                    title=f"Queue - {len(tracks)} Tracks",
                    # description="\n".join(allSongs),
                    color=0x00ff00
                )
                songs = [i.title for i in vc.queue]
                for song in songs:
                    embed.add_field(
                        name="\u200b",
                        value=f"``{song}``",
                        inline=False
                    )

                await interaction.edit_original_message(embed=embed)

    @commands.slash_command(name="modes")
    async def modes(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @commands.slash_command(name="pause", description="Pause the current track")
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
            if vc.is_paused:
                embed = disnake.Embed(
                    description="The player is already paused",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(embed=embed)
            else:
                vc.pause()
                embed = disnake.Embed(
                    description="Paused the player",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(embed=embed)
                await vc.pause()

    @commands.slash_command(name="resume", description="Resume the current track")
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
            if not vc.is_paused:
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

    @commands.slash_command(name="volume", description="Changes the volume of the player")
    async def volume(self, interaction: disnake.ApplicationCommandInteraction, volume: int):
        if interaction.guild.voice_client is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.response.send_message(
                embed=bad_embed,
                ephemeral=True
            )
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            if volume > 100:
                embed = disnake.Embed(
                    description="The volume can't be higher than 100",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True
                )
            else:
                await vc.set_volume(volume)
                embed = disnake.Embed(
                    description=f"The volume has been set to {vc.volume}%",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True
                )

    @commands.slash_command(name="skip", description="Skips the current track")
    async def skip(self, interaction: disnake.ApplicationCommandInteraction):
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
            if vc.is_paused:
                embed = disnake.Embed(
                    description="The player is paused, please resume the player first",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                skip_embed = disnake.Embed(
                    description="Skipping the current track",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=skip_embed
                )
                await vc.stop()
                await vc.play(await vc.queue.get_wait())

    @commands.slash_command(name="nowplaying", description="Shows the current track")
    async def nowplaying(self, interaction: disnake.ApplicationCommandInteraction):
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
            if vc.is_paused:
                embed = disnake.Embed(
                    description="The player is paused",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                embed = disnake.Embed(
                    description=f"Now playing: {vc.queue[0]}",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=embed
                )

    @commands.slash_command(name="loop", description="Loops the current track")
    async def looping(self, interaction: disnake.ApplicationCommandInteraction):
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
            if vc.is_paused:
                embed = disnake.Embed(
                    description="The player is paused",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            elif self.loop is False:
                self.loop = True
                embed = disnake.Embed(
                    description="Looping the current track",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
            else:
                self.loop = False
                embed = disnake.Embed(
                    description="Disabled looping",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=embed
                )


def setup(client):
    client.add_cog(Music(client))
