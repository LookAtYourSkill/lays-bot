import json

import disnake
from disnake.ext import commands


class About(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot
        self.version = "EARLY ACCESS"
        self.prefix = "/"

    @commands.slash_command(
        description="Information about the bot"
    )
    async def about(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        with open("json/licenses.json", "r") as license_info:
            licenses = json.load(license_info)
        with open("json/guild.json", "r") as guild_info:
            guilds = json.load(guild_info)
        with open("json/general.json", "r") as general_info:
            general = json.load(general_info)

        if not guilds[str(interaction.author.guild.id)]["license"] or guilds[str(interaction.author.guild.id)]["license"] not in licenses and not general["license_check"]:
            no_licesnse_embed = disnake.Embed(
                title="No license ⛔",
                description="You have not set a license for this server. Please use `/license activate <license>` to set a license.",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=no_licesnse_embed,
                ephemeral=True
            )

        else:
            loading_embed = disnake.Embed(
                description="Fetching information about the bot...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )
            owner = self.bot.get_user(493370963807830016)

            about_embed = disnake.Embed(
                color=interaction.author.color
            )
            about_embed.add_field(
                name="> ❓ Autor",
                value=f"`»` Der Bot wurde von `{owner}` geschrieben",
                inline=False
            )
            about_embed.add_field(
                name="> ❓ Informationen",
                value=f"`»` Momentane Version: `{self.version}`\n"
                        f"`»` Momentanes Prefix: `{self.prefix}`",
                inline=False
            )
            about_embed.set_author(
                name=owner,
                icon_url=owner.avatar.url
            )
            await interaction.edit_original_message(
                embed=about_embed
            )


def setup(bot):
    bot.add_cog(About(bot))
