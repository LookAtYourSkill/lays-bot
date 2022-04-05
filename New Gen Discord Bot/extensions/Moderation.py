import disnake
from disnake.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Bans a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, reason=None, delete_message_days: int = None):
        await inter.guild.ban(user=user, reason=None if not reason else reason, delete_message_days=1 if not delete_message_days else delete_message_days)
        ban_embed = disnake.Embed(
            description=f'Der User `{user}` [`{user.id}`] wurde wegen `{reason}` **erfolgreich** von `{inter.author}` **gebannt**! Die **Nachrichten** von `{delete_message_days} Tage/n` **wurden gelöscht**.',
            color=disnake.Color.green()
        )
        await inter.response.send_message(
            embed=ban_embed,
            ephemeral=True
        )

    @commands.slash_command(description='Unban a banned user')
    @commands.has_permissions(ban_members=True)
    async def unban(self, inter: disnake.ApplicationCommandInteraction, user):
        if not user.isdigit():
            banned_users = await inter.guild.bans()
            member_name, member_discriminator = user.split("#")
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await inter.guild.unban(user)

                    unban_embed = disnake.Embed(
                        description=f'Der User `{user}` [`{user.id}`] wurde von `{inter.author}` entbannt.',
                        color=disnake.Color.green()
                    )
                    await inter.response.send_message(
                        embed=unban_embed,
                        ephemeral=True
                    )

        elif user.isdigit():
            user_id = await self.bot.fetch_user(user)
            await inter.guild.unban(user_id)

            unban_embed = disnake.Embed(
                description=f'Der User `{user_id}` [`{user}`] wurde von `{inter.author}` entbannt.',
                color=disnake.Color.green()
            )
            await inter.response.send_message(
                embed=unban_embed,
                ephemeral=True
            )

    @commands.slash_command(description='clears messages')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter: disnake.ApplicationCommandInteraction, limit: int):
            check_func = lambda msg: not msg.pinned
            await inter.channel.purge(
                limit=limit,
                check=check_func
            )
            purge_embed = disnake.Embed(
                description=f'Es wurden `{limit} Nachrichten` erfolgreich gelöscht!',
                color=disnake.Color.red()
            )
            await inter.response.send_message(
                embed=purge_embed,
                ephemeral=True
            )


def setup(bot):
    bot.add_cog(Moderation(bot))
