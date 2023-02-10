import json
import sys

import disnake
from disnake.ext import commands


class About(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot
        self.version = "EARLY ACCESS"
        self.prefix = "/"

    
    @commands.slash_command(
        name="about",
        description="Command Group for about the bot"
    )
    async def about(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @about.sub_command(
        description="Information about the bot"
    )
    async def info(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            description="Fetching information about the bot...",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )
        owner = self.bot.get_user(493370963807830016)

        about_embed = disnake.Embed(
            color=interaction.author.color
        )
        about_embed.add_field(
            name="> ❓ Author",
            value=f"`»` Bot written by `{owner}`",
            inline=False
        )
        about_embed.add_field(
            name="> ❓ Information",
            value=f"`»` Version: `{self.version}`\n"
                    f"`»` Disnake Version: `{disnake.__version__}`\n"
                    f"`»` Python Version: `{sys.version[:6]}`\n"
                    f"`»` Prefix: `{self.prefix}`",
            inline=False
        )
        about_embed.add_field(
            name="> ❓ Bot Information",
            value=f"`»` Server: `{len(self.bot.guilds)}`\n`»` User: `{len(self.bot.users)}`",
            inline=False
        )
        about_embed.set_author(
            name=owner,
            icon_url=owner.avatar.url
        )
        about_embed.set_thumbnail(self.bot.user.avatar.url)
        await interaction.edit_original_message(
            embed=about_embed
        )


def setup(bot):
    bot.add_cog(About(bot))
