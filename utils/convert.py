import disnake
from disnake.ext import commands


class BannedUser(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.isdigit():
            member_id = int(argument)
            try:
                return await ctx.guild.fetch_ban(id=member_id)
            except disnake.NotFound:
                raise commands.BadArgument()

        ban_list = await ctx.guild.bans()
        user = disnake.utils.find(lambda u: str(u.user) == argument, ban_list)

        if user is None:
            raise commands.BadArgument()
        return user
