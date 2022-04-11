import json
import requests

with open("etc/config.json", "r", encoding="UTF-8") as config_file:
    config = json.load(config_file)


def get_app_access_token():
    params = {
        "client_id": config["twitch"]["client_id"],
        "client_secret": config["twitch"]["client_secret"],
        "grant_type": "client_credentials"
    }

    response = requests.post("https://id.twitch.tv/oauth2/token", params=params)
    access_token = response.json()["access_token"]
    return access_token


access_token = get_app_access_token()
print(access_token)
