import dateutil.parser
import json
import time
import datetime

import disnake
import humanize
from disnake.ext import commands

from checks.check_license import check_license_lol


class Info(commands.Cog):
    '''
    Shows the information for users or a server
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

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

        if not check_license_lol(interaction.author):
            no_licesnse_embed = disnake.Embed(
                title="No license ⛔",
                description="You have not set a license for this server. Please use `/license activate <license>` to set a license.",
                color=disnake.Color.red()
            )
            no_licesnse_embed.set_footer(
                text="If you dont have a license, please contact the bot owner"
            )
            await interaction.response.send_message(
                embed=no_licesnse_embed,
                ephemeral=True
            )

        else:
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
        with open("json/general.json", "r") as general_info:
            general = json.load(general_info)
        with open("json/guild.json", "r") as guild_info:
            guilds = json.load(guild_info)
        with open("json/licenses.json", "r") as license_info:
            licenses = json.load(license_info)

        if not check_license_lol(interaction.author):
            no_licesnse_embed = disnake.Embed(
                title="No license ⛔",
                description="You have not set a license for this server. Please use `/license activate <license>` to set a license.",
                color=disnake.Color.red()
            )
            no_licesnse_embed.set_footer(
                text="If you dont have a license, please contact the bot owner"
            )
            await interaction.response.send_message(
                embed=no_licesnse_embed,
                ephemeral=True
            )
        else:
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
            description=f"Bot: ``{round(self.bot.latency * 1000)}ms``\nUptime: ``{humanize.precisedelta(round(time.time()-startTime))}``",
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
