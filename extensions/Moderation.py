import disnake
from disnake.ext import commands
import humanfriendly
import datetime

import humanize


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="ban",
        description="Bans a user"
    )
    @commands.has_permissions(
        ban_members=True
    )
    async def ban(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user: disnake.User,
        reason=None,
        delete_message_days: int = None
    ):
        await interaction.guild.ban(
            user=user,
            reason=None if not reason else reason,
            delete_message_days=1 if not delete_message_days else delete_message_days
        )
        ban_embed = disnake.Embed(
            description=f"Der User `{user}` [`{user.id}`] wurde wegen `{reason}` erfolgreich von `{interaction.author}` **gebannt**! Die Nachrichten von `{delete_message_days} Tage/n` wurden **gelöscht**.",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=ban_embed,
            ephemeral=True
        )

    @commands.slash_command(
        name="unban",
        description="Unban a banned user"
    )
    @commands.has_permissions(
        ban_members=True
    )
    async def unban(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user
    ):
        if not user.isdigit():
            banned_users = await interaction.guild.bans()
            member_name, member_discriminator = user.split("#")
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await interaction.guild.unban(user)

                    unban_embed = disnake.Embed(
                        description=f"Der User `{user}` [`{user.id}`] wurde von `{interaction.author}` entbannt.",
                        color=disnake.Color.green()
                    )
                    await interaction.response.send_message(
                        embed=unban_embed,
                        ephemeral=True
                    )

        elif user.isdigit():
            user_id = await self.bot.fetch_user(user)
            await interaction.guild.unban(user_id)

            unban_embed = disnake.Embed(
                description=f"Der User `{user_id}` [`{user}`] wurde von `{interaction.author}` entbannt.",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=unban_embed,
                ephemeral=True
            )

    @commands.slash_command(
        name="timeout",
        description="Timeouts a user"
    )
    @commands.has_permissions(kick_members=True)
    async def timeout(
        interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        time: str,
        reason=str
    ):
        time = humanfriendly.parse_timespan(time)
        await member.timeout(
            until=disnake.utils.utcnow() + datetime.timedelta(seconds=time),
            reason=reason
        )
        timeout_embed = disnake.Embed(
            description=f"Der User {member.mention} [`{member.id}`] wurde von {interaction.author.mention} [`{interaction.author.id}`] für `{humanize.precisedelta(time)}` getimed!",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=timeout_embed,
            ephemeral=True
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
