import datetime
import json
from enum import Enum

import colorama
import disnake
from disnake.ext import commands
from disnake.ext.tasks import loop
from utils.license import (
    generate,
    get_time,
    remove_expired_licenses,
    set_time_calcs
)

# for options


class Times(str, Enum):
    Day = "1 Day"
    Days = "7 Days"
    Month = "1 Month"
    Months = "3 Months"
    Months_ = "6 Months"
    Year = "1 Year"
    Lifetime = "Lifetime"


class LicenseSystem(commands.Cog):
    '''
    The License System, which the bot is based on
    '''
    def __init__(self, bot):
        self.bot = bot
        self.license_check.start()
        self.license_check_expired.start()

    @commands.slash_command(
        name="license",
        description="Shows the license"
    )
    async def license(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        pass

    @license.sub_command(
        name="info",
        description="Shows information about a license"
    )
    async def license_info(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        license
    ):
        await interaction.response.defer(
            ephemeral=True
        )

        with open("json/licenses.json", "r") as licenses:
            licenses = json.load(licenses)

        # check if license is in database
        if license in licenses:
            # put information in an embed
            embed = disnake.Embed(
                title=f"License Key: ||`{license}`|| 🔑",
                description=f"👤 Owner: `{licenses[license]['owner']}`\n"
                            f"👥 Guild: `{licenses[license]['guild']}`\n\n"
                            f"📜 Uses Left: `{licenses[license]['useability']}`\n"
                            f"⌛ Duration: `{licenses[license]['duration']}`\n\n"
                            f"Status: `{'Actived' if licenses[license]['activated'] else 'Deactivated'}`\n",
                color=disnake.Color.green()
            )
            await interaction.edit_original_message(
                embed=embed
            )

        else:
            embed = disnake.Embed(
                title="License not found ⛔",
                description="The license you entered was not found in the database.",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @license.sub_command(
        name="use",
        description="Uses a license"
    )
    async def license_use(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        license
    ):
        await interaction.response.defer(
            ephemeral=True
        )
        # check if the license is valid
        # if it is, activate it
        # continue time
        # set license to active
        # bot will work on that server

        # if not, tell the user that it is not valid
        # if the license is already activated, tell the user that it is already activated
        pass

    @license.sub_command(
        name="activate",
        description="Activates a license"
    )
    async def license_activate(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        license
    ):
        await interaction.response.defer(
            ephemeral=True
        )

        with open("json/licenses.json", "r") as licenses:
            licenses = json.load(licenses)

        with open("json/guild.json", "r") as guild:
            guild_info = json.load(guild)

        # check if license is in database
        if license in licenses:
            # check if the license is already activated/already used till limit
            if licenses[license]["useability"] > 0 or licenses[license]["useability"] == 1:
                # check if the license deactivated
                if licenses[license]["deactivated"]:
                    # update json file
                    licenses[license]["owner"] = interaction.author.id
                    licenses[license]["guild"] = interaction.guild.name
                    licenses[license]["activated"] = True
                    licenses[license]["deactivated"] = False
                    licenses[license]["start_time"] = get_time()
                    licenses[license]["end_time"] = set_time_calcs(license)
                    licenses[license]["useability"] -= 1

                    with open("json/licenses.json", "w") as dumpfile:
                        json.dump(licenses, dumpfile, indent=4, default=str)

                    guild_info[str(interaction.guild.id)]["license"] = license

                    with open("json/guild.json", "w") as dumpfile:
                        json.dump(guild_info, dumpfile, indent=4, default=str)

                    # create confirmation embed
                    embed = disnake.Embed(
                        title="License Activated ✅",
                        description=f"🔑 License Key: ||`{license}`||\n"
                                    f"📜 Uses left: `{licenses[license]['useability']}`\n"
                                    f"⌛ Activation Time: ||`{get_time()}`||\n"
                                    f"⌛ Expiration Time: ||`{set_time_calcs(license)}`||\n\n"
                                    f"👥 Guild: `{interaction.guild.name}`\n"
                                    f"👤 Owner: `{interaction.author.name}`",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
                else:
                    # print error in embed
                    embed = disnake.Embed(
                        description=f"License ||`{license}`|| is not deactived/already activated ⛔",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
            else:
                # print error in embed
                embed = disnake.Embed(
                    description=f"License ||`{license}`|| is not useable anymore ⛔",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
        else:
            # print error in embed
            embed = disnake.Embed(
                description=f"License ||`{license}`|| is not valid. Please check the license ⛔",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @license.sub_command(
        name="deactivate",
        description="Deactivates a license [NOTE - THIS WILL DEACTIVATE THE LICENSE AND CANNOT BE REACTIVATED]"
    )
    async def license_deactivate(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        license
    ):
        await interaction.response.defer(
            ephemeral=True
        )

        with open("json/licenses.json", "r") as licenses:
            licenses = json.load(licenses)

        # check if the author is the owner of the license
        if interaction.author.id == licenses[license]["owner"]:
            # check if the license is in the database
            if license in licenses:
                # check if the license is activated
                if licenses[license]["activated"]:
                    # update json file
                    licenses[license]["activated"] = False
                    licenses[license]["deactivated"] = True
                    licenses[license]["deactivated_time"] = get_time()

                    with open("json/licenses.json", "w") as dumpfile:
                        json.dump(licenses, dumpfile, indent=4)

                    # create confirmation embed
                    embed = disnake.Embed(
                        title="License Deactivated ✅",
                        description=f"License Key: ||`{license}`||",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
                else:
                    # print error in embed
                    embed = disnake.Embed(
                        description=f"License ||`{license}`|| is not active/already deacivated ⛔",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
            else:
                # print error in embed
                embed = disnake.Embed(
                    description=f"License ||`{license}`|| is not valid. Plaese check the license ⛔",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
        else:
            # print error in embed
            embed = disnake.Embed(
                description="You are not the owner of this license. You cannot deactivate it ⛔",
                color=disnake.Color.red()
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @license.sub_command(
        name="delete",
        description="Deletes a license"
    )
    @commands.has_permissions(administrator=True)
    async def license_delete(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        license
    ):
        # let the interaction be longer than three seconds
        await interaction.response.defer(
            ephemeral=True
        )

        with open("json/licenses.json", "r") as f:
            licenses = json.load(f)

        # check if license is in database
        if license in licenses:
            # delete license from json file
            del licenses[license]
            with open("json/licenses.json", "w") as dumpfile:
                json.dump(licenses, dumpfile, indent=4)

            # create confirmation embed
            embed = disnake.Embed(
                description=f"License ||`{license}`|| deleted ✅"
            )
            await interaction.edit_original_message(
                embed=embed
            )
        else:
            # print error in embed
            embed = disnake.Embed(
                description=f"License ||`{license}`|| not found. Please check the key ⛔"
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @loop(hours=6)
    async def license_check(self):
        # wait until bot is ready
        await self.bot.wait_until_ready()

        print(f"{colorama.Fore.LIGHTWHITE_EX} [LICENSE CHECK] [TASK] Checking licenses... {colorama.Fore.RESET}")

        with open("json/licenses.json", "r") as f:
            licenses = json.load(f)

        for license in licenses:
            # fetching the license's date
            if licenses[license]["end_time"] != "Lifetime":
                date_1_string = str(licenses[license]["end_time"])
                # convert it to an datetime object
                date1 = datetime.datetime.strptime(date_1_string, "%d.%m.%Y %H:%M:%S")

                # fetching the current time and date
                date_2_string = str(get_time())
                # convert it to an datetime object
                date2 = datetime.datetime.strptime(date_2_string, "%d.%m.%Y %H:%M:%S")

                print(f"{colorama.Fore.LIGHTGREEN_EX} [LICENSE CHECK] [CHECK] Checking license {license}... {colorama.Fore.RESET}")
                # check if the license is expired || if the local time is older than the license's end time
                if date1 < date2:
                    # change json
                    licenses[license]["activated"] = False
                    licenses[license]["deactivated"] = True
                    licenses[license]["expired"] = True
                    licenses[license]["deactivated_time"] = get_time()

                    with open("json/licenses.json", "w") as dumpfile:
                        json.dump(licenses, dumpfile, indent=4)

                    print(f"{colorama.Fore.RED} [LICENSE CHECK] [EXPIRED] License {license} expired. {colorama.Fore.RESET}")

                    user = self.bot.get_user(licenses[license]["owner"])
                    embed = disnake.Embed(
                        title="Your License Expired ⛔",
                        description=f"🔑 License Key: ||`{license}`||\n"
                                    f"⌛ Expired At: `{licenses[license]['end_time']}`\n\n"
                                    f"👥 Guild: `{licenses[license]['guild']}`\n"
                                    f"👤 Owner: `{licenses[license]['owner']}`",
                        color=disnake.Color.red()
                    )
                    embed.set_footer(text="Your license expired and was removed from the database!", icon_url=user.avatar.url)

                    # try to send embed to user
                    try:
                        await user.send(embed=embed)
                    except disnake.HTTPException:
                        print(f"{colorama.Fore.RED} [LICENSE CHECK] [ERROR] Could not send message to {user.name}#{user.discriminator}! {colorama.Fore.RESET}")

                else:
                    print(f"{colorama.Fore.GREEN} [LICENSE ] [SUCCESS] License {license} not expired. {colorama.Fore.RESET}")
            else:
                print(f"{colorama.Fore.GREEN} [LICENSE CHECK] [SUCCESS] License {license} skipping. {colorama.Fore.RESET}")

        print(f"{colorama.Fore.LIGHTMAGENTA_EX} [LICENSE CHECK] [DONE] Finished {colorama.Fore.RESET}")

    @loop(hours=12)
    async def license_check_expired(self):
        await self.bot.wait_until_ready()
        print(f"{colorama.Fore.LIGHTWHITE_EX} [LICENSE REMOVE] [TASK] Removing expired licenses...{colorama.Fore.RESET}")
        # use method created in the other file
        remove_expired_licenses()
        print(f"{colorama.Fore.LIGHTMAGENTA_EX} [LICENSE REMOVE] [DONE] Finished {colorama.Fore.RESET}")

    @license.sub_command(
        name="create",
        description="Creates a license"
    )
    @commands.has_permissions(administrator=True)
    async def license_create(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        duration: Times,
        useability: int
    ):
        # create a new license
        license_key = generate()
        # let the interaction be longer than three seconds
        await interaction.response.defer(
            ephemeral=True
        )

        with open("json/licenses.json", "r") as f:
            licenses = json.load(f)

        # create license in json file
        licenses[license_key] = {}
        licenses[license_key]["duration"] = duration
        licenses[license_key]["useability"] = useability
        licenses[license_key]["owner"] = None
        licenses[license_key]["start_time"] = None
        licenses[license_key]["end_time"] = None
        licenses[license_key]["expired"] = False
        licenses[license_key]["deactivated_time"] = None
        licenses[license_key]["activated"] = False
        licenses[license_key]["deactivated"] = True

        with open("json/licenses.json", "w") as dumpfile:
            json.dump(licenses, dumpfile, indent=4)

        # create confirmation embed
        license_embed = disnake.Embed(
            title="License Created ✅",
            color=disnake.Color.green()
        )
        # check if useability is bigger than 1
        if useability > 1:
            # create customized embed
            license_embed.add_field(
                name="License ✅",
                value=f"🔑License Key: ||`{license_key}`||\n👥Useability: `{useability}`\n⌛Duration: `{duration}`",
            )

            await interaction.edit_original_message(
                embed=license_embed
            )

        # check if useability is 1 or less
        elif useability < 1 or useability == 1:
            # create customized embed
            license_embed.add_field(
                name="License ✅",
                value=f"🔑License Key: ||`{license_key}`||\n👤Useability: `{useability}`\n⌛Duration: `{duration}`",
            )

            await interaction.edit_original_message(
                embed=license_embed
            )


def setup(bot):
    bot.add_cog(LicenseSystem(bot))
