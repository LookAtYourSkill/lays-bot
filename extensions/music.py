import pstats
import disnake
import wavelink
from wavelink.ext import spotify
from disnake.ext import commands


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loop = False
        self.channel = None
        self.queue = []
        self.QUEUE_COMMAND = "/queue list"

        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.client,
                                            host='127.0.0.1',
                                            port=2333,
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
            name="Duration", value=f"``{track.duration}``"
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

        if self.loop:
            await vc.play(track)

        elif vc.queue.is_empty():
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

    @play_group.sub_command(name="song", aliases=["p"])
    async def play_song(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        await interaction.response.defer()

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
                track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(search, return_first=True)
                await vc.play(track)
            else:
                vc: wavelink.Player = interaction.guild.voice_client
                track: wavelink.Track = await wavelink.Track.search(search, vc.node, return_first=True)
                await vc.queue.put_wait(track)

                queue_embed = disnake.Embed(
                    description=f"Added ``{track.author} - {track.title}`` to queue! Check queue with ``{self.QUEUE_COMMAND}``",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=queue_embed,
                    ephemeral=True
                )

    @play_group.sub_command(name="playlist")
    async def play_playlist(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        if interaction.author.voice is None:
            bad_embed = disnake.Embed(
                description="You are not connected to a voice channel!",
                color=disnake.Color.red()
            )
            return await interaction.response.send_message(
                embed=bad_embed, ephemeral=True
            )
        vc: wavelink.Player = interaction.voice_client or await interaction.author.voice.channel.connect(cls=wavelink.Player)
        playlist = await self.node.get_playlist(wavelink.YouTubePlaylist, search)
        for track in playlist.tracks:
            await vc.queue.put_wait(track)

    @play_group.sub_command(name="stream")
    async def play_stream(self, interaction: disnake.ApplicationCommandInteraction, url: str):
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        track = await vc.node.get_tracks(query=url, cls=wavelink.LocalTrack)
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(track[0])

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
                embed=bad_embed, ephemeral=True
            )

        elif vc.queue.is_empty():
            empty = disnake.Embed(
                description="There are no tracks in the queue.",
                color=disnake.Color.red()
            )
            channel = await self.client.fetch_channel(self.channel)
            await channel.send(embed=empty)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

            for i in self.queue:
                vc.queue.clear()

    @queue_group.sub_command(name="remove", description="Remove a track from the queue")
    async def remove_queue(self, interaction: disnake.ApplicationCommandInteraction, index: int):
        vc: wavelink.Player = interaction.guild.voice_client
        await vc.queue.__delitem__(index)

        delete_embed = disnake.Embed(
            title="Removed from queue",
            description=f"Removed track ``{index}`` from the queue",
            color=disnake.Color.green()
        )

        await interaction.response.send_message(embed=delete_embed)

    @queue_group.sub_command(name="add", description="Adds a song to queue")
    async def add_queue(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        vc: wavelink.Player = interaction.guild.voice_client
        track: wavelink.Track = await wavelink.Track.search(search, vc.node, return_first=True)
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
            if vc.queue.is_empty:
                embed = disnake.Embed(
                    description="Queue is empty!",
                    color=disnake.Color.red()
                )
            else:
                vc: wavelink.Player = interaction.guild.voice_client 
                tracks = vc.queue
                embed = disnake.Embed(
                    title="Queue",
                    description=f"``{len(tracks)} tracks``",
                    color=0x00ff00
                )
                for i, track in enumerate(tracks):
                    songs = [i.title for i in vc.queue]
                    for song in songs:
                        embed.add_field(
                            name=f"``{i + 1}`` ``{song}``",
                            value=f"``{track.duration}``",
                            inline=False
                        )

                await interaction.response.send_message(embed=embed)

    @commands.slash_command(name="modes")
    async def modes(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @commands.slash_command(name="pause", description="Pause the current track")
    async def pause(self, interaction: disnake.ApplicationCommandInteraction):
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
            if vc.is_paused:
                embed = disnake.Embed(
                    description="The player is already paused",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            await vc.pause()

    @commands.slash_command(name="resume", description="Resume the current track")
    async def resume(self, interaction: disnake.ApplicationCommandInteraction):
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
            if not vc.is_paused:
                embed = disnake.Embed(
                    description="The player is already playing",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            await vc.resume()


def setup(client):
    client.add_cog(Music(client))
