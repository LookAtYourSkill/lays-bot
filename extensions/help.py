from typing import Optional
from enum import Enum

import disnake
from disnake.ext import commands


class Cogs(str, Enum):
    About = "About"
    AntiAlt = "AntiAlt"
    Changelog = "Changelog"
    Help = "Help"
    Info = "Info"
    JoinToCreate = "joinToCreate"
    LicenseSystem = "LicenseSystem"
    Meme = "Meme"
    Moderation = "Moderation"
    Owner = "Owner"
    Roles = "Roles"
    Setup = "Setup"
    Suggest = "Suggest"
    Change = "Change"
    TicketSystem = "TicketSystem"
    Timer = "Timer"
    Twitch = "Twitch"
    Twitter = "Twitter"


class Help(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot

    @commands.slash_command(
        description="Shows help for a command"
    )
    async def help(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        cog: (Optional[str]) = commands.Param(
            None,
            name="cog",
            description="Chose the cog you want help from!",
            choices=Cogs,
        )
        # command: (Optional[str]) = None
    ):
        cog: commands.Cog

        await interaction.response.defer(ephemeral=True)

        lol_embed = disnake.Embed(
            description="Gettings everything ready...",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=lol_embed
        )

        embed = disnake.Embed(
            title="Help",
            description="This is the help command. Use `/help` to get help for an extension.",
            color=interaction.author.color
        )

        # check if the cog is set
        if not cog:  # and not command:
            # filter cogs that have minimal one command in it
            cog_filter = [
                cog for cog in self.bot.cogs.values() if len(cog.get_application_commands()) > 0
            ]
            cog_list = []

            # going through all cogs
            for cog in cog_filter:
                # emoji = getattr(cog, "COG_EMOJI", None)
                # add a field for the cog
                cog_list.append("- `{!s:15s}` | `{!s:25s}`\n".format(cog.qualified_name, cog.description))
                # cog_list.append(f"- `{cog.qualified_name}` | `{cog.description}`\n")

            embed.add_field(
                name=f"__All cogs ({len(cog_list)})__",
                value=f"{' '.join(cog_list)}",
                inline=False
            )

            await interaction.edit_original_message(
                embed=embed
            )

        # check if cog is set
        elif cog:  # and not command:

            # get the cog
            __cog = self.bot.get_cog(cog)

            # check if cog exists
            if not __cog:
                error_embed = disnake.Embed(
                    description=f"Did not found the cog you requested (`{cog}`)",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=error_embed
                )

            else:
                # ! print([i.qualified_name for i in __cog.get_application_commands()])
                # if cog exists
                cog_embed = disnake.Embed(
                    # get the name of the cog
                    title=f"__{__cog.qualified_name}__",
                    # get the description of the cog if it have one
                    description=f"`{__cog.description or 'Cog has no description'}`\n",
                    #  description=f"`{__cog.description if __cog.description else '`No description`'}`",
                    color=interaction.author.color
                )
                # get all commands of the cog
                cmd_list = []
                # loop through all slash commands
                # for cmd in __cog.get_application_commands():
                for cmd in __cog.get_application_commands():
                    # check if qualified name is longer than one word
                    if len(cmd.qualified_name.split()) > 1:
                        # if it is, add the command to the list
                        cmd_list.append(f" - `{cmd.qualified_name}`\n")

                # add the list of commands to the embed
                cog_embed.add_field(
                    name="__Commands__",
                    value=f"{' '.join(cmd_list)}",
                )

                await interaction.edit_original_message(
                    embed=cog_embed
                )


def setup(bot):
    bot.add_cog(Help(bot))
