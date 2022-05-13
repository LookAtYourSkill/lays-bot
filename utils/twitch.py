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
