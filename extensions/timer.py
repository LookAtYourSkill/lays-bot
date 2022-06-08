import disnake
from disnake.ext import commands
import humanize
import asyncio


class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="timer", description="Creates a timer for yourself or a user")
    async def timer(interaction: disnake.ApplicationCommandInteraction, time: int, member: disnake.Member = None, *, message: str):
        if member is None:
            member = interaction.author

        embed = disnake.Embed(
            title="Timer",
            description=f"{interaction.author.mention} set a timer for `{humanize.naturaldelta(time)}`. I will remind you when its finished!",
            color=disnake.Color.green()
        )
        embed.add_field(
            name="Message",
            value=f"`{message}`",
            inline=False
        )
        embed.add_field(
            name="Member",
            value=member.mention,
            inline=False
        )
        embed.set_author(
            name=interaction.author.name,
            icon_url=interaction.author.avatar.url
        )
        await interaction.response.send_message(
            embed=embed
        )

        await asyncio.sleep(time)

        finish_embed = disnake.Embed(
            description=f"{member.mention}'s timer has finished!",
            color=disnake.Color.green()
        )

        await interaction.edit_original_message(
            embed=finish_embed,
            content=f"{member.mention} | {interaction.author.mention}"
        )


def setup(bot):
    bot.add_cog(Timer(bot))
