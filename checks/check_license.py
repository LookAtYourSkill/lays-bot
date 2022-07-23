import json
import disnake


def check_license_lol(interaction: disnake.ApplicationCommandInteraction):
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
