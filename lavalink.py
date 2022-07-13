import json
import subprocess

import colorama


with open("etc/config.json", "r") as config_file:
    config = json.load(config_file)

print(f"{colorama.Fore.LIGHTYELLOW_EX} [SETUP] Starting Lavalink... {colorama.Fore.RESET}")
subprocess.call(['java', '-jar', config['lavalink']['path']])
