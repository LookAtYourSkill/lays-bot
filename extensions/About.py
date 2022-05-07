import disnake
from disnake.ext import commands


class About(commands.Cog):
    def __init__(
        self,
        bot
    ):
        self.bot = bot
        self.author = "LookAtYourSkill#0001"
        self.version = 1.6
        self.prefix = "/"

    @commands.slash_command(
        description="Information about the bot"
    )
    async def about(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        about_embed = disnake.Embed(
            color=interaction.author.color
        )
        about_embed.add_field(
            name="> Autor",
            value=f"`»` Der Bot wurde von `{self.author}` geschrieben",
            inline=False
        )
        about_embed.add_field(
            name="> Informationen",
            value=f"`»` Momentane Version: `{self.version}`\n"
                  f"`»` Momentanes Prefix: `{self.prefix}`",
            inline=False
        )
        about_embed.set_author(
            name=self.author
        )
        await interaction.response.send_message(
            embed=about_embed,
            ephemeral=True
        )


def setup(bot):
    bot.add_cog(About(bot))
