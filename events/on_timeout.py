import disnake
from disnake.ext import commands
import json
import humanize
from datetime import datetime, timezone


class onTimeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        with open("json/guild.json", "r") as guild:
            guild = json.load(guild)

        log_channel = self.bot.get_channel(guild[str(before.guild.id)]["mod_channel"])

        if before.timeout:
            # print(before.current_timeout)
            # print("#######################")
            # print(after.current_timeout)

            if not after.current_timeout:
                async for author in before.guild.audit_logs(
                    limit=1,
                    action=disnake.AuditLogAction.member_update
                ):
                    punisher = author.user

                untime_embed = disnake.Embed(
                    title="Timeout Log",
                    description=f"> **User:** {before.mention}'s timeout ended!\n"
                                f"> **ID**: `{before.id}`\n"
                                f"> **Untimed from:** {punisher.mention}",
                    timestamp=datetime.now(timezone.utc),
                    color=disnake.Color.green()
                )
                untime_embed.set_thumbnail(
                    url=before.avatar.url
                )
                untime_embed.set_footer(
                    text=punisher,
                    icon_url=punisher.avatar.url
                )
                await log_channel.send(
                    embed=untime_embed
                )
            else:
                async for author in before.guild.audit_logs(
                    limit=1,
                    action=disnake.AuditLogAction.member_update
                ):
                    punisher = author.user

                time_embed = disnake.Embed(
                    title="Timeout Log",
                    description=f"> **User:** {before.mention} was timed out!\n"
                                f"> **ID:** `{before.id}`\n"
                                f"> **Timeout Duration:** {str(humanize.precisedelta(after.current_timeout - datetime.now(timezone.utc)))}\n"
                                f"> **Expires in:** <t:{round(after.current_timeout.timestamp())}>\n"
                                f"> **Punisher:** {punisher.mention}",
                    timestamp=datetime.now(timezone.utc),
                    color=disnake.Color.red()
                )
                time_embed.set_thumbnail(
                    url=before.avatar.url
                )
                time_embed.set_footer(
                    text=punisher,
                    icon_url=punisher.avatar.url
                )
                await log_channel.send(
                    embed=time_embed
                )


def setup(bot):
    bot.add_cog(onTimeout(bot))