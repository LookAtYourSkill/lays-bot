import disnake
from disnake.ext import commands


class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.version = "EARLY ACCESS"

    @commands.slash_command(
        name="changelog",
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
            description="- **Added** License System [Soon Finished]\n"
                        "- **Added** new commands\n"
                        "- **Fixed** a few commands\n"
        )
        await interaction.edit_original_message(
            embed=changelog_embed
        )


def setup(bot):
    bot.add_cog(Changelog(bot))
