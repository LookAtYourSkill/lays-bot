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
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Maybe need new client secret? {response.status_code} see the full response: {response.json()}")


access_token = get_app_access_token()
print(access_token)
