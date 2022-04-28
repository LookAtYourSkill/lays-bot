import disnake
from disnake.ext import commands


class open_component(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(
        label="Channel Opened",
        style=disnake.ButtonStyle.grey
    )
    async def open_channel(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):
        await interaction.response.send_message(
            content="Channel was opened",
            ephemeral=True
        )


class close_component(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(
        label="Channel Closed",
        style=disnake.ButtonStyle.grey
    )
    async def close_channel(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):
        await interaction.response.send_message(
            content="Channel was closed",
            ephemeral=True
        )


class hide_component(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(
        label="Channel Hidden",
        style=disnake.ButtonStyle.grey
    )
    async def hide_channel(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):
        await interaction.response.send_message(
            content="Channel was hidden",
            ephemeral=True
        )


class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="close_channel")
    async def close_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        if interaction.author.guild_permissions.manage_channels:
            await interaction.channel.set_permissions(
                interaction.guild.default_role,
                read_messages=True,
                send_messages=False
            )
            close_embed = disnake.Embed(
                description=f"The channel <#{interaction.channel.id}> was closed by {interaction.author.mention}!",
                color=disnake.Color.red()
            )
            view = close_component()
            await interaction.response.send_message(
                embed=close_embed,
                view=view
            )
        else:
            await interaction.response.send_message(
                content="You don't have the permissions to do that!",
                ephemeral=True
            )

    @commands.slash_command(name="hide_channel")
    async def hide_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        if interaction.author.guild_permissions.manage_channels:
            await interaction.channel.set_permissions(
                interaction.guild.default_role,
                read_messages=False,
                send_messages=False
            )
            close_embed = disnake.Embed(
                description=f"The channel <#{interaction.channel.id}> was hidden from {interaction.author.mention}!",
                color=disnake.Color.red()
            )
            view = hide_component()
            await interaction.response.send_message(
                embed=close_embed,
                view=view
            )
        else:
            await interaction.response.send_message(
                content="You don't have the permissions to do that!",
                ephemeral=True
            )

    @commands.slash_command(name="open_channel")
    async def open_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        if interaction.author.guild_permissions.manage_channels:
            await interaction.channel.set_permissions(
                interaction.guild.default_role,
                read_messages=True,
                send_messages=True
            )
            open_embed = disnake.Embed(
                description=f"The channel <#{interaction.channel.id}> was opened by {interaction.author.mention}!",
                color=disnake.Color.red()
            )
            view = open_component()
            await interaction.response.send_message(
                embed=open_embed,
                view=view
            )
        else:
            await interaction.response.send_message(
                content="You don't have the permissions to do that!",
                ephemeral=True
            )


def setup(bot):
    bot.add_cog(Channel(bot))
