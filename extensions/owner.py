import disnake
from disnake.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="load",
        description="Loads a module"
    )
    @commands.is_owner()
    async def load(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        module: str
    ):
        self.bot.load_extension(f"extensions.{module}")

        load_embed = disnake.Embed(
            description=f"Successfully loaded `{module}`",
            color=disnake.Color.green()
        )

        await interaction.response.send_message(
            embed=load_embed,
            ephemeral=True
        )

    @commands.slash_command(
        name="unload",
        description="Unloads a module"
    )
    @commands.is_owner()
    async def unload(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        module: str
    ):
        self.bot.unload_extension(f"extensions.{module}")

        unload_embed = disnake.Embed(
            description=f"Successfully unloaded `{module}`",
            color=disnake.Color.green()
        )

        await interaction.response.send_message(
            embed=unload_embed,
            ephemeral=True
        )

    @commands.slash_command(
        name="eval",
        description="Evaluates a code"
    )
    @commands.is_owner()
    async def eval(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        code: str
    ):
        try:
            result = eval(code)
            result_embed = disnake.Embed(
                description=f"`{result}`",
                color=disnake.Color.green()
            )
        except Exception as e:
            result_embed = disnake.Embed(
                description=f"`{e}`",
                color=disnake.Color.red()
            )

        await interaction.response.send_message(
            embed=result_embed,
            ephemeral=True
        )


def setup(bot):
    bot.add_cog(Owner(bot))
