import datetime
import json
import disnake
from disnake.ext import commands
import dateutil.parser


class onJoin(commands.Cog):
    def __init__(self, bot):
        self.bot: disnake.Client = bot

        self.DISCORD_DEFAULT_URLS = [
            "https://cdn.discordapp.com/embed/avatars/0.png",
            "https://cdn.discordapp.com/embed/avatars/1.png",
            "https://cdn.discordapp.com/embed/avatars/2.png",
            "https://cdn.discordapp.com/embed/avatars/3.png",
            "https://cdn.discordapp.com/embed/avatars/4.png",
            "https://cdn.discordapp.com/embed/avatars/5.png",
        ]

    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: disnake.Member
    ):
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        with open("json/settings.json", "r") as f:
            settings_data = json.load(f)

        # define variables
        #! defined here so i can use them everywhere in this file
        # get the user time of creation
        string = f"{member.created_at}"
        LastDate = dateutil.parser.parse(string)
        now = datetime.datetime.now()

        try:
            joinChannel: disnake.TextChannel = self.bot.get_channel(guild_data[str(member.guild.id)]["welcome_channel"])
            modChannel: disnake.TextChannel = self.bot.get_channel(guild_data[str(member.guild.id)]["mod_channel"])
            joinRole: disnake.Role = member.guild.get_role(guild_data[str(member.guild.id)]["join_role"])

            standardAvatarCheck: bool = settings_data[str(member.guild.id)]["standard_avatar_check"]
            antiAltDays: int = settings_data[str(member.guild.id)]["anti_alt_days"]
        except KeyError:
            pass

        # calculate the difference between the user time of creation and the current time
        diff = (now - LastDate.replace(tzinfo=None)).days

        if member.bot:
            # if member is a bot
            return

        if not joinChannel:
            # there is no join channel
            return
        else:
            # send the join message in the mod channel
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
            await joinChannel.send(
                embed=embed
            )
        
        if not joinRole:
            # there is no join role
            return
        else:
            # if there is a join role
            try:
                await member.add_roles(
                    joinRole,
                    reason="Join Role"
                )
            except disnake.Forbidden:
                # if the bot doesn't have the permissions
                pass
        
        if not antiAltDays:
            # there is no anti alt days
            return
        else:
            if diff < antiAltDays:
                embed = disnake.Embed(
                    title="> Antialt Detection Kick ⛔",
                    description=f":exclamation: **Your Account has to be at least {antiAltDays} days old!**\n"
                                f"⌛ **Account Age** : `{diff}` days old\n"
                                f":exclamation: **Must be** at least : `{antiAltDays}` days old",
                    color=disnake.Color.red()
                )
                await member.send(
                    embed=embed
                )

                # try to kick user if the bot has the permissions
                try:
                    await member.kick(
                        reason="Anti Alt Detection System"
                    )
                except disnake.Forbidden:
                    # if the bot doesn't have the permissions
                    pass
                
                if not modChannel:
                    # there is no mod channel
                    return
                else:
                    # if there is a mod channel
                    embed = disnake.Embed(
                        title="> Antialt Detection Kick ⛔",
                        description=f":exclamation: {member.name} got kicked by `the Anti Alt System`!\n"
                                    f"⌛ **Account Age** : `{diff}` days old\n"
                                    f":exclamation: **Must be** at least : `{antiAltDays}` days old",
                        color=disnake.Color.red()
                    )
                    
                    await modChannel.send(
                        embed=embed
                    )
            else:
                # if the difference is bigger than the anti alt days
                pass

        if not standardAvatarCheck:
            # standard avatar check is set to false
            return
        else:
            # if there is a standard avatar check
            if member.avatar.url in self.DISCORD_DEFAULT_URLS:
                embed = disnake.Embed(
                    title="> Default Avatar Detection System ⛔",
                    description=f":exclamation: **You can't use a default avatar!**\n"
                                f":exclamation: **You must use a custom avatar!**",
                    color=disnake.Color.red()
                )
                await member.send(
                    embed=embed
                )

                # try to kick user if the bot has the permissions
                try:
                    await member.kick(
                        reason="Anti Alt Detection System"
                    )
                except disnake.Forbidden:
                    # if the bot doesn't have the permissions
                    pass
                
                if not modChannel:
                    # there is no mod channel
                    return
                else:
                    # if there is a mod channel
                    embed = disnake.Embed(
                        title="> Default Avatar Detection System ⛔",
                        description=f":exclamation: {member.name} got kicked by the `Default Avatar Detection System`!\n"
                                f"**Problem** : Using a Default Discord Avatar\n" # -> possible bot
                                f":exclamation: **Must use** a custom avatar!",
                        color=disnake.Color.red()
                    )
                    
                    await modChannel.send(
                        embed=embed
                    )
            else:
                # if the user has a custom avatar
                pass


def setup(bot):
    bot.add_cog(onJoin(bot))
