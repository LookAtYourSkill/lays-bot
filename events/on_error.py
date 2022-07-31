import disnake
from disnake.ext import commands
import wavelink


class onError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_channel = 1000043915753304105

    @commands.Cog.listener()
    async def on_slash_command_error(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        error: commands.CommandError
    ):

        if isinstance(
            error,
            commands.BotMissingPermissions
        ):
            embed = disnake.Embed(
                description=f"The bot misses a few permission to use that command. Required perms: `` {''.join(error.missing_permissions)}`` ⛔",
                color=disnake.Color.red()
            )

            await interaction.followup.send(
                embed=embed
            )

        if isinstance(
            error,
            commands.MissingPermissions
        ):
            embed = disnake.Embed(
                description=f"You dont have permission to use this commands. Required perms: ``{''.join(error.missing_permissions)}`` ⛔",
                color=disnake.Color.red()
            )

            await interaction.followup.send(
                embed=embed
            )

        if isinstance(
            error,
            commands.CommandOnCooldown
        ):
            embed = disnake.Embed(
                description=f"You are on cooldown {round(error.retry_after)} ⛔",
                color=disnake.Color.red()
            )

            await interaction.followup.send(
                embed=embed
            )

        else:
            channel = self.bot.get_channel(self.error_channel)

            error_embed = disnake.Embed(
                title=f"Error while command: {interaction.application_command.qualified_name}",
                description=f"```{error}``` \nGuild: `{interaction.guild.name}` \nChannel: `{interaction.channel.name}` \nUser: `{interaction.author.name}`",
                color=disnake.Color.red()
            )
            await channel.send(embed=error_embed)

    @commands.Cog.listener()
    async def on_wavelink_track_exception(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        player: wavelink.Player,
        track: wavelink.Track,
        error: wavelink.WavelinkError
    ):
        if isinstance(
            error,
            wavelink.LoadTrackError
        ):
            embed = disnake.Embed(
                description=f"The Track `{track.title}` could not be found ⛔",
                color=disnake.Color.red()
            )
            await interaction.followup.send(
                embed=embed
            )

        if isinstance(
            error,
            wavelink.QueueException
        ):
            embed = disnake.Embed(
                description="Something is wrong with the queue, please try again later ⛔",
                color=disnake.Color.red()
            )
            await interaction.followup(
                embed=embed
            )

        if isinstance(
            error,
            wavelink.QueueFull
        ):
            embed = disnake.Embed(
                description="The queue is full, please try again later ⛔",
                color=disnake.Color.red()
            )
            await interaction.followup.send(
                embed=embed
            )

        if isinstance(
            error,
            wavelink.BuildTrackError
        ):
            embed = disnake.Embed(
                description=f"The Track `{track.title}` could not be converted ⛔",
                color=disnake.Color.red()
            )
            await interaction.followup.send(
                embed=embed
            )

        if isinstance(
            error,
            wavelink.WavelinkError
        ):
            embed = disnake.Embed(
                description="Something is wrong with the bot, please try again later ⛔",
                color=disnake.Color.red()
            )
            await interaction.followup.send(
                embed=embed
            )

        else:
            print(error)


def setup(bot):
    bot.add_cog(onError(bot))
