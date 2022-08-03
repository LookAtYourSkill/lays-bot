import disnake
from disnake.ext import commands
import json


class join_to_create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        with open("json/join_to_create.json", "r") as json_file:
            data = json.load(json_file)
        with open("json/guild.json", "r") as guild_file:
            guild_data = json.load(guild_file)

        if before.channel is None and after.channel is not None:
            channel = disnake.utils.get(
                member.guild.voice_channels,
                id=guild_data[str(member.guild.id)]["join_to_create_channel"]
            )
            category = disnake.utils.get(
                member.guild.categories,
                id=guild_data[str(member.guild.id)]["join_to_create_category"]
            )
            if after.channel.id == channel.id:
                new_voice = await member.guild.create_voice_channel(
                    name=f"║🔊・{member.name}'s channel",
                    category=category,
                    overwrites={
                        member: disnake.PermissionOverwrite(
                            administrator=True
                        )
                    }
                )
                await member.move_to(new_voice)
                data["jtcc"][str(new_voice.id)] = {}
                data["jtcc"][str(new_voice.id)]["owner"] = member.id
                data["jtcc"][str(new_voice.id)]["channel_name"] = new_voice.name
                data["jtcc"][str(new_voice.id)]["channel_id"] = new_voice.id
                data["jtcc"][str(new_voice.id)]["state"] = "public"
                with open("json/join_to_create.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)

        elif len(before.channel.members) == 0:  # and after.channel is None:
            if str(before.channel.id) in data["jtcc"]:
                await before.channel.delete()

                del data["jtcc"][str(before.channel.id)]
                with open("json/join_to_create.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)
            else:
                return


def setup(bot):
    bot.add_cog(join_to_create(bot))
