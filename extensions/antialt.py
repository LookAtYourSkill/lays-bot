import disnake
import json
from disnake.ext import commands

from archive.checks._check_license import check_license


class AntiAlt(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot

    @check_license()
    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="antialt", description="Anti Alt Group Command")
    async def antialt(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @antialt.sub_command(name="set", description="Set a level for the days for the anti alt system")
    async def antialt_set(self, interaction: disnake.ApplicationCommandInteraction, days: int):
        await interaction.response.defer(ephemeral=True)

        if days < 0:
            embed = disnake.Embed(
                title="Anti Alt Detection",
                description="**Error**: `Days must be greater than 0`",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(embed=embed)
        else:
            with open("json/settings.json", "r") as f:
                settings_data = json.load(f)

            settings_data[str(interaction.guild.id)]["anti_alt_days"] = days
            with open("json/settings.json", "w") as f:
                json.dump(settings_data, f, indent=4)

            embed = disnake.Embed(
                title="Anti Alt System",
                description=f"Anti Alt System has been set to `{days}` days",
                color=disnake.Color.green()
            )

            await interaction.edit_original_message(embed=embed)

    @antialt.sub_command(name="get", description="Get the current level for the days for the anti alt system")
    async def antialt_get(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        with open("json/settings.json", "r") as f:
            settings_data = json.load(f)

        embed = disnake.Embed(
            title="Anti Alt System Info",
            description=f"Anti Alt System is set to `{settings_data[str(interaction.guild.id)]['anti_alt_days']}` days",
            color=disnake.Color.yellow()
        )

        await interaction.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(AntiAlt(bot))
