import disnake
from disnake.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        description="Check every server´the bot is in"
    )
    @commands.is_owner()
    async def allserver(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        msg = "```js\n"
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
        msg += "|      Insgesamt      |-----------------------| {!s:>6s} |----------------------|\n".format(len(set(self.bot.get_all_members())))
        msg += "```"
        await interaction.response.send_message(msg)


def setup(bot):
    bot.add_cog(Owner(bot))
