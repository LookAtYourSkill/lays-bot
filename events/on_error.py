import json

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

        with open("json/errors.json", "r") as f:
            error_data = json.load(f)

        errors = 0
        for _ in error_data:
            errors += 1

        error_data[errors] = {
            "error": str(error),
            "status": "open / error",
            "command": interaction.application_command.name,
            "user": interaction.user.name,
            "user id": interaction.user.id,
            "guild": interaction.guild.name,
            "guild id": interaction.guild.id
        }

        with open("json/errors.json", "w") as f:
            json.dump(error_data, f, indent=4)

        if isinstance(
            error,
            commands.BotMissingPermissions
        ):
            embed = disnake.Embed(
                description=f"The bot misses a few permission to use that command. Required perms: `` {''.join(error.missing_permissions)}`` ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if isinstance(
            error,
            commands.MissingPermissions
        ):
            embed = disnake.Embed(
                description=f"{interaction.author.mention} dont have permission to use this commands. Required perms: ``{''.join(error.missing_permissions)}`` ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if isinstance(
            error,
            commands.CommandOnCooldown
        ):
            embed = disnake.Embed(
                description=f"{interaction.author.mention} is on cooldown {round(error.retry_after)} ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if isinstance(
            error,
            commands.CheckFailure
        ):
            no_licesnse_embed = disnake.Embed(
                title="No license ⛔",
                description="You have not set a license for this server. Please use `/license activate <license>` to set a license.",
                color=disnake.Color.red()
            )
            no_licesnse_embed.set_footer(
                text="If you dont have a license, please contact the bot owner or the server owner"
            )

            embed = disnake.Embed(
                description=f"{interaction.author.mention} This server does not have a valid license ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        else:
            embed = disnake.Embed(
                description=f"{interaction.author.mention} the error has been send to the developer and will be taken care of as soon as possible! I hope for your patience ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

            channel = self.bot.get_channel(self.error_channel)

            error_embed = disnake.Embed(
                title=f"Error while command: {interaction.application_command.qualified_name}",
                description=f"```{error}``` \nGuild: `{interaction.guild.name}` \nChannel: `{interaction.channel.name}` \nUser: `{interaction.author}` \nID: `{interaction.author.id}`",
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

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if isinstance(
            error,
            wavelink.QueueException
        ):
            embed = disnake.Embed(
                description="Something is wrong with the queue, please try again later ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if isinstance(
            error,
            wavelink.QueueFull
        ):
            embed = disnake.Embed(
                description="The queue is full, please try again later ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if isinstance(
            error,
            wavelink.BuildTrackError
        ):
            embed = disnake.Embed(
                description=f"The Track `{track.title}` could not be converted ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if isinstance(
            error,
            wavelink.WavelinkError
        ):
            embed = disnake.Embed(
                description="Something is wrong with the bot, please try again later ⛔",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        else:
            print(error)


def setup(bot):
    bot.add_cog(onError(bot))
