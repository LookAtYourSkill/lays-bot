import asyncio
import json

import disnake
import humanize
from disnake.ext import commands


class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="timer", description="Creates a timer for yourself or a user")
    async def timer(interaction: disnake.ApplicationCommandInteraction, time: int, member: disnake.Member = None, *, message: str):
        with open("json/general.json", "r") as general_info:
            general = json.load(general_info)
        with open("json/guild.json", "r") as guild_info:
            guilds = json.load(guild_info)
        with open("json/licenses.json", "r") as license_info:
            licenses = json.load(license_info)

        if not general["license_check"]:
            if not guilds[str(interaction.author.guild.id)]["license"] or guilds[str(interaction.author.guild.id)]["license"] not in licenses:
                no_licesnse_embed = disnake.Embed(
                    title="No license ⛔",
                    description="You have not set a license for this server. Please use `/license activate <license>` to set a license.",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=no_licesnse_embed,
                    ephemeral=True
                )

            else:
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

        else:
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
