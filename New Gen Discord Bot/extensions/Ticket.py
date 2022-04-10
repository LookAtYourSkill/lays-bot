import asyncio
import disnake
from disnake.ext import commands
import json


class open_message(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(
        label="Open",
        style=disnake.ButtonStyle.green,
        emoji="🔓"
    )
    async def open_ticket(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        # Load all jsons
        with open("json/tickets.json", "r") as f:
            ticket_data = json.load(f)
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]["status"] = "open"

        with open("json/tickets.json", "w") as f:
            json.dump(ticket_data, f, indent=4)

        # setup variables and perms
        target = disnake.utils.get(
            interaction.guild.members,
            id=ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]["author"]
        )
        await interaction.channel.set_permissions(
            target, send_messages=True, read_messages=True
        )

        # create and send embed
        open_embed = disnake.Embed(
            description=f"Ticket Opened by {interaction.author.mention}",
            color=disnake.Color.green()
        )
        view = close_message()
        await interaction.send(
            embed=open_embed,
            view=view
        )

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
        await interaction.channel.edit(name=str(ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]["channel_name"]))

    @disnake.ui.button(
        label="Delete",
        style=disnake.ButtonStyle.red,
        emoji="🗑"
    )
    async def delete_ticket(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):
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
            await interaction.send(
                embed=delete_embed
            )

            # delete channel
            await asyncio.sleep(3.5)
            await interaction.channel.delete()

            # create log
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
            await ticket_log_channel.send(
                embed=log_embed
            )
        else:
            await interaction.send(
                "You do not have the permissions to use this button"
            )

    @disnake.ui.button(
        label="Save",
        style=disnake.ButtonStyle.grey,
        emoji="💾"
    )
    async def save_ticket(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):
        if interaction.author.guild_permissions.manage_channels:
            # Load all jsons
            with open("json/tickets.json", "r") as f:
                ticket_data = json.load(f)
            with open("json/guild.json", "r") as f:
                guild_data = json.load(f)

            ticket_data[str(interaction.guild.id)][str(interaction.channel.id)]["status"] = "saved"

            with open("json/tickets.json", "w") as f:
                json.dump(ticket_data, f, indent=4)

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
            await ticket_log_channel.send(
                embed=log_embed
            )
        else:
            await interaction.send(
                "You do not have the permissions to use this button"
            )

        # Load all jsons
        with open("json/guild.json", "r") as f:
            guild_data = json.load(f)

        # create and send embed
        save_embed = disnake.Embed(
            description=f"Ticket Saved in <#{guild_data[str(interaction.guild.id)]['ticket_save_channel']}>",
            color=disnake.Color.blue()
        )
        await interaction.send(
            embed=save_embed
        )

        # create log
        ticket_log_channel = disnake.utils.get(
            interaction.guild.channels,
            id=guild_data[str(interaction.guild.id)]["ticket_log_channel"]
        )
        log_embed = disnake.Embed(
            title="Ticket Logging",
            description=f"Ticket <#{interaction.channel.id}> saved | Action: `{button.label}`",
            color=disnake.Color.blue()
        )
        log_embed.set_author(
            name=interaction.author.name,
            icon_url=interaction.author.avatar.url
        )
        await ticket_log_channel.send(
            embed=log_embed
        )


class close_message(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(
        label="Close",
        style=disnake.ButtonStyle.grey,
        emoji="🔒"
    )
    async def close_ticket(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

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

        await interaction.channel.set_permissions(
            ticket_author,
            send_messages=False,
            read_messages=False
        )

        # edit channel and create embed
        # await interaction.channel.edit(name=f"closed {ticket_id}")

        close_embed = disnake.Embed(
            description=f"Ticket Closed by {interaction.author.mention}",
            color=disnake.Color.yellow()
        )
        view = open_message()
        await interaction.send(
            embed=close_embed,
            view=view
        )

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
        await ticket_log_channel.send(
            embed=log_embed
        )


class ticket_message(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    # BUTTONS
    @disnake.ui.button(
        label="General",
        style=disnake.ButtonStyle.green,
        emoji="📩"
    )
    async def tickets(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        # Load all jsons
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)
        with open("json/tickets.json", "r", encoding="UTF-8") as f:
            ticket_data = json.load(f)

        # Setup variables and perms
        ticket_category_id = disnake.utils.get(
            interaction.guild.categories,
            id=guild_data[str(interaction.guild.id)]["ticket_category"]
        )
        ticket = await interaction.guild.create_text_channel(
            name=f"Gen Ticket {interaction.author.name}",
            reason="Ticketsystem",
            category=ticket_category_id,
            overwrites={
                interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: disnake.PermissionOverwrite(read_messages=True)
            }
        )
        # Json Stuff
        ticket_data[str(interaction.guild.id)][ticket.id] = {}
        ticket_data[str(interaction.guild.id)][ticket.id]["author"] = interaction.author.id
        ticket_data[str(interaction.guild.id)][ticket.id]["channel_id"] = ticket.id
        ticket_data[str(interaction.guild.id)][ticket.id]["channel_name"] = ticket.name
        ticket_data[str(interaction.guild.id)][ticket.id]["status"] = "open"

        with open("json/tickets.json", "w", encoding="UTF-8") as f:
            json.dump(ticket_data, f, indent=4)

        # Change channel name and create embed
        await ticket.edit(topic=f"General Ticket | {interaction.author.name}")
        begin_embed = disnake.Embed(
            description="Support will be shortly with you! To close the ticket react with 🔒\n"
                        "Please ask your question",
            color=disnake.Color.green()
        )
        await ticket.send(
            content=f"{interaction.author.mention} please ask your question!",
            embed=begin_embed,
            view=close_message()
        )

        await interaction.response.send_message(
            content="_General Ticket erstetllt!_",
            ephemeral=True
        )

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
        await ticket_log_channel.send(
            embed=log_embed
        )

    # BUTTONS
    @disnake.ui.button(
        label="Moderation",
        style=disnake.ButtonStyle.green,
        emoji="🔨"
    )
    async def tickets1(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        # Load all jsons
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)
        with open("json/tickets.json", "r", encoding="UTF-8") as f:
            ticket_data = json.load(f)

        # Setup variables and perms
        ticket_category_id = disnake.utils.get(
            interaction.guild.categories,
            id=guild_data[str(interaction.guild.id)]["ticket_category"]
        )
        ticket = await interaction.guild.create_text_channel(
            name=f"Mod Ticket {interaction.author.name}",
            reason="Ticketsystem",
            category=ticket_category_id,
            overwrites={
                interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: disnake.PermissionOverwrite(read_messages=True)
            }
        )

        # Json Stuff
        ticket_data[str(interaction.guild.id)][ticket.id] = {}
        ticket_data[str(interaction.guild.id)][ticket.id]["author"] = interaction.author.id
        ticket_data[str(interaction.guild.id)][ticket.id]["channel_id"] = ticket.id
        ticket_data[str(interaction.guild.id)][ticket.id]["channel_name"] = ticket.name
        ticket_data[str(interaction.guild.id)][ticket.id]["status"] = "open"

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
        await ticket.send(
            content=f"{interaction.author.mention} please ask your question!",
            embed=begin_embed,
            view=close_message()
        )

        await interaction.response.send_message(
            content="_Moderation Ticket erstetllt!_",
            ephemeral=True
        )

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
        await ticket_log_channel.send(
            embed=log_embed
        )

    # BUTTONS
    @disnake.ui.button(
        label="Support",
        style=disnake.ButtonStyle.green,
        emoji="❔"
    )
    async def tickets2(
        self,
        button: disnake.ui.Button,
        interaction: disnake.MessageInteraction
    ):

        # Load all jsons
        with open("json/guild.json", "r", encoding="UTF-8") as f:
            guild_data = json.load(f)
        with open("json/tickets.json", "r", encoding="UTF-8") as f:
            ticket_data = json.load(f)

        # Setup variables and perms
        ticket_category_id = disnake.utils.get(
            interaction.guild.categories,
            id=guild_data[str(interaction.guild.id)]["ticket_category"]
        )
        ticket = await interaction.guild.create_text_channel(
            name=f"Sup Ticket {interaction.author.name}",
            reason="Ticketsystem",
            category=ticket_category_id,
            overwrites={
                interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                interaction.author: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: disnake.PermissionOverwrite(read_messages=True)
            }
        )

        # Json Stuff
        ticket_data[str(interaction.guild.id)][ticket.id] = {}
        ticket_data[str(interaction.guild.id)][ticket.id]["author"] = interaction.author.id
        ticket_data[str(interaction.guild.id)][ticket.id]["channel_id"] = ticket.id
        ticket_data[str(interaction.guild.id)][ticket.id]["channel_name"] = ticket.name
        ticket_data[str(interaction.guild.id)][ticket.id]["status"] = "open"

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
        await ticket.send(
            content=f"{interaction.author.mention} please ask your question!",
            embed=begin_embed,
            view=close_message()
        )

        await interaction.response.send_message(
            content="_Support Ticket erstetllt!_",
            ephemeral=True
        )

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
        await ticket_log_channel.send(
            embed=log_embed
        )

    # DROPDOWN MENU
    # @disnake.ui.select(
    #    options=[
    #        disnake.SelectOption(label="General", value=1, emoji="📩"),
    #        disnake.SelectOption(label="Moderation", value=2, emoji="🔨"),
    #        disnake.SelectOption(label="Support", value=3, emoji="❔")
    #    ]
    # )
    # async def ticket_select(self, select: disnake.ui.Select, interaction: disnake.MessageInteraction):
    #    pass


class ticketCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load all jsons
    with open("json/guild.json", "r") as f:
        guild = json.load(f)

    # Create command
    @commands.slash_command(
        name="sendticket",
        description="Send a ticket to the support team"
    )
    @commands.has_permissions(
        manage_guild=True
    )
    async def sendTicket(
        self,
        interaction
    ):

        # Create embed
        view = ticket_message()
        ticket_embed = disnake.Embed(
            title="Ticketsystem",
            description="Reagiere mit 📩, 🔨 oder ❔ um ein Ticket zu erstellen!",
            color=disnake.Color.green()
        )

        # send embed with buttons
        await interaction.send(
            embed=ticket_embed,
            view=view
        )


def setup(bot):
    bot.add_cog(ticketCreator(bot))
