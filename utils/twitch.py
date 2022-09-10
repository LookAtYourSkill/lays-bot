import json
import requests
import colorama


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


def get_streams(users):
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

    with open("json/guild.json", "r", encoding="UTF-8") as file:
        for guild in json.load(file).values():

            stream = get_streams(get_users(watchlist_data["overall_watchlist"]))

            for i in watchlist_data["overall_watchlist"]:
                if i in stream and i in guild["watchlist"]:
                    if i not in twitch_updates:
                        print(f"{colorama.Fore.GREEN} [INFO] {i} is not in data! - {guild['server_name']} {colorama.Fore.RESET}")
                        twitch_updates[i] = {}
                        twitch_updates[i][guild['server_id']] = {
                            "title": stream[i]["title"],
                            "game_id": stream[i]["game_id"],
                            "viewer_count": stream[i]["viewer_count"],
                            "started_at": stream[i]["started_at"],
                            "thumbnail_url": stream[i]["thumbnail_url"],
                            "user_id": stream[i]["user_id"],
                            "user_name": stream[i]["user_name"],
                            "status": "live",
                            "message_id": None
                        }

                        with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                            json.dump(twitch_updates, file, indent=4)
                    else:
                        print(f"{colorama.Fore.GREEN} [INFO] {i} is in data but update! - {guild['server_name']} {colorama.Fore.RESET}")
                        twitch_updates[i][guild['server_id']] = {
                            "title": stream[i]["title"],
                            "game_id": stream[i]["game_id"],
                            "viewer_count": stream[i]["viewer_count"],
                            "started_at": stream[i]["started_at"],
                            "thumbnail_url": stream[i]["thumbnail_url"],
                            "user_id": stream[i]["user_id"],
                            "user_name": stream[i]["user_name"],
                            "status": "live",
                            "message_id": None
                        }

                        with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                            json.dump(twitch_updates, file, indent=4)

                else:
                    print(f"{colorama.Fore.RED} [INFO] {i} is not live! - {guild['server_name']} {colorama.Fore.RESET}")
                    if i in twitch_updates:
                        if guild['server_id'] in twitch_updates[i]:
                            twitch_updates[i][guild['server_id']]['status'] = "offline"
                            twitch_updates[i][guild['server_id']]['message_id'] = None
                            with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                json.dump(twitch_updates, file, indent=4)
                        else:
                            continue
                    else:
                        continue
