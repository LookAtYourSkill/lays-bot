import datetime
import json
import disnake
from disnake.ext import commands
import dateutil.parser


class onJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(
        self,
        member
    ):
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        if member.bot:
            return

        elif not guild_data[str(member.guild.id)]["welcome_channel"]:
            string = f"{member.created_at}"
            LastDate = dateutil.parser.parse(string)
            now = datetime.datetime.now()

            diff = (now - LastDate.replace(tzinfo=None)).days

            if diff < 7:
                embed = disnake.Embed(
                    title="Antialt Detection Kick ⛔",
                    description=f":exclamation: **Your Account has to be at least 7 days old!**\n"
                                f"⌛ **Account Age** : `{diff}` days old\n"
                                ":exclamation: **Must be** at least : `7` days old",
                    color=disnake.Color.red()
                )
                await member.send(
                    embed=embed
                )
                await member.kick(
                    reason="Anti Alt Detection"
                )

                if guild_data[str(member.guild.id)]["mod_channel"]:
                    embed = disnake.Embed(
                        title="Anti Alt Detection Kick ⛔",
                        description=f"`{member}` was kicked by the **Anti Alt Detection** :white_check_mark:",
                        color=disnake.Color.green()
                    )
                    embed.add_field(
                        name="__Ages__",
                        value=f"⌛ Days old: `{diff}` days\n ⌛ Needed at least : `7` days",
                        inline=False
                    )
                    embed.add_field(
                        name="__Reason__",
                        value="`Anti Alt Detection`",
                        inline=False
                    )
                    embed.set_footer(
                        text=f"ID: {member.id}"
                    )
                    channel = self.bot.get_channel(guild_data[str(member.guild.id)]["mod_channel"])
                    await channel.send(embed=embed)
                else:
                    return
            else:
                return

        else:
            string = f"{member.created_at}"
            LastDate = dateutil.parser.parse(string)
            now = datetime.datetime.now()

            diff = (now - LastDate.replace(tzinfo=None)).days

            if diff < 7:
                embed = disnake.Embed(
                    title="Antialt Detection Kick ⛔",
                    description=f":exclamation: **Your Account has to be at least 7 days old!**\n"
                                f"⌛ **Account Age** : `{diff}` days old\n"
                                ":exclamation: **Must be [at least]** : `7` days old",
                    color=disnake.Color.red()
                )
                await member.send(
                    embed=embed
                )
                await member.kick(
                    reason="Anti Alt Detection"
                )

                if guild_data[str(member.guild.id)]["mod_channel"]:
                    embed = disnake.Embed(
                        title="Anti Alt Detection Kick ⛔",
                        description=f"`{member}` was kicked by the **Anti Alt Detection** :white_check_mark:",
                        color=disnake.Color.green()
                    )
                    embed.add_field(
                        name="__Ages__",
                        value=f"⌛ Days old: `{diff}` days\n ⌛ Needed at least : `7` days",
                        inline=False
                    )
                    embed.add_field(
                        name="__Reason__",
                        value="`Anti Alt Detection`",
                        inline=False
                    )
                    embed.set_footer(
                        text=f"ID: {member.id}"
                    )
                    channel = self.bot.get_channel(
                        guild_data[str(member.guild.id)]["mod_channel"]
                    )
                    await channel.send(
                        embed=embed
                    )
                else:
                    return
            else:
                channel = self.bot.get_channel(guild_data[str(member.guild.id)]["welcome_channel"])
                role = disnake.utils.get(member.guild.roles, id=guild_data[str(member.guild.id)]["join_role"])

                embed = disnake.Embed(
                    title="> Welcome :tada:",
                    description=f"{member.mention} Joined **{member.guild.name}**",
                    color=disnake.Color.random(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_thumbnail(
                    url=member.avatar.url
                )
                embed.add_field(
                    name="Total members",
                    value=f"{member.guild.member_count}",
                    inline=False
                )
                embed.set_footer(
                    text=f"{member.name} joined"
                )
                await channel.send(
                    embed=embed
                )
                await member.add_roles(role, reason="Join Role")

    @commands.Cog.listener()
    async def on_member_ban(
        self,
        guild,
        user
    ):
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        if guild_data[str(guild.id)]["mod_channel"]:
            embed = disnake.Embed(
                title="⚔️ User Ban",
                description=f"`{user}` wurde von `{guild.me}` gebannt!",
                color=disnake.Color.red()
            )
            channel = self.bot.get_channel(
                guild_data[str(guild.id)]["mod_channel"]
            )
            await channel.send(
                embed=embed
            )
        else:
            return

    @commands.Cog.listener()
    async def on_member_unban(
        self,
        guild,
        user
    ):
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        if guild_data[str(guild.id)]["mod_channel"]:
            embed = disnake.Embed(
                title="⚔️ User Unban",
                description=f"`{user}` wurde von `{guild.me}` entbannt!",
                color=disnake.Color.green()
            )
            channel = self.bot.get_channel(
                guild_data[str(guild.id)]["mod_channel"]
            )
            await channel.send(
                embed=embed
            )
        else:
            return


def setup(bot):
    bot.add_cog(onJoin(bot))
