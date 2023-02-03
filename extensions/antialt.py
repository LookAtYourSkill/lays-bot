import disnake
import json
from disnake.ext import commands



class AntiAlt(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot

    
    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="antialt", description="Anti Alt Group Command")
    async def antialt(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @antialt.sub_command_group(name="time", description="Anti Alt Time Group Command")
    async def antialt_time(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @antialt.sub_command_group(name="avatar", description="Anti Alt Avatar Group Command")
    async def antialt_avatar(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @antialt_time.sub_command(name="set", description="Set a level for the days for the anti alt system")
    async def antialt_set(self, interaction: disnake.ApplicationCommandInteraction, days: int):
        await interaction.response.defer(ephemeral=True)

        if days < 0:
            embed = disnake.Embed(
                # title="Anti Alt Detection System",
                description="> **Error**: Days must be **higher** than `0`",
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
                # title="Anti Alt Detection System",
                description=f"> AADS has been set to `{days}` days",
                color=disnake.Color.green()
            )
            embed.set_footer(text="AADS = Anti Alt Detection System")

            await interaction.edit_original_message(embed=embed)

    @antialt_time.sub_command(name="get", description="Get the current level for the days for the anti alt system")
    async def antialt_get(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        with open("json/settings.json", "r") as f:
            settings_data = json.load(f)

        embed = disnake.Embed(
            # title="Anti Alt Detection System Info",
            description=f"> AADS is set to `{settings_data[str(interaction.guild.id)]['anti_alt_days']}` days",
            color=disnake.Color.yellow()
        )
        embed.set_footer(text="AADS = Anti Alt Detection System")

        await interaction.edit_original_message(embed=embed)

    @antialt_avatar.sub_command(name="set", description="Set an option for the default avatar detection system")
    async def antialt_avatar_set(self, interaction: disnake.ApplicationCommandInteraction, status: bool):
        await interaction.response.defer(ephemeral=True)

        with open("json/settings.json", "r") as f:
            settings_data = json.load(f)

        settings_data[str(interaction.guild.id)]["standard_avatar_check"] = status
        with open("json/settings.json", "w") as f:
            json.dump(settings_data, f, indent=4)

        embed = disnake.Embed(
            # title="Default Avatar Detection System",
            description=f"> DADS has been set to `{status}`",
            color=disnake.Color.green()
        )
        embed.set_footer(text="DADS = Default Avatar Detection System")

        await interaction.edit_original_message(embed=embed)

    @antialt_avatar.sub_command(name="get", description="Get the current option for the default avatar detection system")
    async def antialt_get(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        with open("json/settings.json", "r") as f:
            settings_data = json.load(f)

        embed = disnake.Embed(
            # title="Default Avatar Detection System Info",
            description=f"> DADS is set to `{settings_data[str(interaction.guild.id)]['standard_avatar_check']}`",
            color=disnake.Color.yellow()
        )
        embed.set_footer(text="DADS = Default Avatar Detection System")

        await interaction.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(AntiAlt(bot))
