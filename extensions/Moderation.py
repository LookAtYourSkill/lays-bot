import disnake
from disnake.ext import commands
from disnake.ext.tasks import loop
import humanfriendly
import datetime
import humanize
import json


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
        try:
            await interaction.guild.ban(
                user=user,
                reason=None if not reason else reason,
                delete_message_days=1 if not delete_message_days else delete_message_days
            )
            ban_embed = disnake.Embed(
                description=f"Der User `{user}` [`{user.id}`] wurde wegen `{reason}` erfolgreich von `{interaction.author}` **gebannt**! Die Nachrichten von `{delete_message_days} Tag/en` wurden **gelöscht**.",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=ban_embed,
                ephemeral=True
            )
        except disnake.errors.Forbidden:
            await interaction.response.send_message(
                "Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen!",
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
                    try:
                        await interaction.guild.unban(user)

                        unban_embed = disnake.Embed(
                            description=f"Der User `{user}` [`{user.id}`] wurde von `{interaction.author}` entbannt.",
                            color=disnake.Color.green()
                        )
                        await interaction.response.send_message(
                            embed=unban_embed,
                            ephemeral=True
                        )
                    except disnake.errors.Forbidden:
                        await interaction.response.send_message(
                            "Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen!",
                            ephemeral=True
                        )

        elif user.isdigit():
            user_id = await self.bot.fetch_user(user)
            try:
                await interaction.guild.unban(user_id)

                unban_embed = disnake.Embed(
                    description=f"Der User `{user_id}` [`{user}`] wurde von `{interaction.author}` entbannt.",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=unban_embed,
                    ephemeral=True
                )
            except disnake.errors.Forbidden:
                await interaction.response.send_message(
                    "Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen!",
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
        try:
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
        except disnake.errors.Forbidden:
            await interaction.response.send_message(
                "Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen!",
                ephemeral=True
            )

    @commands.slash_command(
        name="clear",
        description="Clears a channel",
        options=[
            disnake.Option(
                name="amount",
                description="The amount of messages to delete",
                required=True,
                min_value=1,
                max_value=100
            ),
            disnake.Option(
                name="type",
                description="What kind do you want to clear?",
                required=True,
                choices=[
                    disnake.OptionChoice(
                        name="embeds",
                        value="delete all embeds within your limit"
                    ),
                    disnake.OptionChoice(
                        name="pinned",
                        value="delete all pinned messages within your limit"
                    ),
                    disnake.OptionChoice(
                        name="messages",
                        value="delete all message within your limit"
                    ),
                    disnake.OptionChoice(
                        name="images",
                        value="delete all images within your limit"
                    )
                ]
            )
        ]
    )
    @commands.has_permissions(
        manage_messages=True
    )
    async def clear(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        amount: int,
        type: str
    ):

        if type == "embeds":
            check = lambda msg: msg.embeds

            await interaction.channel.purge(

                limit=amount,
                check=check
            )
            if amount == 1:
                purge_embed = disnake.Embed(
                    description="Es wurde `1 Embed` erfolgreich gelöscht!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=purge_embed,
                    ephemeral=True
                )
            else:
                purge_embed = disnake.Embed(
                    description=f"Es wurden `{amount} Embeds` erfolgreich gelöscht!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=purge_embed,
                    ephemeral=True
                )

        elif type == "pinned":
            check = lambda msg: msg.pinned and not msg.embeds

            await interaction.channel.purge(

                limit=amount,
                check=check
            )
            if amount == 1:
                purge_embed = disnake.Embed(
                    description="Es wurde `1 gepinnte Nachricht` erfolgreich gelöscht!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=purge_embed,
                    ephemeral=True
                )
            else:
                purge_embed = disnake.Embed(
                    description=f"Es wurden `{amount} gepinnte Nachrichten` erfolgreich gelöscht!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=purge_embed,
                    ephemeral=True
                )

        elif type == "messages":
            check = lambda msg: not msg.pinned and not msg.embeds

            await interaction.channel.purge(

                limit=amount,
                check=check
            )

            if amount == 1:
                purge_embed = disnake.Embed(
                    description="Es wurde `1 Nachricht` erfolgreich gelöscht!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=purge_embed,
                    ephemeral=True
                )
            else:
                purge_embed = disnake.Embed(
                    description=f"Es wurden `{amount} Nachrichten` erfolgreich gelöscht!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=purge_embed,
                    ephemeral=True
                )

        elif type == "images":
            check = lambda msg: not msg.pinned and msg.attachments

            await interaction.channel.purge(

                limit=amount,
                check=check
            )
            if amount == 1:
                purge_embed = disnake.Embed(
                    description="Es wurde `1 Bild` erfolgreich gelöscht!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=purge_embed,
                    ephemeral=True
                )
            else:
                purge_embed = disnake.Embed(
                    description=f"Es wurden `{amount} Bilder` erfolgreich gelöscht!",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=purge_embed,
                    ephemeral=True
                )

    @loop(seconds=90)
    async def check_streams(self):
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)



def setup(bot):
    bot.add_cog(Moderation(bot))
