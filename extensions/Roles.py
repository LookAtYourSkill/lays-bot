import json

import disnake
from disnake.ext import commands

from checks._check_license import check_license


class Roles(commands.Cog):
    '''
    Role management for users per chat
    '''
    def __init__(self, bot):
        self.bot = bot

    @check_license()
    @commands.slash_command(
        name="role",
        description="Manage roles for users per chat"
    )
    async def role(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @role.sub_command(description="Add/Remove a role to/from somebody")
    @commands.has_permissions(manage_roles=True)
    async def manage_role(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        role: disnake.Role,
        reason="Role remove/add per Command"
    ):
        loading_embed = disnake.Embed(
            description="Fetching roles from user...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        if interaction.author.top_role.position > role.position:
            if role in member.roles:
                await member.remove_roles(role, reason=reason)
                remove_embed = disnake.Embed(
                    description=f"{member.mention} wurde die Rolle `{role}` entfernt!",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=remove_embed
                )
            elif role not in member.roles:
                await member.add_roles(role, reason=reason)
                add_embed = disnake.Embed(
                    description=f"{member.mention} wurde die Rolle `{role}` hinzugefügt ✅",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=add_embed
                )
            else:
                top_role_under_role_embed = disnake.Embed(
                    description=f"Deine Höchste Rolle [`{interaction.author.top_role}`] ist niedriger als die Rolle [`{role}`], die du hinzufügen möchtest ❌",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=top_role_under_role_embed
                )

        elif role not in interaction.guild.roles:
            not_role_embed = disnake.Embed(
                description=f"Die Rolle `{role}` konnte auf diesen Server nicht gefunden werden ❌"
            )
            await interaction.edit_original_message(
                embed=not_role_embed
            )

        else:
            top_role_under_role_embed = disnake.Embed(
                description=f"Deine Höchste Rolle [`{interaction.author.top_role}`] ist niedriger als die Rolle [`{role}`], die du hinzufügen möchtest ❌",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=top_role_under_role_embed
            )


def setup(bot):
    bot.add_cog(Roles(bot))
