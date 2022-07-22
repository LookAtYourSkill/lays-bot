import disnake
import requests
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

        URL = "https://some-random-api.ml/meme"
        response = requests.get(
            URL,
            params={},
            headers={}
        )
        if response.status_code == 200:
            data = await response.json()
            await interaction.edit_original_message(data["fact"])
        else:
            await interaction.edit_original_message(f"Die API gibt den Status:{response.status_code}.")


def setup(bot):
    bot.add_cog(Meme(bot))
