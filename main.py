import json
import logging
import os
import asyncio

import disnake
from disnake.ext import commands

log = logging.getLogger(__name__)

bot = commands.Bot(
    intents=disnake.Intents.all(),
    command_prefix=commands.when_mentioned_or("%"),
    owner_id=493370963807830016,
    sync_commands=True
)


async def status_task():
    while True:
        await bot.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.listening,
                name=f"{len(bot.guilds)} servers"),
            status=disnake.Status.online
        )
        await asyncio.sleep(1800)
        await bot.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.listening,
                name=f"{len(bot.guilds)} servers"),
            status=disnake.Status.online
        )
        await asyncio.sleep(1800)


@bot.event
async def on_ready():
    print(f"Bot successfully set up!\nLogged in as {bot.user.name}\nCurrently in {len(bot.guilds)} servers")
    bot.loop.create_task(status_task())


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
        if filename.startswith("_"):
            continue
        try:
            bot.load_extension(f"events.{filename[:-3]}")
            print(f"Loaded event {filename}")
        except Exception as e:
            print(f"Failed to load event {filename}, {e}")
    else:
        continue


log.info("Loaded checks")
for filename in os.listdir("./checks"):
    if filename.endswith(".py"):
        if filename.startswith("_"):
            continue
        try:
            bot.load_extension(f"checks.{filename[:-3]}")
            print(f"Loaded check {filename}")
        except Exception as e:
            print(f"Failed to load check {filename}, {e}")
    else:
        continue

print("----------------------------------------------------")
log.info("Finished")



with open("etc/config.json", "r") as config_file:
    config = json.load(config_file)

if __name__ == "__main__":
    bot.run(config["token"]["lays_bot_2_0_token"])
    bot.wait_until_ready
