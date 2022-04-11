import json
import os
from termcolor import colored
import disnake
from disnake.ext import commands


bot = commands.Bot(
    intents=disnake.Intents.all(),
    command_prefix=commands.when_mentioned_or(">"),
    owner_id=493370963807830016,
    sync_commands=True
)


@bot.event
async def on_ready():
    print(colored(
        f"Botid: {bot.user.id} - Name: {bot.user}",
        "green")
    )
    await bot.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.listening,
            name=f"{len(bot.guilds)} servers"),
        status=disnake.Status.idle
    )


print(colored("COGS", "yellow"))
for filename in os.listdir("./extensions"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"extensions.{filename[:-3]}")
            print(
                "Loaded " + colored(
                    f"{filename} ", "green"
                ) + "Successful"
            )
        except disnake.Forbidden:
            print(
                colored(
                    f"Error, something went wrong with {filename}!", "red"
                )
            )

print(colored("EVENT PART", "yellow"))
for filename in os.listdir("./events"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"events.{filename[:-3]}")
            print(
                "Loaded " + colored(
                    f"{filename} ", "green"
                ) + "Successful"
            )
        except Exception as e:
            print(
                colored(
                    f"Error, something went wrong with {filename}! {e}", "red"
                )
            )

print(
    colored(
        "Finished setting up files!", "green"
    )
)

with open("etc/config.json", "r") as config:
    config = json.load(config)

if __name__ == "__main__":
    bot.run(config["token"]["token"])
    bot.wait_until_ready
