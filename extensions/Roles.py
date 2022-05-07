import disnake
from disnake.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Add/Remove a role to/from somebody")
    async def role(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        role: disnake.Role,
        reason="Role remove/add per Command"
    ):
        if interaction.author.top_role.position > role.position:
            if role in member.roles:
                await member.remove_roles(role, reason=reason)
                remove_embed = disnake.Embed(
                    description=f"{member.mention} wurde die Rolle `{role}` entfernt!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=remove_embed,
                    ephemeral=True
                )
            elif role not in member.roles:
                await member.add_roles(role, reason=reason)
                add_embed = disnake.Embed(
                    description=f"{member.mention} wurde die Rolle `{role}` hinzugefügt!",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=add_embed,
                    ephemeral=True
                )
            else:
                top_role_under_role_embed = disnake.Embed(
                    description=f"Deine Höchste Rolle [`{interaction.author.top_role}`] ist niedriger als die Rolle [`{role}`], die du hinzufügen möchtest",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=top_role_under_role_embed,
                    ephemeral=True
                )

        elif role not in interaction.guild.roles:
            not_role_embed = disnake.Embed(
                description=f"Die Rolle `{role}` konnte auf diesen Server nicht gefunden werden!"
            )
            await interaction.response.send_message(
                embed=not_role_embed,
                ephemeral=True
            )

        else:
            top_role_under_role_embed = disnake.Embed(
                description=f"Deine Höchste Rolle [`{interaction.author.top_role}`] ist niedriger als die Rolle [`{role}`], die du hinzufügen möchtest",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=top_role_under_role_embed,
                ephemeral=True
            )


def setup(bot):
    bot.add_cog(Roles(bot))
