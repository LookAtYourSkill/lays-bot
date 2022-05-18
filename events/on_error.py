import disnake
from disnake.ext import commands


class onError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                description=f"Um diesen Befehl auszuführen, fehlen mir folgende Berechtigungen: `` {''.join(error.missing_permissions)}``!",
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
                description=f"Um diesen Befehl auszuführen, fehlen dir folgende Berechtigungen: ``{''.join(error.missing_permissions)}``!",
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
                description=f"Der Befehl ist noch {round(error.retry_after)} gesperrt!",
                color=disnake.Color.red()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )


def setup(bot):
    bot.add_cog(onError(bot))
