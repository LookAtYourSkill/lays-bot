import json

import disnake
from disnake.ext import commands


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

            await interaction.edit_original_response(
                embed=embed
            )

        if isinstance(
            error,
            commands.MissingPermissions
        ):
            embed = disnake.Embed(
                description=f"{interaction.author.mention} dont have permission to use this commands. Required perms: ``{''.join(error.missing_permissions)}`` ⛔",
                color=disnake.Color.red()
            )

            await interaction.edit_original_response(
                embed=embed
            )

        if isinstance(
            error,
            commands.CommandOnCooldown
        ):
            embed = disnake.Embed(
                description=f"{interaction.author.mention} is on cooldown {round(error.retry_after)} ⛔",
                color=disnake.Color.red()
            )

            await interaction.edit_original_response(
                embed=embed
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
                description=f"{interaction.author.mention} This command isnt allowed in this server ⛔",
                color=disnake.Color.red()
            )

            await interaction.edit_original_message(
                embed=embed
            )

        else:
            embed = disnake.Embed(
                description=f"{interaction.author.mention} the error has been send to the developer and will be taken care of as soon as possible! I hope for your patience ⛔",
                color=disnake.Color.red()
            )

            await interaction.edit_original_response(
                embed=embed
            )

            channel = self.bot.get_channel(self.error_channel)

            error_embed = disnake.Embed(
                title=f"Error while command: {interaction.application_command.qualified_name}",
                description=f"```{error}``` \nGuild: `{interaction.guild.name}` \nChannel: `{interaction.channel.name}` \nUser: `{interaction.author}` \nID: `{interaction.author.id}`",
                color=disnake.Color.red()
            )
            # await channel.send(embed=error_embed)

def setup(bot):
    bot.add_cog(onError(bot))
