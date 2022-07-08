import asyncio
import datetime
import json

import disnake
import humanfriendly
import humanize
from disnake.ext import commands


class Moderation(commands.Cog):
    '''
    Moderation command to manage users
    '''
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
                loading_embed = disnake.Embed(
                    description="Preparing to ban the member...",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=loading_embed,
                    ephemeral=True
                )

                try:
                    await interaction.guild.ban(
                        user=user,
                        reason=None if not reason else reason,
                        delete_message_days=1 if not delete_message_days else delete_message_days
                    )
                    ban_embed = disnake.Embed(
                        description=f"Der User `{user}` [`{user.id}`] wurde wegen `{reason}` erfolgreich von `{interaction.author}` **gebannt**! Die Nachrichten von `{delete_message_days} Tag/en` wurden **gelöscht** ✅",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=ban_embed
                    )
                except disnake.errors.Forbidden:
                    await interaction.edit_original_message(
                        content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
                    )

        else:
            loading_embed = disnake.Embed(
                description="Preparing to ban the member...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )

            try:
                await interaction.guild.ban(
                    user=user,
                    reason=None if not reason else reason,
                    delete_message_days=1 if not delete_message_days else delete_message_days
                )
                ban_embed = disnake.Embed(
                    description=f"Der User `{user}` [`{user.id}`] wurde wegen `{reason}` erfolgreich von `{interaction.author}` **gebannt**! Die Nachrichten von `{delete_message_days} Tag/en` wurden **gelöscht** ✅",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=ban_embed
                )
            except disnake.errors.Forbidden:
                await interaction.edit_original_message(
                    content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
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
                loading_embed = disnake.Embed(
                    description="Preparing to unban the member...",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=loading_embed,
                    ephemeral=True
                )
                if not user.isdigit():
                    banned_users = await interaction.guild.bans()
                    member_name, member_discriminator = user.split("#")
                    for ban_entry in banned_users:
                        user = ban_entry.user
                        if (user.name, user.discriminator) == (member_name, member_discriminator):
                            try:
                                await interaction.guild.unban(user)

                                unban_embed = disnake.Embed(
                                    description=f"Der User `{user}` [`{user.id}`] wurde von `{interaction.author}` entbannt ✅",
                                    color=disnake.Color.green()
                                )
                                await interaction.edit_original_message(
                                    embed=unban_embed
                                )
                            except disnake.errors.Forbidden:
                                await interaction.edit_original_message(
                                    content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
                                )
                elif user.isdigit():
                    user_id = await self.bot.fetch_user(user)
                    try:
                        await interaction.guild.unban(user_id)

                        unban_embed = disnake.Embed(
                            description=f"Der User `{user_id}` [`{user}`] wurde von `{interaction.author}` entbannt ✅",
                            color=disnake.Color.green()
                        )
                        await interaction.edit_original_message(
                            embed=unban_embed
                        )
                    except disnake.errors.Forbidden:
                        await interaction.edit_original_message(
                            content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
                        )

        else:
            loading_embed = disnake.Embed(
                description="Preparing to unban the member...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )
            if not user.isdigit():
                banned_users = await interaction.guild.bans()
                member_name, member_discriminator = user.split("#")
                for ban_entry in banned_users:
                    user = ban_entry.user
                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        try:
                            await interaction.guild.unban(user)

                            unban_embed = disnake.Embed(
                                description=f"Der User `{user}` [`{user.id}`] wurde von `{interaction.author}` entbannt ✅",
                                color=disnake.Color.green()
                            )
                            await interaction.edit_original_message(
                                embed=unban_embed
                            )
                        except disnake.errors.Forbidden:
                            await interaction.edit_original_message(
                                content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
                            )

            elif user.isdigit():
                user_id = await self.bot.fetch_user(user)
                try:
                    await interaction.guild.unban(user_id)

                    unban_embed = disnake.Embed(
                        description=f"Der User `{user_id}` [`{user}`] wurde von `{interaction.author}` entbannt ✅",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=unban_embed
                    )
                except disnake.errors.Forbidden:
                    await interaction.edit_original_message(
                        content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
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
        reason: str
    ):
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
                loading_embed = disnake.Embed(
                    description="Preparing to timeout the member...",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=loading_embed,
                    ephemeral=True
                )

                time = humanfriendly.parse_timespan(time)
                try:
                    await member.timeout(
                        until=disnake.utils.utcnow() + datetime.timedelta(seconds=time),
                        reason=reason
                    )
                    timeout_embed = disnake.Embed(
                        description=f"Der User {member.mention} [`{member.id}`] wurde von {interaction.author.mention} [`{interaction.author.id}`] für `{humanize.precisedelta(time)}` getimed ✅",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=timeout_embed
                    )

                    await asyncio.sleep(time)
                    await member.timeout(
                        until=None,
                        reason="Timeout Expired"
                    )

                except disnake.errors.Forbidden:
                    await interaction.edit_original_message(
                        content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
                    )

        else:
            loading_embed = disnake.Embed(
                description="Preparing to timeout the member...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )

            time = humanfriendly.parse_timespan(time)
            try:
                await member.timeout(
                    until=disnake.utils.utcnow() + datetime.timedelta(seconds=time),
                    reason=reason
                )
                timeout_embed = disnake.Embed(
                    description=f"Der User {member.mention} [`{member.id}`] wurde von {interaction.author.mention} [`{interaction.author.id}`] für `{humanize.precisedelta(time)}` getimed ✅",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=timeout_embed
                )

                await asyncio.sleep(time)
                await member.timeout(
                    until=None,
                    reason="Timeout Expired"
                )

            except disnake.errors.Forbidden:
                await interaction.edit_original_message(
                    content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
                )

    @commands.slash_command(
        name="untimeout",
        description="Timeouts a user"
    )
    @commands.has_permissions(kick_members=True)
    async def untime(
        interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member
    ):
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
                loading_embed = disnake.Embed(
                    description="Preparing to timeout the member...",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=loading_embed,
                    ephemeral=True
                )

                try:
                    await member.timeout(
                        until=disnake.utils.utcnow()
                    )
                    timeout_embed = disnake.Embed(
                        description=f"Der User {member.mention} [`{member.id}`] wurde von {interaction.author.mention} [`{interaction.author.id}`] entimed ✅",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=timeout_embed
                    )
                except disnake.errors.Forbidden:
                    await interaction.edit_original_message(
                        content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
                    )

        else:
            loading_embed = disnake.Embed(
                description="Preparing to timeout the member...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )

            try:
                await member.timeout(
                    until=disnake.utils.utcnow()
                )
                timeout_embed = disnake.Embed(
                    description=f"Der User {member.mention} [`{member.id}`] wurde von {interaction.author.mention} [`{interaction.author.id}`] entimed ✅",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_message(
                    embed=timeout_embed
                )
            except disnake.errors.Forbidden:
                await interaction.edit_original_message(
                    content="Etwas ist schliefgelaufen, es tut mir leid, dass solche Unannehmlichkeiten vorkommen ⛔"
                )

    @commands.slash_command(invoke_without_command=True)
    async def clear(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        pass

    @clear.sub_command(description="Clears embed in a channel")
    async def embeds(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        amount: int
    ):
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
                loading_embed = disnake.Embed(
                    description=f"Deleting {amount} embeds...",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=loading_embed,
                    ephemeral=True
                )

                check = lambda msg: msg.embeds

                await interaction.channel.purge(

                    limit=amount,
                    check=check
                )
                if amount == 1:
                    purge_embed = disnake.Embed(
                        description="Es wurde `1 Embed` erfolgreich gelöscht ✅",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=purge_embed
                    )
                else:
                    purge_embed = disnake.Embed(
                        description=f"Es wurden `{amount} Embeds` erfolgreich gelöscht ✅",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=purge_embed
                    )

        else:

            loading_embed = disnake.Embed(
                description=f"Deleting {amount} embeds...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )

            check = lambda msg: msg.embeds

            await interaction.channel.purge(

                limit=amount,
                check=check
            )
            if amount == 1:
                purge_embed = disnake.Embed(
                    description="Es wurde `1 Embed` erfolgreich gelöscht ✅",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=purge_embed
                )
            else:
                purge_embed = disnake.Embed(
                    description=f"Es wurden `{amount} Embeds` erfolgreich gelöscht ✅",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=purge_embed
                )

    @clear.sub_command(description="Clears pinned messages in a channel")
    async def pinned(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        amount: int
    ):
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
                loading_embed = disnake.Embed(
                    description=f"Deleting {amount} pinned messages...",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=loading_embed,
                    ephemeral=True
                )

                check = lambda msg: msg.pinned and not msg.embeds

                await interaction.channel.purge(

                    limit=amount,
                    check=check
                )
                if amount == 1:
                    purge_embed = disnake.Embed(
                        description="Es wurde `1 gepinnte Nachricht` erfolgreich gelöscht ✅",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=purge_embed,
                        ephemeral=True
                    )
                else:
                    purge_embed = disnake.Embed(
                        description=f"Es wurden `{amount} gepinnte Nachrichten` erfolgreich gelöscht ✅",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=purge_embed,
                        ephemeral=True
                    )

        else:
            loading_embed = disnake.Embed(
                description=f"Deleting {amount} pinned messages...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )

            check = lambda msg: msg.pinned and not msg.embeds

            await interaction.channel.purge(

                limit=amount,
                check=check
            )
            if amount == 1:
                purge_embed = disnake.Embed(
                    description="Es wurde `1 gepinnte Nachricht` erfolgreich gelöscht ✅",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=purge_embed,
                    ephemeral=True
                )
            else:
                purge_embed = disnake.Embed(
                    description=f"Es wurden `{amount} gepinnte Nachrichten` erfolgreich gelöscht ✅",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=purge_embed,
                    ephemeral=True
                )

    @clear.sub_command(description="Clears all messages in a channel")
    async def messages(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        amount: int
    ):
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
                loading_embed = disnake.Embed(
                    description=f"Deleting {amount} messages...",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=loading_embed,
                    ephemeral=True
                )

                check = lambda msg: not msg.pinned and not msg.embeds

                await interaction.channel.purge(

                    limit=amount,
                    check=check
                )

                if amount == 1:
                    purge_embed = disnake.Embed(
                        description="Es wurde `1 Nachricht` erfolgreich gelöscht ✅",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=purge_embed
                    )
                else:
                    purge_embed = disnake.Embed(
                        description=f"Es wurden `{amount} Nachrichten` erfolgreich gelöscht ✅",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=purge_embed
                    )

        else:
            loading_embed = disnake.Embed(
                description=f"Deleting {amount} messages...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )

            check = lambda msg: not msg.pinned and not msg.embeds

            await interaction.channel.purge(

                limit=amount,
                check=check
            )

            if amount == 1:
                purge_embed = disnake.Embed(
                    description="Es wurde `1 Nachricht` erfolgreich gelöscht ✅",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=purge_embed
                )
            else:
                purge_embed = disnake.Embed(
                    description=f"Es wurden `{amount} Nachrichten` erfolgreich gelöscht ✅",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=purge_embed
                )

    @clear.sub_command(description="Clears images in a channel")
    async def images(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        amount: int
    ):
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
                loading_embed = disnake.Embed(
                    description=f"Deleting {amount} images...",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=loading_embed,
                    ephemeral=True
                )

                check = lambda msg: not msg.pinned and msg.attachments

                await interaction.channel.purge(

                    limit=amount,
                    check=check
                )
                if amount == 1:
                    purge_embed = disnake.Embed(
                        description="Es wurde `1 Bild` erfolgreich gelöscht ✅",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=purge_embed
                    )
                else:
                    purge_embed = disnake.Embed(
                        description=f"Es wurden `{amount} Bilder` erfolgreich gelöscht ✅",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=purge_embed
                    )

        else:
            loading_embed = disnake.Embed(
                description=f"Deleting {amount} images...",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=loading_embed,
                ephemeral=True
            )

            check = lambda msg: not msg.pinned and msg.attachments

            await interaction.channel.purge(

                limit=amount,
                check=check
            )
            if amount == 1:
                purge_embed = disnake.Embed(
                    description="Es wurde `1 Bild` erfolgreich gelöscht ✅",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=purge_embed
                )
            else:
                purge_embed = disnake.Embed(
                    description=f"Es wurden `{amount} Bilder` erfolgreich gelöscht ✅",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=purge_embed
                )


def setup(bot):
    bot.add_cog(Moderation(bot))
