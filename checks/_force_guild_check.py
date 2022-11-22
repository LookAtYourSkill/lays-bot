import disnake
from disnake.ext import commands


def right_guild(target_id: disnake.Guild):
    def predicate(interaction: disnake.ApplicationCommandInteraction) -> bool:
        guild = interaction.guild.id
        if guild == target_id and interaction.user.guild_permissions.administrator:
            return True
        else:
            raise commands.CheckFailure("You are not allowed to use this command.")
    return commands.check(predicate)
