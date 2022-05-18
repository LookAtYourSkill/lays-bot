import disnake
from disnake.ext import commands
import json


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.PATH = "json/guild.json"
        self.prefix = "/"

    @commands.slash_command()
    async def setup(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @setup.sub_command_group()
    async def channel(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @setup.sub_command_group()
    async def category(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @setup.sub_command_group()
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(interaction.guild.id)]["mod_channel"]:

            guild_data[str(interaction.guild.id)]["mod_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Moderation Log Channel` wurde auf {channel.mention} gesetzt!",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=set_embed,
                ephemeral=True
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Moderation Log Channel` wurde bereits auf <#{guild_data[str(interaction.guild.id)]['mod_channel']}> festgelegt! Benutze `den dazu gehörigen Change /-Command` um ihn zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=already_embed,
                ephemeral=True
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(interaction.guild.id)]["msg_channel"]:

            guild_data[str(interaction.guild.id)]["msg_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Message Log Channel` wurde auf {channel.mention} gesetzt!",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=set_embed,
                ephemeral=True
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Message Log Channel` wurde bereits auf <#{guild_data[str(interaction.guild.id)]['msg_channel']}> festgelegt! Benutze `den dazu gehörigen Change /-Command` um ihn zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=already_embed,
                ephemeral=True
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(interaction.guild.id)]["ticket_log_channel"]:

            guild_data[str(interaction.guild.id)]["ticket_log_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Ticket Log Channel` wurde auf {channel.mention} gesetzt!",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=set_embed,
                ephemeral=True
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Ticket Log Channel` wurde bereits auf <#{guild_data[str(interaction.guild.id)]['ticket_log_channel']}> festgelegt! Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=already_embed,
                ephemeral=True
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(interaction.guild.id)]["ticket_save_channel"]:

            guild_data[str(interaction.guild.id)]["ticket_save_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Ticket Save Channel` wurde auf {channel.mention} gesetzt!",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=set_embed,
                ephemeral=True
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Ticket Save Channel` wurde bereits auf <#{guild_data[str(interaction.guild.id)]['ticket_save_channel']}> festgelegt! Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=already_embed,
                ephemeral=True
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(interaction.guild.id)]["notify_channel"]:

            guild_data[str(interaction.guild.id)]["notify_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Notification Channel` wurde auf {channel.mention} gesetzt!",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=set_embed,
                ephemeral=True
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Notification Channel` wurde bereits auf <#{guild_data[str(interaction.guild.id)]['notify_channel']}> festgelegt! Benutze `den dazu gehörigen Change /-Command` um ihn zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=already_embed,
                ephemeral=True
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(interaction.guild.id)]["welcome_channel"]:

            guild_data[str(interaction.guild.id)]["welcome_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Welcome Channel` wurde auf {channel.mention} gesetzt!",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=set_embed,
                ephemeral=True
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Welcome Channel` wurde bereits auf <#{guild_data[str(interaction.guild.id)]['welcome_channel']}> festgelegt! Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=already_embed,
                ephemeral=True
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(interaction.guild.id)]["ticket_category"]:

            guild_data[str(interaction.guild.id)]["ticket_category"] = int(category.id)
            with open(f"{self.PATH}", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Die `Ticket Category` wurde auf `{category}` gesetzt!",
                color=disnake.Color.green()
            )
            await interaction.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Die `Ticket Category` wurde bereits auf `{guild_data[str(interaction.guild.id)]['ticket_category']}` festgelegt! Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.send(
                embed=already_embed
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["closed_ticket_category"]:

            guild_data[str(interaction.guild.id)]["closed_ticket_category"] = int(category.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Die `Closed Ticket Category` wurde erfolgreich auf <#{category}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=change_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Die `Closed Ticket Category` wurde bereits auf <#{guild_data[str(interaction.guild.id)]['closed_ticket_category']}> festgelegt! Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=already_embed
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
        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
                guild_data = json.load(data_file)

        if not guild_data[str(interaction.guild.id)]["join_role"]:

            guild_data[str(interaction.guild.id)]["join_role"] = int(role.id)
            with open(f"{self.PATH}", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Die `Join-Role` wurde auf {role.mention} gesetzt!",
                color=disnake.Color.green()
            )
            await interaction.response.send_message(
                embed=set_embed,
                ephemeral=True
            )
        else:
            already_embed = disnake.Embed(
                description=f"Die `Join-Role` wurde bereits auf <@&{guild_data[str(interaction.guild.id)]['join_role']}> festgelegt! Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.response.send_message(
                embed=already_embed,
                ephemeral=True
            )


class Change(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.PATH = "json/guild.json"
        self.prefix = "/"

    @commands.slash_command()
    async def change(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @change.sub_command_group()
    async def channel(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @change.sub_command_group()
    async def role(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @change.sub_command_group()
    async def category(
        self,
        interaction: disnake.CommandInteraction
    ):
        pass

    @channel.sub_command(
        name="mod",
        description="Changes the mod setup command"
    )
    @commands.has_permissions(administrator=True)
    async def change_mod_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["mod_channel"]:

            guild_data[str(interaction.guild.id)]["mod_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Moderation Log Channel` wurde erfolgreich auf <#{channel.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch kein `Moderation Log Channel` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!.",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )

    @channel.sub_command(
        name="msg",
        description="Changes the mod setup command"
    )
    @commands.has_permissions(administrator=True)
    async def change_msg_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["msg_channel"]:

            guild_data[str(interaction.guild.id)]["msg_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Message Log Channel` wurde erfolgreich auf <#{channel.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch kein `Message Log Channel` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )

    @channel.sub_command(
        name="notification",
        description="Changes the mod setup command"
    )
    @commands.has_permissions(administrator=True)
    async def change_notify_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["notify_channel"]:

            guild_data[str(interaction.guild.id)]["notify_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Notification Channel` wurde erfolgreich auf <#{channel.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch kein `Notification Channel` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )

    @role.sub_command(
        name="join",
        description="Changes join role"
    )
    @commands.has_permissions(administrator=True)
    async def change_join_role(
        self,
        interaction: disnake.ApplicationCommandInteraction, 
        role: disnake.Role
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["join_role"]:

            guild_data[str(interaction.guild.id)]["join_role"] = int(role.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Die `Join Role` wurde erfolgreich auf <@&{role.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch keine `Join Role` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )

    @channel.sub_command(
        name="welcome",
        description="Changes the welcome channel"
    )
    @commands.has_permissions(administrator=True)
    async def change_welcome_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["welcome_channel"]:

            guild_data[str(interaction.guild.id)]["welcome_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Welcome Channel` wurde erfolgreich auf <#{channel.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch kein `Welcome Channel` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )

    @category.sub_command(
        name="ticket_open",
        description="Changes the ticket category"
    )
    @commands.has_permissions(administrator=True)
    async def change_ticket_category(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        category: disnake.CategoryChannel
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["ticket_category"]:

            guild_data[str(interaction.guild.id)]["ticket_category"] = int(category.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Die `Ticket Category` wurde erfolgreich auf <#{category.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch keine `Ticket Category` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )

    @category.sub_command(
        name="ticket_log",
        description="Changes the ticket log channel"
    )
    @commands.has_permissions(administrator=True)
    async def change_ticket_log_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction, 
        channel: disnake.TextChannel
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:

            guild_data[str(interaction.guild.id)]["ticket_log_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Ticket Log Channel` wurde erfolgreich auf <#{channel.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch kein `Ticket Log Channel` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )

    @category.sub_command(
        name="ticket_save",
        description="Changes the ticket save channel"
    )
    @commands.has_permissions(administrator=True)
    async def change_ticket_save_channel(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["ticket_save_channel"]:

            guild_data[str(interaction.guild.id)]["ticket_save_channel"] = int(channel.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Ticket Save Channel` wurde erfolgreich auf <#{channel.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch kein `Ticket Save Channel` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )

    @category.sub_command(
        name="ticket_close",
        description="Changes the ticket close category"
    )
    @commands.has_permissions(administrator=True)
    async def change_ticket_close_category(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        category: disnake.CategoryChannel
    ):
        loading_embed = disnake.Embed(
            description="Setting everything up...",
            color=disnake.Color.green()
        )
        await interaction.response.send_message(
            embed=loading_embed,
            ephemeral=True
        )

        with open(f"{self.PATH}", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(interaction.guild.id)]["closed_ticket_category"]:

            guild_data[str(interaction.guild.id)]["closed_ticket_category"] = int(category.id)
            with open(f"{self.PATH}", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Die `Ticket Close Category` wurde erfolgreich auf <#{category.id}> geändert!",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description="Für `diesen Server` wurde noch keine `Ticket Close Category` festgelgt. Benutze `den dazu gehörigen Change /-Command` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=not_channel_set_embed
            )


def setup(bot):
    bot.add_cog(Setup(bot))
    bot.add_cog(Change(bot))
