import json
import requests
import colorama
from datetime import datetime


with open("json/watchlist.json", 'r', encoding='UTF-8') as data_file:
    watchlist_data = json.load(data_file)

with open('etc/config.json', 'r', encoding='UTF-8') as config_file:
    config = json.load(config_file)


def get_users(login_names):
    params = {
        "login": login_names
    }

    headers = {
        "Authorization": f'Bearer {config["twitch"]["access_token"]}',
        "Client-Id": config["twitch"]["client_id"]
    }

    response = requests.get(
        "https://api.twitch.tv/helix/users",
        params=params,
        headers=headers
    )
    if response.status_code == 200:
        return {entry["login"]: entry["id"] for entry in response.json()["data"]}
    else:
        print(f"{colorama.Fore.RED} [ERROR] Failed to get users from Twitch API, possible new access token needed {colorama.Fore.RESET}")


def get_all_user_info(login_name):
    params = {
        "login": login_name
    }

    headers = {
        "Authorization": f'Bearer {config["twitch"]["access_token"]}',
        "Client-Id": config["twitch"]["client_id"]
    }

    response = requests.get(
        "https://api.twitch.tv/helix/users",
        params=params,
        headers=headers
    )
    if response.status_code == 200:
        return [entry for entry in response.json()["data"]]
    else:
        print(f"{colorama.Fore.RED} [ERROR] Failed to get users from Twitch API, possible new access token needed {colorama.Fore.RESET}")


def get_followers(user_id):
    params = {
        "to_id": user_id
    }

    headers = {
        "Authorization": f'Bearer {config["twitch"]["access_token"]}',
        "Client-Id": config["twitch"]["client_id"]
    }
    response = requests.get(
        "https://api.twitch.tv/helix/users/follows",
        params=params,
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{colorama.Fore.RED} [ERROR] Failed to get followers from Twitch API, possible new access token needed {colorama.Fore.RESET}")


def get_streams(users: dict):
    params = {
        "user_id": users.values()
    }

    headers = {
        "Authorization": f'Bearer {config["twitch"]["access_token"]}',
        "Client-Id": config["twitch"]["client_id"]
    }
    response = requests.get(
        "https://api.twitch.tv/helix/streams",
        params=params,
        headers=headers
    )
    if response.status_code == 200:
        return {entry["user_login"]: entry for entry in response.json()["data"]}
    else:
        print(f"{colorama.Fore.RED} [ERROR] Failed to get streams from Twitch API, possible new access token needed {colorama.Fore.RESET}")


def update_streams():
    with open("json/watchlist.json", 'r', encoding='UTF-8') as data_file:
        watchlist_data: dict = json.load(data_file)

    with open('json/twitch_updates.json', 'r', encoding='UTF-8') as update_file:
        twitch_updates: dict = json.load(update_file)

    # load and loop through data in file
    with open("json/guild.json", "r", encoding="UTF-8") as file:
        for guild in json.load(file).values():

            # get all streamers from watchlist
            users = get_users(watchlist_data["overall_watchlist"])
            stream = get_streams(users)

            # loop through all streamers
            for streamer in watchlist_data["overall_watchlist"]:
                # check if streamer is live and in watchlist from guild
                if streamer in stream and streamer in guild["watchlist"]:

                    # get started at info
                    twitchTime = stream[streamer]["started_at"]
                    # format to timestamp
                    finalTime = datetime.strptime(twitchTime, "%Y-%m-%dT%H:%M:%SZ").timestamp()

                    # ! print(finalTime)

                    # if streamer not in update file, add him
                    if streamer not in twitch_updates:
                        twitch_updates[streamer] = {}
                        twitch_updates[streamer][guild['server_id']] = {
                            "title": stream[streamer]["title"],
                            "channel_id": guild["notify_channel"],
                            "game_id": stream[streamer]["game_id"],
                            "game_name": stream[streamer]["game_name"],
                            "game_list": [],
                            "viewer_count": stream[streamer]["viewer_count"],
                            "started_at": finalTime,
                            "ended_at": None,
                            "last_update": datetime.now().timestamp(),
                            "thumbnail_url": stream[streamer]["thumbnail_url"],
                            "user_id": stream[streamer]["user_id"],
                            "user_name": stream[streamer]["user_name"],
                            "status": "live",
                            "message_id": None
                        }

                        # !! print(f"{colorama.Fore.GREEN} [INFO] {i} is not in data! - {guild['server_name']} {colorama.Fore.RESET}")

                        with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                            json.dump(twitch_updates, file, indent=4)
                    else:
                        # check if guild is in update file
                        # if not add guild to streamer
                        if guild['server_id'] not in twitch_updates[streamer]:
                            twitch_updates[streamer][guild['server_id']] = {
                                "title": stream[streamer]["title"],
                                "channel_id": guild["notify_channel"],
                                "game_id": stream[streamer]["game_id"],
                                "game_name": stream[streamer]["game_name"],
                                "game_list": [],
                                "viewer_count": stream[streamer]["viewer_count"],
                                "started_at": finalTime,
                                "ended_at": None,
                                "last_update": datetime.now().timestamp(),
                                "thumbnail_url": stream[streamer]["thumbnail_url"],
                                "user_id": stream[streamer]["user_id"],
                                "user_name": stream[streamer]["user_name"],
                                "status": "live",
                                "message_id": None
                            }

                            with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                json.dump(twitch_updates, file, indent=4)
                        else:
                            # check if guild is in update file
                            # if yes, update data for streamer
                            # !! print(f"{colorama.Fore.GREEN} [INFO] {i} is in data but update! - {guild['server_name']} {colorama.Fore.RESET}")
                            twitch_updates[streamer][guild['server_id']]['title'] = stream[streamer]["title"]
                            twitch_updates[streamer][guild['server_id']]['game_id'] = stream[streamer]["game_id"]
                            twitch_updates[streamer][guild['server_id']]['game_name'] = stream[streamer]["game_name"]
                            twitch_updates[streamer][guild['server_id']]['viewer_count'] = stream[streamer]["viewer_count"]
                            twitch_updates[streamer][guild['server_id']]['started_at'] = finalTime
                            twitch_updates[streamer][guild['server_id']]['thumbnail_url'] = stream[streamer]["thumbnail_url"]
                            twitch_updates[streamer][guild['server_id']]['user_id'] = stream[streamer]["user_id"]
                            twitch_updates[streamer][guild['server_id']]['user_name'] = stream[streamer]["user_name"]
                            twitch_updates[streamer][guild['server_id']]['status'] = "live"

                            with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                json.dump(twitch_updates, file, indent=4)

                            if stream[streamer]["game_name"] not in twitch_updates[streamer][guild['server_id']]["game_list"]:
                                list_of_games: list = twitch_updates[streamer][guild['server_id']]["game_list"]
                                list_of_games.append(stream[streamer]["game_name"])

                                with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                    json.dump(twitch_updates, file, indent=4)
                            else:
                                continue

                else:
                    # !! print(f"{colorama.Fore.RED} [INFO] {i} is not live! - {guild['server_name']} {colorama.Fore.RESET}")
                    # check if streamer is in update file
                    if streamer in twitch_updates:
                        # check if guild id is in update file
                        if guild['server_id'] in twitch_updates[streamer]:
                            # change status to offline
                            twitch_updates[streamer][guild['server_id']]['status'] = "offline"
                            twitch_updates[streamer][guild['server_id']]['ended_at'] = datetime.now().timestamp()

                            with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                json.dump(twitch_updates, file, indent=4)
                        else:
                            continue
                    else:
                        continue
