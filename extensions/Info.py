import dateutil.parser
import json
import datetime

import disnake
from disnake.ext import commands

from checks._check_license import check_license


class Info(commands.Cog):
    '''
    Shows the information for users or a server
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = round(datetime.datetime.timestamp(datetime.datetime.now()))

    @check_license()
    @commands.slash_command(
        name="info",
        description="Command Group for info"
    )
    async def info(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @info.sub_command(
        name="user",
        description="Give information about a user"
    )
    @commands.guild_only()
    async def user_info(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user: disnake.User
    ):

        string = f"{user.created_at}"
        LastDate = dateutil.parser.parse(string)
        now = datetime.datetime.now()

        diff = (now - LastDate.replace(tzinfo=None)).days

        loading_embed = disnake.Embed(
            description="Fetching information about the user...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        members = sorted(interaction.guild.members, key=lambda m: m.joined_at)

        if not user:
            interaction.author = user

        info_embed = disnake.Embed(
            description=f"```Inforamtion über {user.name}```",
            color=user.color
        )
        info_embed.set_thumbnail(
            url=user.avatar.url
        )
        info_embed.set_author(
            name=interaction.user.name,
            icon_url=interaction.user.avatar.url
        )
        info_embed.add_field(
            name="__Name__",
            value=f"`»`Name: `{user}`\n"
                  f"`»`ID: `{user.id}`\n"
                  f"`»`Nick: `{(user.nick if user.nick else 'Nein')}`",
            inline=False
        )
        info_embed.add_field(
            name="__Account__",
            value=f"`»`Discord Beigetreten: `{user.created_at.strftime('%d.%m.%Y')}`\n"
                  f"`»`Tage: `{diff}`\n"
                  f"`»`Bot: `{('Ja' if user.bot else 'Nein')}`\n"
                  f"`»`Farbe: `{user.color}`\n"
                  f"`»`Status: `{user.status}`\n"
                  f"`»`Join Position: `{str(members.index(user) + 1)}`",
            inline=False
        )
        info_embed.add_field(
            name="__Server__",
            value=f"`»`Server Beigetreten: `{user.joined_at.strftime('%d.%m.%Y')}`\n"
                  f"`»`Rollen: `{len(user.roles)}`\n"
                  f"`»`Booster: `{('Ja' if user.premium_since else 'Nein')}`",
            inline=False
        )
        await interaction.edit_original_message(
            embed=info_embed
        )

    @info.sub_command(
        name="server",
        description="Give information about the server"
    )
    @commands.guild_only()
    async def server_info(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)
        with open("json/settings.json", "r") as f:
            settings_data = json.load(f)

        loading_embed = disnake.Embed(
            description="Fetching information about the server...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        server_embed = disnake.Embed(
            description=f"```Informationen über {interaction.guild.name}```",
            color=disnake.Color.orange()
        )
        server_embed.set_thumbnail(
            url=interaction.guild.icon
        )
        server_embed.add_field(
            name="__Information__",
            value=f"`»`Name: `{interaction.guild.name}` [`{interaction.guild.id}`]\n"
                    f"`»`Owner: `{interaction.guild.owner}`\n"
                    f"`»`Region: `{interaction.guild.region}`",
            inline=False
        )
        server_embed.add_field(
            name="__Personal Server Info__",
            value=f"`»` Twitch Everyone: `{'Yes' if guild_data[str(interaction.author.guild.id)]['twitch_with_everyone'] == 'on' else 'No'}`\n"
                    f"`»` AntiAlt-Days: `{settings_data[str(interaction.author.guild.id)]['anti_alt_days']}`",
            inline=False
        )
        server_embed.add_field(
            name="__Daten__",
            value=f"`»`Erstellt: `{interaction.guild.created_at.strftime('%d.%m.%Y')}`\n"
                    f"`»` Rollen: `{len(interaction.guild.roles)}`\n"
                    f"`»`Boost Status: `{interaction.guild.premium_subscription_count} von 30`",
            inline=True
        )
        server_embed.add_field(
            name="__Channel__",
            value=f"`»` Channel insgesamt: `{len(interaction.guild.channels) - len(interaction.guild.categories)}`\n"
                    f"`»` Text Channels: `{len(interaction.guild.text_channels)}`\n"
                    f"`»` Voice Channels: `{len(interaction.guild.voice_channels)}`\n"
                    f"`»` Kategorien: `{len(interaction.guild.categories)}`",
            inline=False
        )
        await interaction.edit_original_message(
            embed=server_embed
        )

    @info.sub_command(name="ping", description="Pings the bot")
    async def ping(self, interaction: disnake.ApplicationCommandInteraction):
        search_embed = disnake.Embed(
            description="Pinging...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=search_embed,
            ephemeral=True
        )
        ping_embed = disnake.Embed(
            description=f"Bot: ``{round(self.bot.latency * 1000)}ms``\nUptime: {disnake.utils.format_dt(startTime, style='R')}",
            color=disnake.Color.green()
        )
        ping_embed.set_author(
            name=interaction.user.name,
            icon_url=interaction.user.avatar.url
        )
        await interaction.edit_original_message(
            embed=ping_embed
        )


def setup(bot):
    bot.add_cog(Info(bot))
