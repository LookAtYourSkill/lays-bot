import asyncio
import disnake
from disnake.ext import commands
import json
import pytz
import os

from checks._force_guild_check import right_guild


class open_message(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(
        label="Open",
        style=disnake.ButtonStyle.green,
        emoji="🔓",
        custom_id="persistent_view:open"
    )
    async def open_ticket(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.response.defer()

        # Load all jsons
        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]["status"] = "open"

        with open("json/tickets.json", "w") as f:
            json.dump(ticket_data, f, indent=4)

        if guild_data[str(interaction.guild.id)]["ticket_category"]:
            # setup variables and perms
            ticket_category = disnake.utils.get(
                interaction.guild.categories,
                id=int(guild_data[str(interaction.guild.id)]["ticket_category"])
            )

            target = disnake.utils.get(
                interaction.guild.members,
                id=ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]["author"]
            )

            await interaction.channel.set_permissions(
                target, send_messages=True, read_messages=True
            )
            await interaction.channel.edit(
                category=ticket_category
            )

            # create and send embed
            open_embed = disnake.Embed(
                description=f"Ticket Opened by {interaction.author.mention}",
                color=disnake.Color.green()
            )
            view = close_message()
            await interaction.followup.send(
                embed=open_embed,
                view=view
            )

            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:
                # create log
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket <#{interaction.channel.id}> reopened | Action: `{button.label}`",
                    color=disnake.Color.green()
                )
                log_embed.set_author(
                    name=interaction.author.name,
                    icon_url=interaction.author.avatar.url
                )
                await ticket_log_channel.send(
                    embed=log_embed
                )
            else:
                await interaction.followup.send(
                    content="_No ticket log channel set_. Skipped it!",
                    ephemeral=True
                )
        else:
            await interaction.followup.send(
                content="_No ticket category set_. Skipped it!",
                ephemeral=True
            )

    @disnake.ui.button(
        label="Delete",
        style=disnake.ButtonStyle.red,
        emoji="🗑",
        custom_id="persistent_view:delete"
    )
    async def delete_ticket(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.response.defer()

        if interaction.author.guild_permissions.manage_channels:

            # Load all jsons
            with open("json/tickets.json", "r") as f:
                ticket_data = json.load(f)
            with open("json/guild.json", "r") as f:
                guild_data = json.load(f)

            del ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]

            with open("json/tickets.json", "w") as f:
                json.dump(ticket_data, f, indent=4)

            # create and send embed
            delete_embed = disnake.Embed(
                description="Ticket will be deleted in a few seconds",
                color=disnake.Color.red()
            )
            await interaction.followup.send(
                embed=delete_embed
            )

            # create log
            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket `{interaction.channel.name}` deleted | Action: `{button.label}`",
                    color=disnake.Color.red()
                )
                log_embed.set_author(
                    name=interaction.author.name,
                    icon_url=interaction.author.avatar.url
                )
                if ticket_log_channel:
                    await ticket_log_channel.send(
                        embed=log_embed
                    )
                else:
                    await interaction.followup.send(
                        content="_No ticket log channel set_. Skipped it!",
                        ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    content="_No ticket log channel set_",
                    ephemeral=True
                )

            # delete channel
            await asyncio.sleep(3.5)
            await interaction.channel.delete()

        else:
            await interaction.followup.send(
                "You do not have the permissions to use this button",
                ephemeral=True
            )

    @disnake.ui.button(
        label="Save",
        style=disnake.ButtonStyle.grey,
        emoji="💾",
        custom_id="persistent_view:save"
    )
    async def save_ticket(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.response.defer()

        if interaction.author.guild_permissions.manage_channels:
            # Load all jsons
            with open("json/tickets.json", "r") as f:
                ticket_data = json.load(f)
            with open("json/guild.json", "r") as f:
                guild_data = json.load(f)

            ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]["status"] = "saved"

            with open("json/tickets.json", "w") as f:
                json.dump(ticket_data, f, indent=4)

            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:
                # create log
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket `{interaction.channel.name}` saved | Action: `{button.label}`",
                    color=disnake.Color.green()
                )
                log_embed.set_author(
                    name=interaction.author.name,
                    icon_url=interaction.author.avatar.url
                )
                if ticket_log_channel:
                    await ticket_log_channel.send(
                        embed=log_embed
                    )
                else:
                    pass

                if guild_data[str(interaction.guild.id)]["ticket_save_channel"]:
                    # create and send embed
                    save_embed = disnake.Embed(
                        description=f"Ticket Saved in <#{guild_data[str(interaction.guild.id)]['ticket_save_channel']}>",
                        color=disnake.Color.blue()
                    )
                    await interaction.followup.send(
                        embed=save_embed
                    )

                    transcript_channel_id = guild_data[str(interaction.guild.id)]["ticket_save_channel"]

                    transcript_channel = disnake.utils.get(
                        interaction.guild.channels,
                        id=transcript_channel_id
                    )

                    tz = pytz.timezone('Europe/Berlin')
                    fileName = f"{interaction.channel.name}.txt"
                    with open(fileName, "w+", encoding="UTF-8") as file:
                        file.write(
                            f"[INFO]\n "
                            f"Server : {interaction.guild.name} ({interaction.guild.id})\n "
                            f"Channel: {interaction.channel.name} ({interaction.channel.id})\n\n\n"
                        )
                        async for msg in interaction.channel.history(limit=9999999):
                            file.write(
                                f"{msg.created_at.astimezone(tz=tz).strftime('%d.%m.%Y %H:%M:%S')} - {msg.author.display_name}: {msg.content}\n"
                            )

                        file.close()

                        if transcript_channel:
                            await transcript_channel.send(
                                file=disnake.File(fileName)
                            )
                            os.remove(fileName)
                        else:
                            pass
                else:
                    await interaction.followup.send(
                        content="_No ticket save channel set_. Skipped it!",
                        ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    content="_No ticket log channel set_. Skipped it!",
                    ephemeral=True
                )
        else:
            await interaction.followup.send(
                "You do not have the permissions to use this button",
                ephemeral=True
            )


class close_message(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(
        label="Close",
        style=disnake.ButtonStyle.grey,
        emoji="🔒",
        custom_id="persistent_view:close"
    )
    async def close_ticket(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.response.defer()

        # Load all jsons and json stuff
        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]["status"] = "closed"

        with open("json/tickets.json", "w") as f:
            json.dump(ticket_data, f, indent=4)

        # Setup variables and perms
        ticket_id = interaction.channel.id
        ticket_author = disnake.utils.get(
            interaction.guild.members,
            id=int(ticket_data[str(interaction.guild.id)][str(ticket_id)]["author"])
        )
        close_ticket_category = disnake.utils.get(
            interaction.guild.categories,
            id=int(guild_data[str(interaction.guild.id)]["closed_ticket_category"])
        )

        await interaction.channel.set_permissions(
            ticket_author,
            send_messages=False,
            read_messages=False
        )

        close_embed = disnake.Embed(
            description=f"Ticket Closed by {interaction.author.mention}",
            color=disnake.Color.yellow()
        )
        view = open_message()
        await interaction.followup.send(
            embed=close_embed,
            view=view
        )

        if guild_data[str(interaction.guild.id)]["closed_ticket_category"]:
            await interaction.channel.edit(
                category=close_ticket_category
            )

            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:
                # create log
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket <#{interaction.channel.id}> closed | Action: `{button.label}`",
                    color=disnake.Color.yellow()
                )
                log_embed.set_author(
                    name=interaction.author.name,
                    icon_url=interaction.author.avatar.url
                )
                if ticket_log_channel:
                    await ticket_log_channel.send(
                        embed=log_embed
                    )
                else:
                    await interaction.followup.send(
                        content="_Counldn't resolve log channel_! Skipped it!",
                        ephemeral=True
                )
            else:
                await interaction.followup.send(
                    content="_No ticket log channel set_! Skipped it!",
                    ephemeral=True
                )
        else:
            await interaction.followup.send(
                content="_No category for closed tickets set_! Skiped it!",
                ephemeral=True
            )


class ticket_message(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    # BUTTONS
    @disnake.ui.button(
        label="General",
        style=disnake.ButtonStyle.green,
        emoji="📩",
        custom_id="persistent_view:general_ticket"
    )
    async def tickets(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.response.defer(ephemeral=True)

        # Load all jsons
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)
        with open("json/tickets.json", "r", encoding="UTF-8") as f:
            ticket_data = json.load(f)

        if guild_data[str(interaction.guild.id)]["ticket_category"]:

            # Setup variables and perms
            ticket_category_id = disnake.utils.get(
                interaction.guild.categories,
                id=guild_data[str(interaction.guild.id)]["ticket_category"]
            )
            ticket = await interaction.guild.create_text_channel(
                name=f"ticket-{ticket_data[str(interaction.guild.id)]['ticket_counter']}",
                reason="Ticketsystem",
                category=ticket_category_id,
                overwrites={
                    interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                    interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.guild.me: disnake.PermissionOverwrite(read_messages=True)
                }
            )

            for i in ticket_data[str(interaction.guild.id)]["support_roles"]:
                await ticket.set_permissions(disnake.utils.get(interaction.guild.roles, id=i), read_messages=True, send_messages=True)

            for i in ticket_data[str(interaction.guild.id)]["support_members"]:
                await ticket.set_permissions(disnake.utils.get(interaction.guild.members, id=i), read_messages=True, send_messages=True)

            # Json Stuff
            ticket_data[str(interaction.guild.id)][ticket.id] = {}
            ticket_data[str(interaction.guild.id)][ticket.id]["author"] = interaction.author.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_id"] = ticket.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_name"] = ticket.name
            ticket_data[str(interaction.guild.id)][ticket.id]["ticket_number"] = ticket_data[str(interaction.guild.id)]["ticket_counter"]
            ticket_data[str(interaction.guild.id)][ticket.id]["status"] = "open"

            ticket_data[str(interaction.guild.id)]["ticket_counter"] += 1

            with open("json/tickets.json", "w", encoding="UTF-8") as f:
                json.dump(ticket_data, f, indent=4)

            # Change channel and create embed
            await ticket.edit(topic=f"General Ticket | {interaction.author.name}")
            begin_embed = disnake.Embed(
                description="Support will be shortly with you! To close the ticket react with 🔒\n"
                            "Please ask your question",
                color=disnake.Color.green()
            )
            begin_embed.add_field(
                name="Category",
                value=f"`{button.label}`",
                inline=True
            )
            begin_embed.add_field(
                name="Author",
                value=interaction.author.mention,
                inline=True
            )
            role_list = []
            for role in ticket_data[str(interaction.guild.id)]['ping_roles']:
                role_list.append(f"<@&{role}>")

            await ticket.send(
                content=f"{interaction.author.mention} please ask your question!\n||Pingroles: {' '.join(role_list) if role_list else 'N/A'}||",
                embed=begin_embed,
                view=close_message()
            )

            await interaction.edit_original_response(
                content=f"_General Ticket successfully created!_ <#{ticket.id}>"
            )

            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:

                # create log
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket created | Action: `{button.label}`",
                    color=disnake.Color.green()
                )
                log_embed.set_author(
                    name=interaction.author.name,
                    icon_url=interaction.author.avatar.url
                )
                if ticket_log_channel:
                    await ticket_log_channel.send(
                        embed=log_embed
                    )
                else:
                    await interaction.followup.send(
                        content="_Counldn't resolve log channel_! Skipped it!",
                        ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    content="_Ticket Logging channel not set!_ Skipped it!",
                    ephemeral=True
                )
        else:
            await interaction.followup.send(
                content="_Ticket Category not set!_ Skipped it!",
                ephemeral=True
            )

    # BUTTONS
    @disnake.ui.button(
        label="Moderation",
        style=disnake.ButtonStyle.green,
        emoji="🔨",
        custom_id="persistent_view:moderation_ticket"
    )
    async def tickets1(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.response.defer(ephemeral=True)

        # Load all jsons
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)
        with open("json/tickets.json", "r", encoding="UTF-8") as f:
            ticket_data = json.load(f)

        if guild_data[str(interaction.guild.id)]["ticket_category"]:
            # Setup variables and perms
            ticket_category_id = disnake.utils.get(
                interaction.guild.categories,
                id=guild_data[str(interaction.guild.id)]["ticket_category"]
            )
            ticket = await interaction.guild.create_text_channel(
                name=f"ticket-{ticket_data[str(interaction.guild.id)]['ticket_counter']}",
                reason="Ticketsystem",
                category=ticket_category_id,
                overwrites={
                    interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                    interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.guild.me: disnake.PermissionOverwrite(read_messages=True)
                }
            )

            for i in ticket_data[str(interaction.guild.id)]["support_roles"]:
                await ticket.set_permissions(disnake.utils.get(interaction.guild.roles, id=i), read_messages=True, send_messages=True)

            for i in ticket_data[str(interaction.guild.id)]["support_members"]:
                await ticket.set_permissions(disnake.utils.get(interaction.guild.members, id=i), read_messages=True, send_messages=True)

            # Json Stuff
            ticket_data[str(interaction.guild.id)][ticket.id] = {}
            ticket_data[str(interaction.guild.id)][ticket.id]["author"] = interaction.author.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_id"] = ticket.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_name"] = ticket.name
            ticket_data[str(interaction.guild.id)][ticket.id]["ticket_number"] = ticket_data[str(interaction.guild.id)]["ticket_counter"]
            ticket_data[str(interaction.guild.id)][ticket.id]["status"] = "open"

            ticket_data[str(interaction.guild.id)]["ticket_counter"] += 1

            with open("json/tickets.json", "w", encoding="UTF-8") as f:
                json.dump(ticket_data, f, indent=4)

            # Change channel name and create embed
            await ticket.edit(
                topic=f"Moderation Ticket | {interaction.author.name}"
            )
            begin_embed = disnake.Embed(
                description="Support will be shortly with you! To close the ticket react with 🔒\n"
                            "Please ask your question",
                color=disnake.Color.green()
            )
            begin_embed.add_field(
                name="Category",
                value=f"`{button.label}`",
                inline=True
            )
            begin_embed.add_field(
                name="Author",
                value=interaction.author.mention,
                inline=True
            )
            role_list = []
            for role in ticket_data[str(interaction.guild.id)]['ping_roles']:
                role_list.append(f"<@&{role}>")

            await ticket.send(
                content=f"{interaction.author.mention} please ask your question!\n||Pingroles: {' '.join(role_list) if role_list else 'N/A'}||",
                embed=begin_embed,
                view=close_message()
            )

            await interaction.edit_original_response(
                content=f"_Moderation ticket successfully created!_ <#{ticket.id}>"
            )

            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:
                # create log
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket Created by {interaction.author.mention} | Action: `{button.label}`",
                    color=disnake.Color.green()
                )
                log_embed.set_author(name=interaction.author.name, icon_url=interaction.author.avatar.url)
                if ticket_log_channel:
                    await ticket_log_channel.send(
                        embed=log_embed
                    )
                else:
                    await interaction.followup.send(
                        content="_Counldn't resolve log channel_! Skipped it!",
                        ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    content="_Ticket Logging channel not set!_ Skipped it!",
                    ephemeral=True
                )
        else:
            await interaction.followup.send(
                content="_Ticket category not set!_ Skipped it!",
                ephemeral=True
            )

    # BUTTONS
    @disnake.ui.button(
        label="Support",
        style=disnake.ButtonStyle.green,
        emoji="❔",
        custom_id="persistent_view:support_ticket"
    )
    async def tickets2(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.edit_original_response(ephermal=True)

        # Load all jsons
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)
        with open("json/tickets.json", "r", encoding="UTF-8") as f:
            ticket_data = json.load(f)

        if guild_data[str(interaction.guild.id)]["ticket_category"]:
            # Setup variables and perms
            ticket_category_id = disnake.utils.get(
                interaction.guild.categories,
                id=guild_data[str(interaction.guild.id)]["ticket_category"]
            )

            ticket = await interaction.guild.create_text_channel(
                name=f"ticket-{ticket_data[str(interaction.guild.id)]['ticket_counter']}",
                reason="Ticketsystem",
                category=ticket_category_id,
                overwrites={
                    interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                    interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.guild.me: disnake.PermissionOverwrite(read_messages=True)
                }
            )

            for i in ticket_data[str(interaction.guild.id)]["support_roles"]:
                await ticket.set_permissions(disnake.utils.get(interaction.guild.roles, id=i), read_messages=True, send_messages=True)

            for i in ticket_data[str(interaction.guild.id)]["support_members"]:
                await ticket.set_permissions(disnake.utils.get(interaction.guild.members, id=i), read_messages=True, send_messages=True)

            # Json Stuff
            ticket_data[str(interaction.guild.id)][ticket.id] = {}
            ticket_data[str(interaction.guild.id)][ticket.id]["author"] = interaction.author.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_id"] = ticket.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_name"] = ticket.name
            ticket_data[str(interaction.guild.id)][ticket.id]["ticket_number"] = ticket_data[str(interaction.guild.id)]["ticket_counter"]
            ticket_data[str(interaction.guild.id)][ticket.id]["status"] = "open"

            ticket_data[str(interaction.guild.id)]["ticket_counter"] += 1

            with open("json/tickets.json", "w", encoding="UTF-8") as f:
                json.dump(ticket_data, f, indent=4)

            # Change channel name and create embed
            await ticket.edit(
                topic=f"Support Ticket | {interaction.author.name}"
            )
            begin_embed = disnake.Embed(
                description="Support will be shortly with you! To close the ticket react with 🔒\n"
                            "Please ask your question",
                color=disnake.Color.green()
            )
            begin_embed.add_field(
                name="Category",
                value=f"`{button.label}`",
                inline=True
            )
            begin_embed.add_field(
                name="Author",
                value=interaction.author.mention,
                inline=True
            )

            role_list = []
            for role in ticket_data[str(interaction.guild.id)]['ping_roles']:
                role_list.append(f"<@&{role}>")

            await ticket.send(
                content=f"{interaction.author.mention} please ask your question!\n||Pingroles: {' '.join(role_list) if role_list else 'N/A'}||",
                embed=begin_embed,
                view=close_message()
            )

            await interaction.edit_original_response(
                content=f"_Support Ticket successfully created!_ <#{ticket.id}>"
            )

            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:
                # create log
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket Created by {interaction.author.mention} | Action: `{button.label}`",
                    color=disnake.Color.green()
                )
                log_embed.set_author(name=interaction.author.name, icon_url=interaction.author.avatar.url)
                if ticket_log_channel:
                    await ticket_log_channel.send(
                        embed=log_embed
                    )
                else:
                    await interaction.followup.send(
                        content="_Counldn't resolve log channel_! Skipped it!",
                        ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    content="_Ticket Logging channel not set!_ Skipped it!",
                    ephemeral=True
                )
        else:
            await interaction.followup.send(
                content="_Ticket category not set!_ Skipped it!",
                ephemeral=True
            )


class tjan_ticket(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    # BUTTONS
    @disnake.ui.button(
        label="Support",
        style=disnake.ButtonStyle.green,
        emoji="❔",
        custom_id="persistent_view:support_ticket"
    )
    async def tickets2(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.response.defer(ephemeral=True)

        # Load all jsons
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)
        with open("json/tickets.json", "r", encoding="UTF-8") as f:
            ticket_data = json.load(f)

        if guild_data[str(interaction.guild.id)]["ticket_category"]:
            # Setup variables and perms
            ticket_category_id = disnake.utils.get(
                interaction.guild.categories,
                id=guild_data[str(interaction.guild.id)]["ticket_category"]
            )

            ticket = await interaction.guild.create_text_channel(
                name=f"mc-ticket-{ticket_data[str(interaction.guild.id)]['ticket_counter']}",
                reason="Ticketsystem",
                category=ticket_category_id,
                overwrites={
                    interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                    interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.guild.me: disnake.PermissionOverwrite(read_messages=True)
                }
            )
            # 929752696834117733 -> mcteam role
            await ticket.set_permissions(disnake.utils.get(interaction.guild.roles, id=929752696834117733), read_messages=True, send_messages=True)

            # Json Stuff
            ticket_data[str(interaction.guild.id)][ticket.id] = {}
            ticket_data[str(interaction.guild.id)][ticket.id]["author"] = interaction.author.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_id"] = ticket.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_name"] = ticket.name
            ticket_data[str(interaction.guild.id)][ticket.id]["ticket_number"] = ticket_data[str(interaction.guild.id)]["ticket_counter"]
            ticket_data[str(interaction.guild.id)][ticket.id]["status"] = "open"

            ticket_data[str(interaction.guild.id)]["ticket_counter"] += 1

            with open("json/tickets.json", "w", encoding="UTF-8") as f:
                json.dump(ticket_data, f, indent=4)

            # Change channel name and create embed
            await ticket.edit(
                topic=f"Minecraft Support Ticket | {interaction.author.name}"
            )
            begin_embed = disnake.Embed(
                description="Support will be shortly with you! To close the ticket react with 🔒\n"
                            "Please ask your question",
                color=disnake.Color.green()
            )
            begin_embed.add_field(
                name="Category",
                value=f"`{button.label}`",
                inline=True
            )
            begin_embed.add_field(
                name="Author",
                value=interaction.author.mention,
                inline=True
            )

            role_list = ["<@&929752696834117733>"]

            await ticket.send(
                content=f"{interaction.author.mention} please ask your question!\n||Pingroles: {' '.join(role_list) if role_list else 'N/A'}||",
                embed=begin_embed,
                view=close_message()
            )

            await interaction.edit_original_response(
                content=f"_Support Ticket successfully created!_ <#{ticket.id}>"
            )

            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:
                # create log
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket Created by {interaction.author.mention} | Action: `{button.label}`",
                    color=disnake.Color.green()
                )
                log_embed.set_author(name=interaction.author.name, icon_url=interaction.author.avatar.url)
                if ticket_log_channel:
                    await ticket_log_channel.send(
                        embed=log_embed
                    )
                else:
                    await interaction.followup.send(
                        content="_Counldn't resolve log channel_! Skipped it!",
                        ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    content="_Ticket Logging channel not set!_ Skipped it!",
                    ephemeral=True
                )
        else:
            await interaction.followup.send(
                content="_Ticket category not set!_ Skipped it!",
                ephemeral=True
            )

    # BUTTONS
    @disnake.ui.button(
        label="Bug melden",
        style=disnake.ButtonStyle.green,
        emoji="🔨",
        custom_id="persistent_view:moderation_ticket"
    )
    async def tickets1(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        await interaction.response.defer(ephemeral=True)

        # Load all jsons
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)
        with open("json/tickets.json", "r", encoding="UTF-8") as f:
            ticket_data = json.load(f)

        if guild_data[str(interaction.guild.id)]["ticket_category"]:
            # Setup variables and perms
            ticket_category_id = disnake.utils.get(
                interaction.guild.categories,
                id=guild_data[str(interaction.guild.id)]["ticket_category"]
            )
            ticket = await interaction.guild.create_text_channel(
                name=f"mc-ticket-{ticket_data[str(interaction.guild.id)]['ticket_counter']}",
                reason="Ticketsystem",
                category=ticket_category_id,
                overwrites={
                    interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                    interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.guild.me: disnake.PermissionOverwrite(read_messages=True)
                }
            )

            # 925692997247590420 -> developer role
            # 929752696834117733 -> mcteam role
            await ticket.set_permissions(disnake.utils.get(interaction.guild.roles, id=925692997247590420), read_messages=True, send_messages=True)
            await ticket.set_permissions(disnake.utils.get(interaction.guild.roles, id=929752696834117733), read_messages=True, send_messages=True)

            # Json Stuff
            ticket_data[str(interaction.guild.id)][ticket.id] = {}
            ticket_data[str(interaction.guild.id)][ticket.id]["author"] = interaction.author.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_id"] = ticket.id
            ticket_data[str(interaction.guild.id)][ticket.id]["channel_name"] = ticket.name
            ticket_data[str(interaction.guild.id)][ticket.id]["ticket_number"] = ticket_data[str(interaction.guild.id)]["ticket_counter"]
            ticket_data[str(interaction.guild.id)][ticket.id]["status"] = "open"

            ticket_data[str(interaction.guild.id)]["ticket_counter"] += 1

            with open("json/tickets.json", "w", encoding="UTF-8") as f:
                json.dump(ticket_data, f, indent=4)

            # Change channel name and create embed
            await ticket.edit(
                topic=f"Minecraft Bug Ticket | {interaction.author.name}"
            )
            begin_embed = disnake.Embed(
                description="Support will be shortly with you! To close the ticket react with 🔒\n"
                            "Please ask your question",
                color=disnake.Color.green()
            )
            begin_embed.add_field(
                name="Category",
                value=f"`{button.label}`",
                inline=True
            )
            begin_embed.add_field(
                name="Author",
                value=interaction.author.mention,
                inline=True
            )
            role_list = ["<@&925692997247590420>"]

            await ticket.send(
                content=f"{interaction.author.mention} please ask your question!\n||Pingroles: {' '.join(role_list) if role_list else 'N/A'}||",
                embed=begin_embed,
                view=close_message()
            )

            await interaction.edit_original_response(
                content=f"_Ticket successfully created!_ <#{ticket.id}>"
            )

            if guild_data[str(interaction.guild.id)]["ticket_log_channel"]:
                # create log
                ticket_log_channel = disnake.utils.get(
                    interaction.guild.channels,
                    id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
                )
                log_embed = disnake.Embed(
                    title="Ticket Logging",
                    description=f"Ticket Created by {interaction.author.mention} | Action: `{button.label}`",
                    color=disnake.Color.green()
                )
                log_embed.set_author(name=interaction.author.name, icon_url=interaction.author.avatar.url)
                if ticket_log_channel:
                    await ticket_log_channel.send(
                        embed=log_embed
                    )
                else:
                    await interaction.followup.send(
                        content="_Counldn't resolve log channel_! Skipped it!",
                        ephemeral=True
                    )
            else:
                await interaction.followup.send(
                    content="_Ticket Logging channel not set!_ Skipped it!",
                    ephemeral=True
                )
        else:
            await interaction.followup.send(
                content="_Ticket category not set!_ Skipped it!",
                ephemeral=True
            )


class TicketSystem(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot
        self.persistent_views_added = False

    @commands.slash_command(
        name="ticket",
    )
    async def ticket(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    # Load all jsons
    with open("json/guild.json", "r") as f:
        guild = json.load(f)

    # Create command
    @ticket.sub_command(
        name="send",
        description="Send a ticket to the support team"
    )
    async def send(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer()

        if interaction.author.guild_permissions.manage_channels:

            # Create embed
            view = ticket_message()
            ticket_embed = disnake.Embed(
                title="Ticketsystem",
                description="Reagiere mit 📩, 🔨 oder ❔ um ein Ticket zu erstellen!",
                color=disnake.Color.green()
            )

            # send embed with buttons
            await interaction.edit_original_response(
                embed=ticket_embed,
                view=view
            )
        else:
            await interaction.edit_original_response(
                content="You don't have the permissions to use this command!"
            )

    @right_guild(813318225655496724)
    @ticket.sub_command(
        name="custom",
        description="Create a custom ticket category"
    )
    async def custom(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer()

        if interaction.author.guild_permissions.manage_channels:
            # Create embed
            view = tjan_ticket()
            ticket_embed = disnake.Embed(
                title="Minecraft Ticketsystem",
                description="Reagiere mit 🔨 oder ❔ um ein Ticket zu erstellen!",
                color=disnake.Color.green()
            )

            # send embed with buttons
            await interaction.edit_original_response(
                embed=ticket_embed,
                view=view
            )
        else:
            await interaction.edit_original_response(
                content="You don't have the permissions to use this command!"
            )

    @ticket.sub_command_group(
        name="supporter"
    )
    async def supporter(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @supporter.sub_command(
        name="add",
        description="Add a category to the ticket system"
    )
    async def add(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
        role: disnake.Role = None
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        for i in ticket_data[str(interaction.guild.id)]["support_roles"]:
            print(i)

        if member:
            ticket_data[str(interaction.guild.id)]["support_members"] += [member.id]

            with open("json/tickets.json", "w", encoding="UTF-8") as f:
                json.dump(ticket_data, f, indent=4)

            embed = disnake.Embed(
                title="Ticket System",
                description=f"{member.mention} added to support members",
                color=disnake.Color.green()
            )
            await interaction.edit_original_response(
                embed=embed
            )

        elif role:
            ticket_data[str(interaction.guild.id)]["support_roles"] += [role.id]

            with open("json/tickets.json", "w", encoding="UTF-8") as f:
                json.dump(ticket_data, f, indent=4)

            embed = disnake.Embed(
                title="Ticket System",
                description=f"{role.mention} added to support roles",
                color=disnake.Color.green()
            )
            await interaction.edit_original_response(
                embed=embed
            )

        else:
            embed = disnake.Embed(
                title="Ticket System",
                description="Please specify a member or a role!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_response(
                embed=embed
            )

    @supporter.sub_command(
        name="remove",
        description="Remove a role or member from the ticket system"
    )
    async def remove(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
        role: disnake.Role = None
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        if member:
            if member.id in ticket_data[str(interaction.guild.id)]["support_members"]:

                ticket_data[str(interaction.guild.id)]["support_members"].remove(member.id)

                with open("json/tickets.json", "w", encoding="UTF-8") as f:
                    json.dump(ticket_data, f, indent=4)

                embed = disnake.Embed(
                    title="Ticket System",
                    description=f"{member.mention} removed from support members",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_response(
                    embed=embed
                )

            elif member.id not in ticket_data[str(interaction.guild.id)]["support_members"]:
                embed = disnake.Embed(
                    title="Ticket System",
                    description=f"{member.mention} is not in support members",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_response(
                    embed=embed
                )

        elif role:
            if role.id in ticket_data[str(interaction.guild.id)]["support_roles"]:

                ticket_data[str(interaction.guild.id)]["support_roles"].remove(role.id)

                with open("json/tickets.json", "w", encoding="UTF-8") as f:
                    json.dump(ticket_data, f, indent=4)

                embed = disnake.Embed(
                    title="Ticket System",
                    description=f"{role.mention} removed from support roles",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_response(
                    embed=embed
                )

            elif role.id not in ticket_data[str(interaction.guild.id)]["support_roles"]:
                embed = disnake.Embed(
                    title="Ticket System",
                    description=f"{role.mention} is not in support roles",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_response(
                    embed=embed
                )

    @supporter.sub_command(
        name="list",
        description="List all the roles and members in the ticket system"
    )
    async def list(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        support_members = ""
        support_roles = ""

        for i in ticket_data[str(interaction.guild.id)]["support_members"]:
            support_members += f"- {interaction.guild.get_member(i).mention}\n"

        for i in ticket_data[str(interaction.guild.id)]["support_roles"]:
            support_roles += f"- {interaction.guild.get_role(i).mention}\n"

        embed = disnake.Embed(
            title="Ticket System",
            description=f"`»`Support members:\n{support_members}\n`»`Support roles:\n{support_roles}",
            color=disnake.Color.green()
        )
        await interaction.edit_original_response(
            embed=embed
        )

    @ticket.sub_command_group(
        name="pingroles",
        description="adds pingroles"
    )
    async def pingroles(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        pass

    @pingroles.sub_command(
        name="add",
        description="Add a category to the ticket system"
    )
    async def pingrole_add(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        role: disnake.Role = None
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        for i in ticket_data[str(interaction.guild.id)]["ping_roles"]:
            print(i)

        if role:
            ticket_data[str(interaction.guild.id)]["ping_roles"] += [role.id]

            with open("json/tickets.json", "w", encoding="UTF-8") as f:
                json.dump(ticket_data, f, indent=4)

            embed = disnake.Embed(
                title="Ticket System",
                description=f"{role.mention} added to ping roles",
                color=disnake.Color.green()
            )
            await interaction.edit_original_response(
                embed=embed
            )

        else:
            embed = disnake.Embed(
                title="Ticket System",
                description="Please specify a member or a role!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_response(
                embed=embed
            )

    @pingroles.sub_command(
        name="remove",
        description="Remove a role or member from the ticket system"
    )
    async def pingrole_remove(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        role: disnake.Role = None
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        if role:
            if role.id in ticket_data[str(interaction.guild.id)]["ping_roles"]:

                ticket_data[str(interaction.guild.id)]["ping_roles"].remove(role.id)

                with open("json/tickets.json", "w", encoding="UTF-8") as f:
                    json.dump(ticket_data, f, indent=4)

                embed = disnake.Embed(
                    title="Ticket System",
                    description=f"{role.mention} removed from ping roles",
                    color=disnake.Color.green()
                )
                await interaction.edit_original_response(
                    embed=embed
                )

            elif role.id not in ticket_data[str(interaction.guild.id)]["ping_roles"]:
                embed = disnake.Embed(
                    title="Ticket System",
                    description=f"{role.mention} is not in ping roles",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_response(
                    embed=embed
                )

    @pingroles.sub_command(
        name="list",
        description="List all the roles and members in the ticket system"
    )
    async def pingrole_list(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)

        ping_roles = ""

        for i in ticket_data[str(interaction.guild.id)]["ping_roles"]:
            ping_roles += f"- {interaction.guild.get_role(i).mention}\n"

        embed = disnake.Embed(
            title="Ticket System",
            description=f"`»`Pinged roles:\n{ping_roles}",
            color=disnake.Color.green()
        )
        await interaction.edit_original_response(
            embed=embed
        )

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.persistent_views_added:
            view1 = ticket_message()
            view2 = close_message()
            view3 = open_message()
            view4 = tjan_ticket()
            self.bot.add_view(view1)
            self.bot.add_view(view2)
            self.bot.add_view(view3)
            self.bot.add_view(view4)
            self.persistent_views_added = True


def setup(bot):
    bot.add_cog(TicketSystem(bot))
