import disnake
from disnake.ext import commands
import json


class joinToCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="join_to_create",
    )
    async def join_to_create(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @join_to_create.sub_command(
        name="name",
        description="Change the name of the voice channel"
    )
    async def change_name(self, interaction: disnake.ApplicationCommandInteraction, *, name):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            voice_channel_id = interaction.author.voice.channel.id
            with open("json/join_to_create.json", "r", encoding="UTF-8") as json_file:
                data = json.load(json_file)

            if data["jtcc"][str(voice_channel_id)]["owner"] == interaction.author.id:

                voice_channel = disnake.utils.get(
                    interaction.author.guild.voice_channels,
                    id=voice_channel_id
                )
                await voice_channel.edit(name=name)

                data["jtcc"][str(voice_channel_id)]["channel_name"] = name
                with open("json/join_to_create.json", "w", encoding="UTF-8") as json_file:
                    json.dump(data, json_file, indent=4)
                change_embed = disnake.Embed(
                    title="Successfully changed the name of your voice channel",
                    description=f"{interaction.author.mention}, I changed the name of your voice channel [{voice_channel.mention}] to `{name}`",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=change_embed,
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    content="You are not the owner of this voice channel",
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="kick",
        description="Kick a member from your voice channel"
    )
    async def kick_member(self, interaction: disnake.ApplicationCommandInteraction, *, member: disnake.Member):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            voice_channel_id = interaction.author.voice.channel.id

            if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                await member.edit(voice_channel=None)

                kick_embed = disnake.Embed(
                    title="Successfully kicked a member from your voice channel",
                    description=f"{interaction.author.mention}, I kicked {member.mention} from your voice channel [<#{voice_channel_id}>]",
                    color=disnake.Color.orange()
                )
                await interaction.response.send_message(
                    embed=kick_embed,
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="delete",
        description="Deletes the voice channel"
    )
    async def delete_voice_channel(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            voice_channel_id = interaction.author.voice.channel.id

            if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                await interaction.author.voice.channel.delete()

                del data["jtcc"][str(voice_channel_id)]

                with open("json/join_to_create.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)

                close_embed = disnake.Embed(
                    title="Successfully deleted your voice channel",
                    description=f"{interaction.author.mention}, I deleted your voice channel",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=close_embed,
                    ephemeral=True
                )
            else:
                not_owner_embed = disnake.Embed(
                    description=f"{interaction.author.mention}, you are not the owner of this voice channel!"
                )
                await interaction.response.send_message(
                    embed=not_owner_embed,
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="private",
        description="Change the voice channel to private"
    )
    async def change_voice_channel_to_private(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            if data["jtcc"][str(interaction.author.voice.channel.id)]["state"] == "public":

                voice_channel_id = interaction.author.voice.channel.id

                if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                    await interaction.author.voice.channel.set_permissions(
                        interaction.guild.default_role,
                        connect=False
                    )

                    data["jtcc"][str(voice_channel_id)]["state"] = "private"

                    with open("json/join_to_create.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)

                    private_embed = disnake.Embed(
                        title="Successfully changed your voice channel to private",
                        description=f"{interaction.author.mention}, I changed your voice channel [<#{voice_channel_id}>] to private. No one can join your voice channel anymore",
                        color=disnake.Color.green()
                    )
                    await interaction.response.send_message(
                        embed=private_embed,
                        ephemeral=True
                    )
                else:
                    not_owner_embed = disnake.Embed(
                        description=f"{interaction.author.mention}, you are not the owner of the voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.red()
                    )
                    await interaction.response.send_message(
                        embed=not_owner_embed,
                        ephemeral=True
                    )

            else:
                already_private_embed = disnake.Embed(
                    description=f"{interaction.author.mention}, your voice channel is **already private**",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=already_private_embed,
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="public",
        description="Change the voice channel to public"
    )
    async def change_voice_channel_to_public(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            if data["jtcc"][str(interaction.author.voice.channel.id)]["state"] == "private":

                voice_channel_id = interaction.author.voice.channel.id

                if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                    await interaction.author.voice.channel.set_permissions(
                        interaction.guild.default_role,
                        connect=True
                    )

                    data["jtcc"][str(voice_channel_id)]["state"] = "public"

                    with open("json/join_to_create.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)

                    public_embed = disnake.Embed(
                        title="Successfully changed your voice channel to public",
                        description=f"{interaction.author.mention}, I changed your voice channel [<#{voice_channel_id}>] to `public`. Everyone can join your voice channel",
                        color=disnake.Color.green()
                    )
                    await interaction.response.send_message(
                        embed=public_embed,
                        ephemeral=True
                    )
                else:
                    not_owner_embed = disnake.Embed(
                        description=f"{interaction.author.mention}, you are not the owner of the voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.red()
                    )
                    await interaction.response.send_message(
                        embed=not_owner_embed,
                        ephemeral=True
                    )

            else:
                already_public_embed = disnake.Embed(
                    description=f"{interaction.author.mention}, your voice channel is **already public**",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=already_public_embed,
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="limit",
        description="Change the voice channel user limit"
    )
    async def change_voice_channel_user_limit(self, interaction: disnake.ApplicationCommandInteraction, limit: int):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            voice_channel_id = interaction.author.voice.channel.id

            if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                await interaction.author.voice.channel.edit(
                    user_limit=limit
                )

                limit_embed = disnake.Embed(
                    title="Successfully changed your voice channel user limit",
                    description=f"{interaction.author.mention}, I changed your voice channel [<#{voice_channel_id}>] user limit to `{limit}`",
                    color=disnake.Color.green()
                )
                await interaction.response.send_message(
                    embed=limit_embed,
                    ephemeral=True
                )
            else:
                not_owner_embed = disnake.Embed(
                    description=f"{interaction.author.mention}, you are not the owner of the voice channel [<#{voice_channel_id}>]",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=not_owner_embed,
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="mute",
        description="Mute a user in the voice channel"
    )
    async def vc_mute(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            voice_channel_id = interaction.author.voice.channel.id

            if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                if interaction.author.voice.channel.permissions_for(member).speak:
                    await interaction.author.voice.channel.set_permissions(
                        member,
                        speak=False
                    )

                    mute_embed = disnake.Embed(
                        title="Successfully muted a user in your voice channel",
                        description=f"{interaction.author.mention}, I muted the user [{member.mention}] in your voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.green()
                    )
                    await interaction.response.send_message(
                        embed=mute_embed,
                        ephemeral=True
                    )
                else:
                    already_mute_embed = disnake.Embed(
                        description=f"{interaction.author.mention}, the user [{member.mention}] is already muted in your voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.red()
                    )
                    await interaction.response.send_message(
                        embed=already_mute_embed,
                        ephemeral=True
                    )
            else:
                not_owner_embed = disnake.Embed(
                    description=f"{interaction.author.mention}, you are not the owner of the voice channel [<#{voice_channel_id}>]",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=not_owner_embed,
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="unmute",
        description="Unmute a user in the voice channel"
    )
    async def vc_unmute(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            voice_channel_id = interaction.author.voice.channel.id

            if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                if not interaction.author.voice.channel.permissions_for(member).speak:
                    await interaction.author.voice.channel.set_permissions(
                        member,
                        speak=True
                    )

                    unmute_embed = disnake.Embed(
                        title="Successfully unmuted a user in your voice channel",
                        description=f"{interaction.author.mention}, I unmuted the user [{member.mention}] in your voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.green()
                    )
                    await interaction.response.send_message(
                        embed=unmute_embed,
                        ephemeral=True
                    )
                else:
                    already_unmuted_embed = disnake.Embed(
                        description=f"{interaction.author.mention}, the user [{member.mention}] is already unmuted in your voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.red()
                    )
                    await interaction.response.send_message(
                        embed=already_unmuted_embed,
                        ephemeral=True
                    )
            else:
                not_owner_embed = disnake.Embed(
                    description=f"{interaction.author.mention}, you are not the owner of the voice channel [<#{voice_channel_id}>]",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=not_owner_embed,
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="info",
        description="Get information about the voice channel"
    )
    async def vc_info(self, interaction: disnake.ApplicationCommandInteraction):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            voice_channel_id = interaction.author.voice.channel.id

            info_embed = disnake.Embed(
                title="Voice channel information",
                description=f"{interaction.author.mention}, here is the information about your voice channel [<#{voice_channel_id}>]",
                color=disnake.Color.green()
            )
            info_embed.add_field(
                name="__Name Infos__",
                value=f" Channel Name: {interaction.author.voice.channel.mention}\n"
                        f" Channel ID: `{voice_channel_id}`\n"
                        f" Owner: <@{data['jtcc'][str(voice_channel_id)]['owner']}>\n"
                        f" Owner ID: `{data['jtcc'][str(voice_channel_id)]['owner']}`"
            )
            info_embed.add_field(
                name="__Channel Infos__",
                value=f"Channel Members: `{len(interaction.author.voice.channel.members)}`\n"
                        f"Category ID: `{interaction.author.voice.channel.category.id}`\n"
                        f"Channel Bitrate: `{interaction.author.voice.channel.bitrate}`\n"
                        f"Status: `{data['jtcc'][str(voice_channel_id)]['state']}`"
            )

            await interaction.response.send_message(
                embed=info_embed,
                ephemeral=True
            )

    @join_to_create.sub_command(
        name="ban",
        description="Ban a user from the voice channel"
    )
    async def vc_ban(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            voice_channel_id = interaction.author.voice.channel.id

            if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                if interaction.author.voice.channel.permissions_for(member).connect:
                    await interaction.author.voice.channel.set_permissions(
                        member,
                        connect=False
                    )

                    ban_embed = disnake.Embed(
                        title="Successfully banned a user from your voice channel",
                        description=f"{interaction.author.mention}, I banned the user [{member.mention}] from your voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.green()
                    )
                    await interaction.response.send_message(
                        embed=ban_embed,
                        ephemeral=True
                    )
                else:
                    already_banned_embed = disnake.Embed(
                        description=f"{interaction.author.mention}, the user [{member.mention}] is already banned from your voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.red()
                    )
                    await interaction.response.send_message(
                        embed=already_banned_embed,
                        ephemeral=True
                    )
            else:
                not_owner_embed = disnake.Embed(
                    description=f"{interaction.author.mention}, you are not the owner of the voice channel [<#{voice_channel_id}>]",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=not_owner_embed,
                    ephemeral=True
                )

    @join_to_create.sub_command(
        name="unban",
        description="Unban a user from the voice channel"
    )
    async def vc_unban(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        if interaction.author.voice is None:
            return await interaction.response.send_message(
                content="You are not in a voice channel",
                ephemeral=True
            )
        else:
            with open("json/join_to_create.json", "r") as json_file:
                data = json.load(json_file)

            voice_channel_id = interaction.author.voice.channel.id

            if interaction.author.id == data["jtcc"][str(voice_channel_id)]["owner"]:
                if not interaction.author.voice.channel.permissions_for(member).connect:
                    await interaction.author.voice.channel.set_permissions(
                        member,
                        connect=True
                    )

                    unban_embed = disnake.Embed(
                        title="Successfully unbanned a user from your voice channel",
                        description=f"{interaction.author.mention}, I unbanned the user [{member.mention}] from your voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.green()
                    )
                    await interaction.response.send_message(
                        embed=unban_embed,
                        ephemeral=True
                    )
                else:
                    already_unbanned_embed = disnake.Embed(
                        description=f"{interaction.author.mention}, the user [{member.mention}] is already unbanned from your voice channel [<#{voice_channel_id}>]",
                        color=disnake.Color.red()
                    )
                    await interaction.response.send_message(
                        embed=already_unbanned_embed,
                        ephemeral=True
                    )
            else:
                not_owner_embed = disnake.Embed(
                    description=f"{interaction.author.mention}, you are not the owner of the voice channel [<#{voice_channel_id}>]",
                    color=disnake.Color.red()
                )
                await interaction.response.send_message(
                    embed=not_owner_embed,
                    ephemeral=True
                )


def setup(bot):
    bot.add_cog(joinToCreate(bot))
