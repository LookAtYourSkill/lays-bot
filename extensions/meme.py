import disnake
import requests
from disnake.ext import commands


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="meme", description="Get a random meme")
    async def meme(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @meme.sub_command(
        name="reddit",
        description="Get a random meme from reddit",
    )
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
            data = response.json()

            meme_embed = disnake.Embed(
                title=data["caption"],
                description=f"Category: {data['category']}",
                color=disnake.Color.green()
            )
            meme_embed.set_image(url=data["image"])

            await interaction.edit_original_message(
                embed=meme_embed
            )
        else:
            await interaction.edit_original_message(f"Die API gibt den Status:{response.status_code}.")


def setup(bot):
    bot.add_cog(Meme(bot))
