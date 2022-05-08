import json
import requests


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
    return {entry["login"]: entry["id"] for entry in response.json()["data"]}


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
    return {entry["user_login"]: entry for entry in response.json()["data"]}
