import json
from enum import Enum

import disnake
import colorama
from disnake.ext import commands
from disnake.ext.tasks import loop
from utils.license import generate, get_time, set_time_calcs


class Times(str, Enum):
    day = "1 Day"
    seven_days = "7 Days"
    one_month = "1 Month"
    three_months = "3 Months"
    six_months = "6 Months"
    year = "1 Year"
    lifetime = "Lifetime"


class LicenseSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.license_check.start()

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

        if license in licenses:
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

        if license in licenses:
            if licenses[license]["useability"] > 0:
                if licenses[license]["deactivated"]:
                    licenses[license]["owner"] = interaction.author.id
                    licenses[license]["guild"] = interaction.guild.name
                    licenses[license]["activated"] = True
                    licenses[license]["deactivated"] = False
                    licenses[license]["start_time"] = get_time()
                    licenses[license]["end_time"] = set_time_calcs(license)
                    licenses[license]["useability"] -= 1

                    with open("json/licenses.json", "w") as dumpfile:
                        json.dump(licenses, dumpfile, indent=4, default=str)

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
                    embed = disnake.Embed(
                        description=f"License ||`{license}`|| is not deactived/already activated ⛔",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
            else:
                embed = disnake.Embed(
                    description=f"License ||`{license}`|| is not useable anymore ⛔",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
        else:
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

        if interaction.author.id == licenses[license]["owner"]:
            if license in licenses:
                if licenses[license]["activated"]:
                    licenses[license]["activated"] = False
                    licenses[license]["deactivated"] = True
                    licenses[license]["deactivated_time"] = get_time()

                    with open("json/licenses.json", "w") as dumpfile:
                        json.dump(licenses, dumpfile, indent=4)

                    embed = disnake.Embed(
                        title="License Deactivated ✅",
                        description=f"License Key: ||`{license}`||",
                        color=disnake.Color.green()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
                else:
                    embed = disnake.Embed(
                        description=f"License ||`{license}`|| is not active/already deacivated ⛔",
                        color=disnake.Color.red()
                    )
                    await interaction.edit_original_message(
                        embed=embed
                    )
            else:
                embed = disnake.Embed(
                    description=f"License ||`{license}`|| is not valid. Plaese check the license ⛔",
                    color=disnake.Color.red()
                )
                await interaction.edit_original_message(
                    embed=embed
                )
        else:
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
        await interaction.response.defer(
            ephemeral=True
        )

        with open("json/licenses.json", "r") as f:
            licenses = json.load(f)

        if license in licenses:
            del licenses[license]
            with open("json/licenses.json", "w") as dumpfile:
                json.dump(licenses, dumpfile, indent=4)

            embed = disnake.Embed(
                description=f"License ||`{license}`|| deleted ✅"
            )
            await interaction.edit_original_message(
                embed=embed
            )
        else:
            embed = disnake.Embed(
                description=f"License ||`{license}`|| not found. Please check the key ⛔"
            )
            await interaction.edit_original_message(
                embed=embed
            )

    @loop(hours=6)
    async def license_check(self):
        await self.bot.wait_until_ready()

        print(f"{colorama.Fore.YELLOW} [TASK] Checking licenses...{colorama.Fore.RESET}")

        with open("json/licenses.json", "r") as f:
            licenses = json.load(f)

        for license in licenses.keys():
            print(f"{colorama.Fore.BLUE} [CHECK] Checking license {license}...{colorama.Fore.RESET}")
            if licenses[license]["end_time"] < get_time():
                licenses[license]["activated"] = False
                licenses[license]["deactivated"] = True
                licenses[license]["expired"] = True
                licenses[license]["deactivated_time"] = get_time()

                with open("json/licenses.json", "w") as dumpfile:
                    json.dump(licenses, dumpfile, indent=4)

                print(f"{colorama.Fore.GREEN} [SUCCESS] License {license} expired.{colorama.Fore.RESET}")

                user = self.bot.get_user(licenses[license]["owner"])
                embed = disnake.Embed(
                    title="Your License Expired ⛔",
                    description=f"🔑 License Key: ||`{license}`||\n"
                                f"⌛ Expiration Time: `{set_time_calcs(license)}`\n\n"
                                f"👥 Guild: `{licenses[license]['guild']}`\n"
                                f"👤 Owner: `{licenses[license]['owner']}`",
                    color=disnake.Color.red()
                )
                await user.send(embed=embed)

                del licenses[license]
                with open("json/licenses.json", "w") as dumpfile:
                    json.dump(licenses, dumpfile, indent=4)

            else:
                print(f"{colorama.Fore.GREEN} [SUCCESS] License {license} not expired.{colorama.Fore.RESET}")

        print(f"{colorama.Fore.GREEN} [SUCCESS] !!!!!!! Checking licenses DONE !!!!!!!{colorama.Fore.RESET}")

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
        license_key = generate()
        await interaction.response.defer(
            ephemeral=True
        )

        with open("json/licenses.json", "r") as f:
            licenses = json.load(f)

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

        license_embed = disnake.Embed(
            title="License Created ✅",
            color=disnake.Color.green()
        )
        if useability > 1:
            license_embed.add_field(
                name="License ✅",
                value=f"🔑License Key: ||`{license_key}`||\n👥Useability: `{useability}`\n⌛Duration: `{duration}`",
            )

            await interaction.edit_original_message(
                embed=license_embed
            )

        elif useability < 1 or useability == 1:
            license_embed.add_field(
                name="License ✅",
                value=f"🔑License Key: ||`{license_key}`||\n👤Useability: `{useability}`\n⌛Duration: `{duration}`",
            )

            await interaction.edit_original_message(
                embed=license_embed
            )


def setup(bot):
    bot.add_cog(LicenseSystem(bot))
