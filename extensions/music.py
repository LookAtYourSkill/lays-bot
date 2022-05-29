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

        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.client,
                                            host='127.0.0.1',
                                            port=2333,
                                            password='youshallnotpass',
                                            spotify_client=spotify.SpotifyClient(client_id="1dbe1627767f40d3b242ea6a77aecf8f", client_secret="ebac778486ed49958f182df9273947fd"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        now_playing = disnake.Embed(
            title="Now Playing",
            description=f"{track.author} - {track.title}",
            color=0x00ff00
        )
        now_playing.add_field(
            name="Duration", value=f"{track.duration}"
        )
        now_playing.add_field(
            name="URL",
            value=f"{track.uri}",
            inline=False
        )

        channel = await self.bot.fetch_channel(self.channel)

        await channel.send(embed=now_playing)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        print(f"Track {track.title} ended with reason {reason}")

    @commands.slash_command(name="play", aliases=["p"])
    async def play(self, interaction: disnake.ApplicationCommandInteraction, *, search: str):
        if interaction.author.voice is None:
            return await interaction.response.send_message("Not in voice channel")
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        track: wavelink.YouTubeTrack = await wavelink.YouTubeTrack.search(search, return_first=True)
        await vc.play(track)

    @commands.slash_command(name="queue")
    async def queue_group(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @queue_group.sub_command(name="clear", description="Clear the queue")
    async def clear_queue(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.guild.voice_client is None:
            return await interaction.response.send_message("Not connected to a voice channel")

        vc: wavelink.Player = interaction.guild.voice_client

        for i in self.queue:
            vc.queue.clear()

    @queue_group.sub_command(name="remove", description="Remove a track from the queue")
    async def remove(self, interaction: disnake.ApplicationCommandInteraction, index: int):
        vc: wavelink.Player = interaction.guild.voice_client
        vc.queue.__delitem__(index)

        delete_embed = disnake.Embed(
            title="Removed from queue",
            description=f"Removed track ``{index}`` from the queue",
            color=0x00ff00
        )

        await interaction.response.send_message(embed=delete_embed)

    @queue_group.sub_command(name="list", description="List the current queue")
    async def queue_list(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.guild.voice_client is None:
            return await interaction.response.send_message("Not connected to a voice channel")

        else:
            vc: wavelink.Player = interaction.guild.voice_client
            print(vc.queue)
            tracks = vc.queue
            embed = disnake.Embed(
                title="Queue",
                description=f"``{len(tracks)} tracks``",
                color=0x00ff00
            )
            for i, track in enumerate(tracks):
                embed.add_field(
                    name=f"``{i + 1}`` ``{track.info}``",
                    value=f"``{track.duration}``",
                    inline=False
                )

            await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
