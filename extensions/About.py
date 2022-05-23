import disnake
from disnake.ext import commands


class About(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot
        self.author = "LookAtYourSkill#6388"
        self.version = 1.7
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

        about_embed = disnake.Embed(
            color=interaction.author.color
        )
        about_embed.add_field(
            name="> ❓ Autor",
            value=f"`»` Der Bot wurde von `{self.author}` geschrieben",
            inline=False
        )
        about_embed.add_field(
            name="> ❓ Informationen",
            value=f"`»` Momentane Version: `{self.version}`\n"
                  f"`»` Momentanes Prefix: `{self.prefix}`",
            inline=False
        )
        about_embed.set_author(
            name=self.author
        )
        await interaction.edit_original_message(
            embed=about_embed
        )


def setup(bot):
    bot.add_cog(About(bot))
