import disnake
from disnake.ext import commands
import json


class Setup(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot
        self.PATH = "json/guild.json"
        self.prefix = "/"

    @commands.slash_command()
    async def set(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @set.sub_command(
        name="check",
        description="Gives back, what channels are set and which are not"
    )
    @commands.has_permissions(administrator=True)
    async def setup_check(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        loading_embed = disnake.Embed(
            description="Fetching data from server...",
            color=disnake.Color.orange()
        )
        await interaction.edit_original_message(
            embed=loading_embed
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        check_embed = disnake.Embed(
            title="Setup Check",
            description="Here are all the things that are set up so far ✅",
            color=disnake.Color.green()
        )
        check_embed.add_field(
            name="> Text Channels",
            value=f"`Ticket Log`: <#{guild_data[str(interaction.author.guild.id)]['ticket_log_channel'] if guild_data[str(interaction.author.guild.id)]['ticket_log_channel'] else '0'}>\n"
                  f"`Ticket Save`: <#{guild_data[str(interaction.author.guild.id)]['ticket_save_channel'] if guild_data[str(interaction.author.guild.id)]['ticket_save_channel'] else '0'}>\n"
                  f"`Notification`: <#{guild_data[str(interaction.author.guild.id)]['notify_channel'] if guild_data[str(interaction.author.guild.id)]['notify_channel'] else '0'}>\n"
                  f"`Moderation`: <#{guild_data[str(interaction.author.guild.id)]['mod_channel'] if guild_data[str(interaction.author.guild.id)]['mod_channel'] else '0'}>\n"
                  f"`Message`: <#{guild_data[str(interaction.author.guild.id)]['msg_channel'] if guild_data[str(interaction.author.guild.id)]['msg_channel'] else '0'}>\n"
                  f"`Welcome`: <#{guild_data[str(interaction.author.guild.id)]['welcome_channel'] if guild_data[str(interaction.author.guild.id)]['welcome_channel'] else '0'}>",
            inline=False
        )
        check_embed.add_field(
            name="> Voice Channels",
            value=f"`Join To Create`: <#{guild_data[str(interaction.author.guild.id)]['join_to_create_channel'] if guild_data[str(interaction.author.guild.id)]['join_to_create_channel'] else '0'}>",
            inline=False
        )
        check_embed.add_field(
            name="> Categories",
            value=f"`Open Ticket`: <#{guild_data[str(interaction.author.guild.id)]['ticket_category'] if guild_data[str(interaction.author.guild.id)]['ticket_category'] else '0'}>\n"
                  f"`Closed Ticket`: <#{guild_data[str(interaction.author.guild.id)]['closed_ticket_category'] if guild_data[str(interaction.author.guild.id)]['closed_ticket_category'] else '0'}>",
            inline=False
        )
        check_embed.add_field(
            name="> Roles",
            value=f"`Join`: <@&{guild_data[str(interaction.author.guild.id)]['join_role'] if guild_data[str(interaction.author.guild.id)]['join_role'] else '0'}>",
            inline=False
        )

        await interaction.edit_original_message(
            embed=check_embed
        )

    @set.sub_command_group()
    async def channel(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @set.sub_command_group()
    async def category(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @set.sub_command_group()
    async def role(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @channel.sub_command(
        name="mod",
        description="Sets the mod log channel"
    )
    @commands.has_permissions(administrator=True)
    async def set_mod_channel(
        self,
        interaction: disnake.CommandInteraction,
        channel: disnake.TextChannel
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["mod_channel"] = int(channel.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Der `Moderation Log Channel` wurde auf {channel.mention} gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @channel.sub_command(
        name="msg",
        description="Sets the log channel"
    )
    @commands.has_permissions(administrator=True)
    async def set_log_channel(
        self,
        interaction: disnake.CommandInteraction,
        channel: disnake.TextChannel,
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)


        guild_data[str(interaction.guild.id)]["msg_channel"] = int(channel.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Der `Message Log Channel` wurde auf {channel.mention} gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @channel.sub_command(
        name="ticket_log",
        description="Sets the ticket log channel"
    )
    @commands.has_permissions(administrator=True)
    async def set_ticket_log_channel(
        self,
        interaction: disnake.CommandInteraction,
        channel: disnake.TextChannel,
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["ticket_log_channel"] = int(channel.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Der `Ticket Log Channel` wurde auf {channel.mention} gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @channel.sub_command(
        name="ticket_save",
        description="Sets the ticket save channel"
    )
    @commands.has_permissions(administrator=True)
    async def set_ticket_save_channel(
        self,
        interaction: disnake.CommandInteraction,
        channel: disnake.TextChannel
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["ticket_save_channel"] = int(channel.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Der `Ticket Save Channel` wurde auf {channel.mention} gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @channel.sub_command(
        name="join_to_create",
        description="Sets the join to cteate channel"
    )
    @commands.has_permissions(administrator=True)
    async def set_join_to_create_channel(
        self,
        interaction: disnake.CommandInteraction,
        channel: disnake.VoiceChannel
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["join_to_create_channel"] = int(channel.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Der `Join To Create Channel` wurde auf {channel.mention} gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @channel.sub_command(
        name="notification",
        description="Sets the notification channel"
    )
    @commands.has_permissions(administrator=True)
    async def set_notify_channel(
        self,
        interaction: disnake.CommandInteraction,
        channel: disnake.TextChannel
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["notify_channel"] = int(channel.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Der `Notification Channel` wurde auf {channel.mention} gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @channel.sub_command(
        name="welcome",
        description="Sets the welcome channel"
    )
    @commands.has_permissions(administrator=True)
    async def setup_welcome_channel(
        self,
        interaction: disnake.CommandInteraction,
        channel: disnake.TextChannel
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["welcome_channel"] = int(channel.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Der `Welcome Channel` wurde auf {channel.mention} gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @category.sub_command(
        name="ticket_open",
        description="Sets the open ticket category"
    )
    @commands.has_permissions(administrator=True)
    async def set_open_ticket_category(
        self,
        interaction: disnake.CommandInteraction,
        category: disnake.CategoryChannel
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["ticket_category"] = int(category.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Die `Ticket Category` wurde auf `{category}` gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @category.sub_command(
        name="ticket_close",
        description="Sets the closed ticket category"
    )
    @commands.has_permissions(administrator=True)
    async def set_closed_ticket_category(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        category: disnake.CategoryChannel
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["closed_ticket_category"] = int(category.id)
        with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
            json.dump(guild_data, dump_file, indent=4)

        change_embed = disnake.Embed(
            description=f"Die `Closed Ticket Category` wurde erfolgreich auf `{category}` geändert!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=change_embed
        )

    @category.sub_command(
        name="join_to_create",
        description="Sets the open ticket category"
    )
    @commands.has_permissions(administrator=True)
    async def join_to_create_category(
        self,
        interaction: disnake.CommandInteraction,
        category: disnake.CategoryChannel
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["join_to_create_category"] = int(category.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Die `Join To Create Category` wurde auf `{category}` gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )

    @role.sub_command(
        name="join",
        description="Sets the join role"
    )
    @commands.has_permissions(administrator=True)
    async def set_join_role(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        role: disnake.Role
    ):
        await interaction.response.defer(ephemeral=True)

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        guild_data[str(interaction.guild.id)]["join_role"] = int(role.id)
        with open(f"{self.PATH}", "w") as f:
            json.dump(guild_data, f, indent=4)

        set_embed = disnake.Embed(
            description=f"Die `Join-Role` wurde auf {role.mention} gesetzt!",
            color=disnake.Color.green()
        )
        await interaction.edit_original_message(
            embed=set_embed
        )


def setup(bot):
    bot.add_cog(Setup(bot))
