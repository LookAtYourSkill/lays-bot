import json

import disnake
from disnake.ext import commands


class Owner(commands.Cog):
    '''
    Commands for the owner of the bot
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="set")
    async def set(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @commands.is_owner()
    @set.sub_command(name="license")
    async def license(self, interaction: disnake.ApplicationCommandInteraction):
        with open("json/general.json", "r") as general_info:
            general = json.load(general_info)

        if not general["license"]:
            on_embed = disnake.Embed(
                description="License check is now enabled",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=on_embed
            )

            general["license"] = True
            with open("json/general.json", "w") as dump_file:
                json.dump(general, dump_file, indent=4)

        elif general["license"]:
            off_embed = disnake.Embed(
                description="License check is now disabled",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=off_embed
            )

            general["license"] = False
            with open("json/general.json", "w") as dump_file:
                json.dump(general, dump_file, indent=4)

        else:
            error_embed = disnake.Embed(
                description="An error occurred",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=error_embed
            )


def setup(bot):
    bot.add_cog(Owner(bot))
