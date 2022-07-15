import disnake
from disnake.ext import commands


class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_guild = 935539295580717067
        self.bot_owner = 493370963807830016
        self.category = 997632888256348270
        self.suggest_channel = 997632979109154930
        self.bug_channel = 997632989653647421

    @commands.slash_command(
        description="Suggest something to the bot"
    )
    async def suggest(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @suggest.sub_command(name="idea", description="Command to suggest an idea")
    async def suggest_idea(self, interaction: disnake.ApplicationCommandInteraction, *, idea: str):
        await interaction.response.send_message(
            "Suggestion sent to the bot owner successfully!",
            ephemeral=True
        )
        sugest_channel = self.bot.get_channel(self.suggest_channel)

        embed = disnake.Embed(
            title="Suggestion :bell: ",
            description=f"{idea}",
            color=disnake.Color.green()
        )
        embed.set_author(
            name=interaction.author.name,
            icon_url=interaction.author.avatar.url
        )
        embed.set_footer(
            text=f"ID: {interaction.author.id}"
        )
        message = await sugest_channel.send(embed=embed)

        await message.add_reaction("✅")
        await message.add_reaction("❌")

    @suggest.sub_command(name="bug", description="Command to report a bug")
    async def suggest_bug(self, interaction: disnake.ApplicationCommandInteraction, *, bug: str):
        await interaction.response.send_message(
            "Bug report sent to the bot owner successfully!",
            ephemeral=True
        )
        bug_report_channel = self.bot.get_channel(self.bug_channel)

        embed = disnake.Embed(
            title="Bug Report :bell: ",
            description=f"{bug}",
            color=disnake.Color.red()
        )
        embed.set_author(
            name=interaction.author.name,
            icon_url=interaction.author.avatar.url
        )
        embed.set_footer(
            text=f"ID: {interaction.author.id}"
        )
        message = await bug_report_channel.send(embed=embed)

        await message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Suggest(bot))
