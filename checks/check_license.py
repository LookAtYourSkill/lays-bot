import json
import disnake
from disnake.ext import commands


def license_check(interaction: disnake.ApplicationCommandInteraction):
    with open("json/general.json", "r") as general_info:
        general = json.load(general_info)
    with open("json/guild.json", "r") as guild_info:
        guilds = json.load(guild_info)
    with open("json/licenses.json", "r") as license_info:
        licenses = json.load(license_info)

    if general["license_check"]:
        if interaction.guild.id in guilds:
            if guilds[str(interaction.guild.id)]["license"] in licenses and guilds[str(interaction.guild.id)]["license"]:
                return True
            else:
                return False
        else:
            return False
    else:
        return True


def check_license():
    def predicate(interaction: disnake.ApplicationCommandInteraction) -> bool:
        with open("json/general.json", "r") as general_info:
            general = json.load(general_info)
        with open("json/guild.json", "r") as guild_info:
            guild_data = json.load(guild_info)
        with open("json/licenses.json", "r") as license_info:
            licenses = json.load(license_info)

        guild = interaction.guild.id
        if general["license_check"]:
            if guild_data[str(guild)]["license"]:
                if guild_data[str(guild)]["license"] in licenses:
                    return True
            else:
                return False
                # raise commands.CheckFailure("This server does not have a valid license.")
        else:
            return True

    return commands.check(predicate)
