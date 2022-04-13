import disnake
from disnake.ext import commands
import json


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = "%"

    @commands.slash_command(
        description="Gives help about setup commands"
    )
    async def setup(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        help_embed = disnake.Embed(
            color=interaction.author.color
        )
        help_embed.add_field(
            name="Set Channels/Roles",
            value=f"`{self.prefix}setup_mod_channel` [`channelid`]\n"
                  f"`{self.prefix}setup_msg_channel` [`channelid`]\n"
                  f"`{self.prefix}setup_ticket_category` [`categoryid`]\n"
                  f"`{self.prefix}setup_ticket_close_category` [`categoryid`]\n"
                  f"`{self.prefix}setup_ticket_log_channel` [`channelid`]\n"
                  f"`{self.prefix}setup_ticket_save_channel` [`channelid`]\n"
                  f"`{self.prefix}setup_notify_channel` [`channelid`]\n"
                  f"`{self.prefix}setup_welcome_channel` [`channelid`]\n"
                  f"`{self.prefix}setup_join_role` [`roleid`]\n",
            inline=False
        )
        help_embed.add_field(
            name="Change Channels/Roles",
            value=f"`{self.prefix}change_mod_channel` [`new channelid`]\n"
                  f"`{self.prefix}change_msg_channel` [`new channelid`]\n"
                  f"`{self.prefix}change_ticket_category` [`categoryid`]\n"
                  f"`{self.prefix}change_ticket_close_category` [`categoryid`]\n"
                  f"`{self.prefix}change_ticket_log_channel` [`channelid`]\n"
                  f"`{self.prefix}change_ticket_save_channel` [`channelid`]\n"
                  f"`{self.prefix}change_notify_channel` [`new channelid`]\n"
                  f"`{self.prefix}change_welcome_channel` [`new channelid`]\n"
                  f"`{self.prefix}change_join_role` [`new roleid`]\n"
        )
        help_embed.set_footer(
            text="Für alle Befehle, benötigst du Administrator Berechtigungen"
        )
        await interaction.response.send_message(
            embed=help_embed,
            ephemeral=True
        )

    @commands.command(description="Set a moderation log channel")
    @commands.has_permissions(administrator=True)
    async def setup_mod_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(inter.guild.id)]["mod_channel"]:

            guild_data[str(inter.guild.id)]["mod_channel"] = int(channel_id)
            with open("json/guild.json", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Moderation Log Channel` wurde auf <#{channel_id}> gesetzt!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Moderation Log Channel` wurde bereits auf <#{guild_data[str(inter.guild.id)]['mod_channel']}> festgelegt! Benutze `{self.prefix}change_mod_channel` um ihn zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )

    @commands.command(description="Set a message log channel")
    @commands.has_permissions(administrator=True)
    async def setup_msg_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(inter.guild.id)]["msg_channel"]:

            guild_data[str(inter.guild.id)]["msg_channel"] = int(channel_id)
            with open("json/guild.json", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Message Log Channel` wurde auf <#{channel_id}> gesetzt!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Message Log Channel` wurde bereits auf <#{guild_data[str(inter.guild.id)]['msg_channel']}> festgelegt! Benutze `{self.prefix}change_msg_channel` um ihn zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )

    @commands.command(description="Set a notification channel for twitch")
    @commands.has_permissions(administrator=True)
    async def setup_notify_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(inter.guild.id)]["notify_channel"]:

            guild_data[str(inter.guild.id)]["notify_channel"] = int(channel_id)
            with open("json/guild.json", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Notification Channel` wurde auf <#{channel_id}> gesetzt!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Notification Channel` wurde bereits auf <#{guild_data[str(inter.guild.id)]['notify_channel']}> festgelegt! Benutze `{self.prefix}change_nofity_channel` um ihn zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )

    @commands.command(description="Changes the mod setup command")
    @commands.has_permissions(administrator=True)
    async def change_mod_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["mod_channel"]:

            guild_data[str(inter.guild.id)]["mod_channel"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Moderation Log Channel` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch kein `Moderation Log Channel` festgelgt. Das kannst du mit `{self.prefix}setup_mod_channel` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )

    @commands.command(description="Changes the mod setup command")
    @commands.has_permissions(administrator=True)
    async def change_msg_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["msg_channel"]:

            guild_data[str(inter.guild.id)]["msg_channel"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Message Log Channel` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch kein `Message Log Channel` festgelgt. Das kannst du mit `{self.prefix}setup_msg_channel` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )

    @commands.command(description="Changes the mod setup command")
    @commands.has_permissions(administrator=True)
    async def change_notify_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["notify_channel"]:

            guild_data[str(inter.guild.id)]["notify_channel"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Notification Channel` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch kein `Notification Channel` festgelgt. Das kannst du mit `{self.prefix}setup_notify_channel` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )

    @commands.command(description="Set join role channel")
    @commands.has_permissions(administrator=True)
    async def setup_join_role(self, inter, role_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(inter.guild.id)]["join_role"]:

            guild_data[str(inter.guild.id)]["join_role"] = int(role_id)
            with open("json/guild.json", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Die `Join-Role` wurde auf <@&{role_id}> gesetzt!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Die `Join-Role` wurde bereits auf <@&{guild_data[str(inter.guild.id)]['join_role']}> festgelegt! Benutze `{self.prefix}change_join_role` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )

    @commands.command(description="Changes join role")
    @commands.has_permissions(administrator=True)
    async def change_join_role(self, inter, role_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["join_role"]:

            guild_data[str(inter.guild.id)]["join_role"] = int(role_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Die `Join Role` wurde erfolgreich auf <@&{role_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch keine `Join Role` festgelgt. Das kannst du mit `{self.prefix}setup_join_role` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )

    @commands.command(description="Set a welcome channel")
    @commands.has_permissions(administrator=True)
    async def setup_welcome_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(inter.guild.id)]["welcome_channel"]:

            guild_data[str(inter.guild.id)]["welcome_channel"] = int(channel_id)
            with open("json/guild.json", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Welcome Channel` wurde auf <#{channel_id}> gesetzt!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Welcome Channel` wurde bereits auf <#{guild_data[str(inter.guild.id)]['welcome_channel']}> festgelegt! Benutze `{self.prefix}change_welcome_channel` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )

    @commands.command(description="Changes the welcome channel")
    @commands.has_permissions(administrator=True)
    async def change_welcome_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["welcome_channel"]:

            guild_data[str(inter.guild.id)]["welcome_channel"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Welcome Channel` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch kein `Welcome Channel` festgelgt. Das kannst du mit `{self.prefix}setup_welcome_channel` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )

    @commands.command(description="Set a ticket category")
    @commands.has_permissions(administrator=True)
    async def setup_ticket_category(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(inter.guild.id)]["ticket_category"]:

            guild_data[str(inter.guild.id)]["ticket_category"] = int(channel_id)
            with open("json/guild.json", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Die `Ticket Category` wurde auf `{channel_id}` gesetzt!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Die `Ticket Category` wurde bereits auf `{guild_data[str(inter.guild.id)]['ticket_category']}` festgelegt! Benutze `{self.prefix}change_ticket_category` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )

    @commands.command(description="Set a ticket log channel")
    @commands.has_permissions(administrator=True)
    async def setup_ticket_log_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(inter.guild.id)]["ticket_log_channel"]:

            guild_data[str(inter.guild.id)]["ticket_log_channel"] = int(channel_id)
            with open("json/guild.json", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Ticket Log Channel` wurde auf <#{channel_id}> gesetzt!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Ticket Log Channel` wurde bereits auf <#{guild_data[str(inter.guild.id)]['ticket_log_channel']}> festgelegt! Benutze `{self.prefix}change_ticket_log_channel` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )

    @commands.command(description="Set a ticket save channel")
    @commands.has_permissions(administrator=True)
    async def setup_ticket_save_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if not guild_data[str(inter.guild.id)]["ticket_save_channel"]:

            guild_data[str(inter.guild.id)]["ticket_save_channel"] = int(channel_id)
            with open("json/guild.json", "w") as f:
                json.dump(guild_data, f, indent=4)

            set_embed = disnake.Embed(
                description=f"Der `Ticket Save Channel` wurde auf <#{channel_id}> gesetzt!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=set_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Der `Ticket Save Channel` wurde bereits auf <#{guild_data[str(inter.guild.id)]['ticket_save_channel']}> festgelegt! Benutze `{self.prefix}change_ticket_save_channel` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )

    @commands.command(description="Changes the ticket category")
    @commands.has_permissions(administrator=True)
    async def change_ticket_category(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["ticket_category"]:

            guild_data[str(inter.guild.id)]["ticket_category"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Die `Ticket Category` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch keine `Ticket Category` festgelgt. Das kannst du mit `{self.prefix}setup_ticket_category` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )

    @commands.command(description="Changes the ticket log channel")
    @commands.has_permissions(administrator=True)
    async def change_ticket_log_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["ticket_log_channel"]:

            guild_data[str(inter.guild.id)]["ticket_log_channel"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Ticket Log Channel` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch kein `Ticket Log Channel` festgelgt. Das kannst du mit `{self.prefix}setup_ticket_log_channel` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )

    @commands.command(description="Changes the ticket save channel")
    @commands.has_permissions(administrator=True)
    async def change_ticket_save_channel(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["ticket_save_channel"]:

            guild_data[str(inter.guild.id)]["ticket_save_channel"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Der `Ticket Save Channel` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch kein `Ticket Save Channel` festgelgt. Das kannst du mit `{self.prefix}setup_ticket_save_channel` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )

    @commands.command(description="Changes the ticket close category")
    @commands.has_permissions(administrator=True)
    async def setup_ticket_close_category(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["closed_ticket_category"]:

            guild_data[str(inter.guild.id)]["closed_ticket_category"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Die `Closed Ticket Category` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            already_embed = disnake.Embed(
                description=f"Die `Closed Ticket Category` wurde bereits auf <#{guild_data[str(inter.guild.id)]['closed_ticket_category']}> festgelegt! Benutze `{self.prefix}change_ticket_close_category` um diese zu verändern!",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=already_embed
            )


    @commands.command(description="Changes the ticket close category")
    @commands.has_permissions(administrator=True)
    async def change_ticket_close_category(self, inter, channel_id):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if guild_data[str(inter.guild.id)]["closed_ticket_category"]:

            guild_data[str(inter.guild.id)]["closed_ticket_category"] = int(channel_id)
            with open("json/guild.json", "w", encoding="UTF-8") as dump_file:
                json.dump(guild_data, dump_file, indent=4)

            change_embed = disnake.Embed(
                description=f"Die `Ticket Close Category` wurde erfolgreich auf <#{channel_id}> geändert!",
                color=disnake.Color.green()
            )
            await inter.send(
                embed=change_embed
            )
        else:
            not_channel_set_embed = disnake.Embed(
                description=f"Für `diesen Server` wurde noch keine `Ticket Close Category` festgelgt. Das kannst du mit `{self.prefix}setup_ticket_close_category` machen.",
                color=disnake.Color.red()
            )
            await inter.send(
                embed=not_channel_set_embed
            )


def setup(bot):
    bot.add_cog(Setup(bot))
