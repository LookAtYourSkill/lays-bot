import json

import disnake
from disnake.ext import commands


class Owner(commands.Cog):
    '''
    Commands for the owner of the bot
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="set")
    async def set(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @commands.is_owner()
    @set.sub_command(name="license", description="Activates/Deactivates the license system")
    async def update_license(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        with open("json/general.json", "r") as general_info:
            general = json.load(general_info)

        if general["license_check"] is False:
            on_embed = disnake.Embed(
                description="License check is now `enabled`",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=on_embed
            )

            general["license_check"] = True
            with open("json/general.json", "w") as dump_file:
                json.dump(general, dump_file, indent=4)

        else:
            off_embed = disnake.Embed(
                description="License check is now `disabled`",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=off_embed
            )

            general["license_check"] = False
            with open("json/general.json", "w") as dump_file:
                json.dump(general, dump_file, indent=4)


    @set.sub_command(
        name="allservers",
        description="Gives back all server, the bot is in"
    )
    @commands.is_owner()
    async def allserver(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        msg = "```\n"
        msg += "|        Informationen zu allen Server        |--------|----------------------|\n"
        msg += "|---------------------|-----------------------|--------|----------------------|\n"
        msg += "| {!s:19s} | {!s:21s} | {!s:>6s} | {!s:20s} |\n".format("ID", "Name", "Member", "Owner")
        msg += "|---------------------|-----------------------|--------|----------------------|\n"
        for guild in self.bot.guilds:
            string = ""
            if len(string + str(guild.name)) > 21:
                string += ".."
                guild_name_longer_19 = str(guild.name)[:18] + string
                msg += "| {!s:19s} | {!s:21s} | {!s:>6s} | {!s:20s} |\n".format(guild.id, guild_name_longer_19, guild.member_count, guild.owner)
            elif len(string + str(guild.owner)) > 21:
                string += ".."
                owner_name_longer_19 = str(guild.owner)[:18] + string
                msg += "| {!s:19s} | {!s:21s} | {!s:>6s} | {!s:20s} |\n".format(guild.id, guild.name, guild.member_count, owner_name_longer_19)
            elif len(string + guild.name) > 21 and len(string + guild.owner) > 21:
                msg += "| {!s:19s} | {!s:21s} | {!s:>6s} | {!s:20s} |\n".format(guild.id, guild_name_longer_19, guild.member_count, owner_name_longer_19)
            else:
                msg += "| {!s:19s} | {!s:21s} | {!s:>6s} | {!s:20s} |\n".format(guild.id, guild.name, guild.member_count, guild.owner)
        msg += "|---------------------|-----------------------|--------|----------------------|\n"
        msg += "|      Insgesamt      | {!s:>21s} | {!s:>6s} |----------------------|\n".format(len(self.bot.guilds), len(set(self.bot.get_all_members())))
        msg += "```"
        await interaction.edit_original_message(msg)

    @commands.is_owner()
    @set.sub_command(name="send", description="Sends a message to a user")
    async def send(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user_id,
        *,
        message: str
    ):
        await interaction.response.defer(ephemeral=True)

        user = await self.bot.fetch_user(user_id)
        embed = disnake.Embed(
            description=message,
            color=disnake.Color.green()
        )
        await user.send(embed=embed)
        await interaction.edit_original_message(
            f"Message sent to {user.mention}"
        )


def setup(bot):
    bot.add_cog(Owner(bot))
