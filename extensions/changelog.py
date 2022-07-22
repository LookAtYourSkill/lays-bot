import disnake
from disnake.ext import commands


class Changelog(commands.Cog):
    '''
    Shows the changelog for the bot
    '''
    def __init__(self, bot):
        self.bot = bot
        self.version = "EARLY ACCESS"

    @commands.slash_command(
        name="changelog",
        description="Shows the changelog for the bot"
    )
    async def changelog(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @changelog.sub_command(
        name="log",
        description="Shows the changelog"
    )
    async def changelog(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        loading_embed = disnake.Embed(
            description="Fetching latest changelog...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        changelog_embed = disnake.Embed(
            title=f"⚙️ Changelog [Version: {self.version}]",
            description="- **Added** License System [Finished :tada: ]\n"
                        "- **Added** Suggest commands\n"
                        "- **Added** meme command\n"
                        "- **changed** error messages\n"
        )
        await interaction.edit_original_message(
            embed=changelog_embed
        )


def setup(bot):
    bot.add_cog(Changelog(bot))
