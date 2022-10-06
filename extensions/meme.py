import disnake
import requests
from disnake.ext import commands

from checks._check_license import check_license


class Meme(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot

    @check_license()
    @commands.slash_command(name="meme", description="Get a random meme")
    async def meme(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @meme.sub_command(
        name="reddit",
        description="Get a random meme from reddit",
    )
    async def meme_reddit(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            description="Getting memes from Reddit...",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )

        URL = "https://some-random-api.ml/meme"
        response = requests.get(
            URL
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

    @meme.sub_command(
        name="heroku",
        description="Get a random meme from heruko",
    )
    async def meme(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        URL = "https://meme-api.herokuapp.com/gimme"
        response = requests.get(
            URL
        )
        if response.status_code == 200:
            data = response.json()
            meme_embed = disnake.Embed(
                title=data['title'],
                color=disnake.Color.green()
            )
            meme_embed.set_image(url=data['url'])
            await interaction.edit_original_message(embed=meme_embed)


def setup(bot):
    bot.add_cog(Meme(bot))
