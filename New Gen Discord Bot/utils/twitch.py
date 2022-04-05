import json
import time
from datetime import datetime
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


def get_profile_image(login_names):
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
    return {entry["login"]: entry["profile_image_url"] for entry in response.json()["data"]}


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


online_users = []


def get_notifications():
    global online_users
    users = get_users(watchlist_data["overall_watchlist"])
    streams = get_streams(users)

    notifications = []
    for user_name in watchlist_data["overall_watchlist"]:
        if user_name in streams and user_name not in online_users:
            giga_time = datetime.strptime(streams[user_name]['started_at'], "%Y-%m-%dT%H:%M:%SZ")
            started_at = time.mktime(giga_time.timetuple()) + giga_time.microsecond / 1E6
            if time.time() - started_at < 4000:
                notifications.append(streams[user_name])
                online_users.append(user_name)

    return notifications
