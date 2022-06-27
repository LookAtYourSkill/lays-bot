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
