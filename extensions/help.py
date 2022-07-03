from typing import Optional

import disnake
from disnake.ext import commands


class Help(commands.Cog):
    '''
    Gives out this help command
    '''
    def __init__(
        self,
        bot
    ):
        self.bot = bot

    @commands.slash_command(
        description="Shows help for a command"
    )
    async def help(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        cog: (Optional[str]) = None
        # command: (Optional[str]) = None
    ):
        lol_embed = disnake.Embed(
            description="Gettings everything ready...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=lol_embed,
            ephemeral=True
        )

        embed = disnake.Embed(
            title="Help",
            description="This is the help command. Use `/help <cog>` to get help for a command.",
            color=interaction.author.color
        )

        # cog_name = [name for name in self.bot.cogs]
        # cog_with_cmd = [cog_name for cog in self.bot.cogs.values() if len(cog.get_commands()) > 0]

        # for _cog in cog_with_cmd:
        #     help_embed.add_field(
        #         name=f"{_cog.qualified_name}",
        #         value=f"{_cog.description}",
        #         inline=False
        #     )

        if not cog:  # and not command:
            cog_filter = [
                cog for cog in self.bot.cogs.values() if len(cog.get_application_commands()) > 0
            ]

            for cog in cog_filter:
                # emoji = getattr(cog, "COG_EMOJI", None)
                embed.add_field(
                    name=f"__{cog.qualified_name}__",
                    value=f"`{cog.description if cog.description else 'No description'}`",
                    inline=False
            )

                await interaction.edit_original_message(
                    embed=embed
                )

        elif cog:  # and not command:

            __cog = self.bot.get_cog(cog)

            if not __cog:
                error_embed = disnake.Embed(
                    description=f"Did not found the cog you requested (`{cog}`)",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=error_embed
                )

            else:
                cog_embed = disnake.Embed(
                    title=f"__{__cog.qualified_name}__",
                    description=f"`{__cog.description if __cog.description else 'No description'}`",
                    color=interaction.author.color
                )
                cmd_list = []
                for cmd in __cog.get_application_commands():
                    cmd_list.append(f" - `{cmd.qualified_name}`\n")

                cog_embed.add_field(
                    name="__Commands__",
                    value="".join(cmd_list),
                )
                await interaction.edit_original_message(
                    embed=cog_embed
                )

                # for command in __cog.get_application_commands():
                #     cog_embed.add_field(
                #         name=f"- {command.qualified_name}",
                #         # value=f"`»` `{command.description if command.description else 'No description'}`",
                #         value="`»` `No description`",
                #         inline=False
                #     )

        # elif command and not cog:
            # return

            # cmd = self.bot.get_slash_command(command)

            # help_embed = disnake.Embed(
            #     title=f"__{cmd.qualified_name}__",
            #     description=f"`»` `{cmd.description}`",
            #     color=interaction.author.color
            # )

            # if cmd.subcommand_group:
            #     help_embed.add_field(
            #         name="__Subcommands__",
            #         value="\n - ".join(f"`{cmd.qualified_name}`"),
            #         inline=False
            #     )
            #     await interaction.edit_original_message(
            #         embed=help_embed
            #     )

            # else:
            # help_embed.add_field(
            #     name="> ❓ Syntax",
            #     value=f"`»` `/{cmd.qualified_name}`",
            #     inline=False
            # )
            # await interaction.edit_original_message(
            #     embed=help_embed
            # )

        # else:
        #     pass

    class Help2(commands.Cog):
        def __init__(
            self,
            bot
        ):
            self.bot = bot

        @commands.slash_command(
            name="help2",
            description="Shows help for a command"
        )
        async def help(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            cog: (Optional[str]) = None,
            command: (Optional[str]) = None
        ):
            if not command and not cog:
                embed = disnake.Embed(
                    title="Help",
                    description="This is the help command. Use `/help <command>` to get help for a command.",
                    color=interaction.author.color
                )

                for cog in self.bot.cogs.values():
                    if len(cog.get_commands()) > 0:
                        embed.add_field(
                            name=f"__{cog.qualified_name}__",
                            value=f"`{cog.description if cog.description else 'No description'}`",
                            inline=False
                        )

                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True
                )

            if not command:
                __cog = self.bot.get_cog(cog)

                if not __cog:
                    error_embed = disnake.Embed(
                        description=f"Did not found the cog, you requested (`{cog}`)",
                        color=disnake.Color.red()
                    )
                    await interaction.response.send_message(
                        embed=error_embed,
                        ephemeral=True
                    )

                else:
                    embed = disnake.Embed(
                        title=f"__{__cog.qualified_name}__",
                        description=f"`{__cog.description if __cog.description else 'No description'}`",
                        color=interaction.author.color
                    )

                    for command in __cog.walk_commands():
                        embed.add_field(
                            name=f"- {command.qualified_name}",
                            value=f"`»` `{command.description if command.description else 'No description'}`",
                            inline=False
                        )

                    await interaction.response.send_message(
                        embed=embed,
                        ephemeral=True
                    )

            elif not cog:
                return
                cmd = self.bot.get_slash_command(command)

                embed = disnake.Embed(
                    title=f"__{cmd.parent}__",
                    description=f"`{[cmd.description if cmd.description else 'No description']}`",
                    color=interaction.author.color
                )

                embed.add_field(
                    name="__Subcommands__",
                    value="\n - ".join(f"`{cmd.qualified_name}`"),
                    inline=False
                )
                await interaction.response.send_message(
                    embed=embed,
                    ephemeral=True
                )


def setup(bot):
    bot.add_cog(Help(bot))
