import datetime
import json

import colorama
import disnake
import humanfriendly
import humanize
from disnake.ext import commands
from disnake.ext.tasks import loop
from utils._time import get_time, remove_expired_timers, set_end_time

from checks._check_license import check_license


class Timer(commands.Cog):
    '''
    Timer for users per chat
    '''
    def __init__(self, bot):
        self.bot = bot
        self.check_timers.start()

    @check_license()
    @commands.slash_command(
        name="timer",
        description="Set a timer for a user"
    )
    async def timer(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @timer.sub_command(name="set", description="Creates a timer for yourself or a user")
    async def set(interaction: disnake.ApplicationCommandInteraction, time, member: disnake.Member = None, *, message: str):
        with open("json/timer.json", "r") as timer_info:
            timers = json.load(timer_info)

        if member is None:
            member = interaction.author

        real_time = humanfriendly.parse_timespan(time)

        timers[str(interaction.author.id)] = {
            "end_time": set_end_time(real_time),
            "message": message,
            "member": member.id,
            "author": interaction.author.id,
            # "messsage_id": interaction.message.id,
            "channel": interaction.channel.id
        }

        with open("json/timer.json", "w") as dump_file:
            json.dump(timers, dump_file, indent=4, default=str)

        embed = disnake.Embed(
            title="Timer",
            description=f"{interaction.author.mention} set a timer for `{humanize.naturaldelta(time)}`. I will remind you when its finished!",
            color=disnake.Color.green()
        )
        embed.add_field(
            name="Message",
            value=f"`{message}`",
            inline=False
        )
        embed.add_field(
            name="Member",
            value=member.mention,
            inline=False
        )
        embed.set_author(
            name=interaction.author.name,
            icon_url=interaction.author.avatar.url
        )
        await interaction.response.send_message(
            embed=embed
        )

    @loop(minutes=1)
    async def check_timers(self):
        await self.bot.wait_until_ready()
        print(f"{colorama.Fore.LIGHTWHITE_EX} [TIMER] [TASK] Checking timers... {colorama.Fore.RESET}")
        with open("json/timer.json", "r") as timer_info:
            timers = json.load(timer_info)

        # !! print(f"{colorama.Fore.BLUE} [TIMER] [PENDING] Removing expired timers...{colorama.Fore.RESET}")
        for timer in timers:
            date_1_string = str(timers[timer]["end_time"])
            date1 = datetime.datetime.strptime(date_1_string, "%d.%m.%Y %H:%M:%S")

            date_2_string = str(get_time())
            date2 = datetime.datetime.strptime(date_2_string, "%d.%m.%Y %H:%M:%S")

            if date1 < date2:
                # !! print(f"{colorama.Fore.GREEN} [TIMER] [SUCCESS] Timer over, removing...{colorama.Fore.RESET}")

                embed = disnake.Embed(
                    title="Timer",
                    description=f"<@{timers[timer]['author']}> your timer just finished!",
                    color=disnake.Color.green()
                )

                channel = self.bot.get_channel(timers[timer]["channel"])

                await channel.send(
                    f"<@{timers[timer]['author']}>",
                    embed=embed
                )

                timers[timer]["end_time"] = True
                with open("json/timer.json", "w") as dump_file:
                    json.dump(timers, dump_file, indent=4, default=str)

                remove_expired_timers()
            else:
                continue
                # !! print(f"{colorama.Fore.GREEN} [TIMER] [SUCCESS] Timer is still running...{colorama.Fore.RESET}")

        print(f"{colorama.Fore.LIGHTWHITE_EX} [TIMER] [DONE] Finished checking timers! {colorama.Fore.RESET}")


def setup(bot):
    bot.add_cog(Timer(bot))
