import disnake
from disnake.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="info", description="Give information about a user")
    @commands.guild_only()
    async def user_info(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        members = sorted(inter.guild.members, key=lambda m: m.joined_at)

        if not user:
            inter.author = user

        info_embed = disnake.Embed(
            description=f"```Inforamtion über {user.name}```",
            color=user.color
        )
        info_embed.set_thumbnail(
            url=user.avatar.url
        )
        info_embed.set_author(
            name=inter.user.name,
            icon_url=inter.user.avatar.url
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
        await inter.response.send_message(
            embed=info_embed,
            ephemeral=True
        )

    @commands.slash_command(name="server", description="Give information about the server")
    @commands.guild_only()
    async def server_info(self, inter: disnake.ApplicationCommandInteraction):
        server_embed = disnake.Embed(
            description=f"```Informationen über {inter.guild.name}```",
            color=disnake.Color.orange()
        )
        server_embed.set_thumbnail(
            url=inter.guild.icon
        )
        server_embed.add_field(
            name="__Information__",
            value=f"`»`Name: `{inter.guild.name}` [`{inter.guild.id}`]\n"
                  f"`»`Owner: `{inter.guild.owner}`\n"
                  f"`»`Region: `{inter.guild.region}`",
            inline=False
        )
        server_embed.add_field(
            name="__Daten__",
            value=f"`»`Erstellt: `{inter.guild.created_at.strftime('\%d.%m.%Y')}`\n"
                  f"`»` Rollen: `{len(inter.guild.roles)}`\n"
                  f"`»`Boost Status: `{inter.guild.premium_subscription_count}/30`",
            inline=True
        )
        server_embed.add_field(
            name=f"__Channel__",
            value=f"`»` Channel insgesamt: `{len(inter.guild.channels) - len(inter.guild.categories)}`\n"
                  f"`»` Text Channels: `{len(inter.guild.text_channels)}`\n"
                  f"`»` Voice Channels: `{len(inter.guild.voice_channels)}`\n"
                  f"`»` Kategorien: `{len(inter.guild.categories)}`",
            inline=False
        )
        await inter.response.send_message(
            embed=server_embed,
            ephemeral=False
        )


def setup(bot):
    bot.add_cog(Info(bot))
