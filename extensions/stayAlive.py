import colorama
import disnake
from disnake.ext.tasks import loop
from disnake.ext import commands

from extensions.youtube import Youtube
from extensions.twitch import Twitch


class stayAlive(commands.Cog):
    '''
    Status: Working
    '''
    def __init__(
        self,
        bot
    ):
        self.bot: commands.Bot = bot
        self.owner = 493370963807830016
        self.zdt.start()

    @loop(seconds=86400)
    async def zdt(self):  # ZDT = Zero Down Time
        Twitch.check_streams.restart()
        Twitch.update.restart()
        Youtube.check_videos.restart()


        print(f" {colorama.Fore.GREEN}Restarted all tasks {colorama.Fore.RESET}")

        user = await self.bot.fetch_user(self.owner)
        embed = disnake.Embed(
            title="> Restarted all tasks",
            description="- `Twitch.check_streams`\n- `Twitch.update` \n- `Youtube.check_videos`",
            color=disnake.Color.green()
        )
        await user.send(embed=embed)


def setup(bot):
    bot.add_cog(stayAlive(bot))
