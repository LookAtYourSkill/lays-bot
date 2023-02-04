import disnake
from disnake.ext import commands
import json


class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: disnake.Client = bot

    @commands.Cog.listener()
    async def on_message_delete(
        self,
        message: disnake.Message
    ):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if message.author.bot:
            return

        if not message.guild:
            return

        elif message.attachments:
            for attachment in message.attachments:
                channel = self.bot.get_channel(
                    guild_data[str(message.author.guild.id)]["msg_channel"]
                )
                if not message.content:
                    message.content = "Keine Nachricht angegeben."

                embed = disnake.Embed(
                    description=f"A message with image from {message.author.mention} was deleted in {message.channel.mention}\nContent: ``{message.content}``",
                    color=disnake.Color.red()
                )
                embed.set_image(url=attachment.url)

                if guild_data[str(message.author.guild.id)]["msg_channel"]:
                    await channel.send(embed=embed)
                else:
                    pass

        else:
            channel = self.bot.get_channel(
                guild_data[str(message.author.guild.id)]["msg_channel"]
            )
            embed = disnake.Embed(
                description=f"A message from {message.author.mention} was deleted in {message.channel.mention}",
                color=disnake.Color.red()
            )
            embed.add_field(
                name="Message",
                value=f": {message.content}",
                inline=False
            )
            if guild_data[str(message.author.guild.id)]["msg_channel"]:
                await channel.send(embed=embed)
            else:
                pass

    @commands.Cog.listener()
    async def on_message_edit(
        self,
        before: disnake.Message,
        after: disnake.Message
    ):
        with open("json/guild.json", "r", encoding="UTF-8") as data_file:
            guild_data = json.load(data_file)

        if before.author.bot:
            return
        
        # check if message is in dm
        if not before.guild:
            return

        elif not guild_data[str(before.author.guild.id)]["msg_channel"]:
            return

        else:
            # check if message is edited
            if before.content != after.content:
                channel = self.bot.get_channel(
                    guild_data[str(after.guild.id)]["msg_channel"]
                )
                embed = disnake.Embed(
                    description=f"{before.author.mention} has edited a message in {before.channel.mention} \n[Jump to the Message]({after.jump_url})",
                    color=disnake.Color.red()
                )
                embed.add_field(
                    name="Old Message",
                    value=f"{before.content}",
                    inline=False
                )
                embed.add_field(
                    name="New Message",
                    value=f"{after.content}",
                    inline=False
                )

                if guild_data[str(before.author.guild.id)]["msg_channel"]:
                    # channel is set
                    await channel.send(embed=embed)
                else:
                    # channel isnt set
                    pass
            else:
                # message isnt edited
                pass


def setup(bot):
    bot.add_cog(onMessage(bot))
