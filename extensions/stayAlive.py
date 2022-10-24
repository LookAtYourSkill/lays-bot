import asyncio

import colorama
import disnake
from disnake.ext.tasks import loop
from disnake.ext import commands

from extensions.twitch import Twitch
from extensions.timer import Timer
from extensions.license import LicenseSystem


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

        Timer.check_timers.restart()

        LicenseSystem.license_check_expired.restart()
        LicenseSystem.license_check.restart()

        print(f" {colorama.Fore.GREEN}Restarted all tasks {colorama.Fore.RESET}")

        user = await self.bot.fetch_user(self.owner)
        embed = disnake.Embed(
            title="> Restarted all tasks",
            description="- `Twitch.check_streams`\n- `Twitch.update`\n- `Timer.check_timers`\n- `LicenseSystem.license_check_expired`\n- `LicenseSystem.license_check`",
            color=disnake.Color.green()
        )
        await user.send(embed=embed)


def setup(bot):
    bot.add_cog(stayAlive(bot))
