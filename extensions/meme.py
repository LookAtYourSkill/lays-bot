import disnake
import utils.reddit

from disnake.ext import commands


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="meme")
    async def meme(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @meme.sub_command(name="reddit")
    async def meme_reddit(self, interaction: disnake.ApplicationCommandInteraction):
        loading_embed = disnake.Embed(
            description="Getting memes from Reddit...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        meme = utils.reddit.get_memes()
        print(meme)


def setup(bot):
    bot.add_cog(Meme(bot))
