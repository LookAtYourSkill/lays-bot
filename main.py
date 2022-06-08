import json
import os
import disnake
from disnake.ext import commands
import logging
import time

log = logging.getLogger(__name__)

bot = commands.Bot(
    intents=disnake.Intents.all(),
    command_prefix=commands.when_mentioned_or("%"),
    owner_id=493370963807830016,
    sync_commands=True
    # sync_commands_debug=True
)


@bot.event
async def on_ready():
    print(f"Bot successfully set up!\nLogged in as {bot.user.name}")

    global startTime
    startTime = time.time()

    log.info("Bot online")
    await bot.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.listening,
            name=f"{len(bot.guilds)} servers"),
        status=disnake.Status.idle
    )


log.info("Loading extensions")
for filename in os.listdir("./extensions"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"extensions.{filename[:-3]}")
            print(f"Loaded extension {filename}")
        except Exception as e:
            print(f"Failed to load extension {filename}, {e}")


log.info("Loaded events")
for filename in os.listdir("./events"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"events.{filename[:-3]}")
            print(f"Loaded event {filename}")
        except Exception as e:
            print(f"Failed to load event {filename}, {e}")

log.info("Finished")


with open("etc/config.json", "r") as config:
    config = json.load(config)

if __name__ == "__main__":
    bot.run(config["token"]["token"])
    bot.wait_until_ready
