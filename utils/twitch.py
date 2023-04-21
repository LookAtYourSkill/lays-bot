import json
import requests
import colorama
import datetime


with open("json/watchlist.json", 'r', encoding='UTF-8') as data_file:
    watchlist_data = json.load(data_file)

with open('etc/config.json', 'r', encoding='UTF-8') as config_file:
    config = json.load(config_file)

def get_app_access_token():
    params = {
        "client_id": config["twitch"]["client_id"],
        "client_secret": config["twitch"]["client_secret"],
        "grant_type": "client_credentials"
    }

    response = requests.post("https://id.twitch.tv/oauth2/token", params=params)
    if response.status_code == 200:
        config["twitch"]["access_token"] = response.json()["access_token"]

        with open('etc/config.json', 'w', encoding='UTF-8') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        print(f"Maybe need new client secret? {response.status_code} see the full response: {response.json()}")

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
        print(f"{colorama.Fore.RED} [ERROR] Failed to get users from Twitch API {colorama.Fore.RESET}")
        print(f"{colorama.Fore.RED} [ERROR] {response.status_code} {response.json()} {colorama.Fore.RESET}")
        print(f"{colorama.Fore.RED} [ERROR] Trying to get new access token... {colorama.Fore.RESET}")

        get_app_access_token()
        print(f"{colorama.Fore.GREEN} [SUCCESS] Granted new Access Token {colorama.Fore.RESET}")
        print(f"{colorama.Fore.BLUE} [PENDING] Trying to get users again... {colorama.Fore.RESET}")

        return get_users(login_names)


def get_all_category_info(category_id):
    # make request to twitch api
    params = {
        "id": category_id
    }

    headers = {
        "Authorization": f'Bearer {config["twitch"]["access_token"]}',
        "Client-Id": config["twitch"]["client_id"]
    }

    response = requests.get(
        "https://api.twitch.tv/helix/games",
        params=params,
        headers=headers
    )
    if response.status_code == 200:
        return [entry for entry in response.json()["data"]]
    else:
        print(f"{colorama.Fore.RED} [ERROR] Failed to get users from Twitch API {colorama.Fore.RESET}")
        return False


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


def averageCalculation(list):
    # check if the list which will be calculated is empty
    if len(list) == 0:
        # if empty return 0
        return 0
    else:
        # if not empty return the average of the list
        # with getting the sum of the list and dividing it by the length of the list
        const = sum(list) / len(list)
        return round(const)


def update_streams():
    with open("json/watchlist.json", 'r', encoding='UTF-8') as data_file:
        watchlist_data: dict = json.load(data_file)

    with open('json/twitch_updates.json', 'r', encoding='UTF-8') as update_file:
        twitch_updates: dict = json.load(update_file)

    # load and loop through data in file
    with open("json/guild.json", "r", encoding="UTF-8") as file:
        for guild in json.load(file).values():
            
            try:

                # get all streamers from watchlist
                users = get_users(watchlist_data["overall_watchlist"])
                stream = get_streams(users)

                # loop through all streamers
                for streamer in watchlist_data["overall_watchlist"]:
                    if guild["watchlist"] and stream:
                        # check if streamer is live and in watchlist from guild
                        if streamer in stream and streamer in guild["watchlist"]:

                            # get started at info
                            twitchTime = stream[streamer]["started_at"]
                            # format to timestamp
                            prefinalTime = datetime.datetime.strptime(twitchTime, "%Y-%m-%dT%H:%M:%SZ")
                            # remove timezone information so it can be converted to timestamp and there is no timezone error
                            finalTime = (prefinalTime.replace(tzinfo=None) + datetime.timedelta(hours=2)).timestamp()

                            # ! print(finalTime)

                            # if streamer not in update file, add him
                            if streamer not in twitch_updates:
                                all_infos = get_all_user_info(streamer)

                                twitch_updates[streamer] = {}
                                twitch_updates[streamer][guild['server_id']] = {
                                    "title": stream[streamer]["title"],
                                    "channel_id": guild["notify_channel"],
                                    "game_id": stream[streamer]["game_id"],
                                    "game_name": stream[streamer]["game_name"],
                                    "game_list": [],
                                    "viewer_count": stream[streamer]["viewer_count"],
                                    "viewer_count_list": [],
                                    "started_at": finalTime,
                                    "ended_at": None,
                                    "last_update": datetime.datetime.now(tz=None).timestamp(),
                                    "thumbnail_url": stream[streamer]["thumbnail_url"],
                                    "offline_url": all_infos[0]["offline_image_url"],
                                    "profile_pic": all_infos[0]["profile_image_url"],
                                    "user_id": stream[streamer]["user_id"],
                                    "user_name": stream[streamer]["user_name"],
                                    "sended": False,
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
                                    all_infos = get_all_user_info(streamer)

                                    twitch_updates[streamer][guild['server_id']] = {
                                        "title": stream[streamer]["title"],
                                        "channel_id": guild["notify_channel"],
                                        "game_id": stream[streamer]["game_id"],
                                        "game_name": stream[streamer]["game_name"],
                                        "game_list": [],
                                        "viewer_count": stream[streamer]["viewer_count"],
                                        "viewer_count_list": [],
                                        "started_at": finalTime,
                                        "ended_at": None,
                                        "last_update": datetime.datetime.now(tz=None).timestamp(),
                                        "thumbnail_url": stream[streamer]["thumbnail_url"],
                                        "offline_url": all_infos[0]["offline_image_url"],
                                        "profile_pic": all_infos[0]["profile_image_url"],
                                        "user_id": stream[streamer]["user_id"],
                                        "user_name": stream[streamer]["user_name"],
                                        "sended": False,
                                        "status": "live",
                                        "message_id": None
                                    }

                                    with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                        json.dump(twitch_updates, file, indent=4)
                                else:
                                    # check if guild is in update file
                                    # if yes, update data for streamer
                                    if guild["server_id"] in twitch_updates[streamer]:
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

                                        # define as a list
                                        # append all viewer counts to a list, which will be used to calculate the average viewer count
                                        list_of_viewer: list = twitch_updates[streamer][guild['server_id']]["viewer_count_list"]
                                        list_of_viewer.append(twitch_updates[streamer][guild['server_id']]["viewer_count"])

                                        # dump to json
                                        with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                            json.dump(twitch_updates, file, indent=4)

                                        # check if game is in update file from streamer
                                        if stream[streamer]["game_name"] not in twitch_updates[streamer][guild['server_id']]["game_list"]:
                                            # define as a list
                                            # append the game to the list if it is not in the list
                                            list_of_games: list = twitch_updates[streamer][guild['server_id']]["game_list"]
                                            list_of_games.append(stream[streamer]["game_name"])
                                            
                                            # dump to json
                                            with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                                json.dump(twitch_updates, file, indent=4)
                                        else:
                                            continue
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
                                    twitch_updates[streamer][guild['server_id']]['ended_at'] = datetime.datetime.now(tz=None).timestamp()

                                    with open("json/twitch_updates.json", "w", encoding="UTF-8") as file:
                                        json.dump(twitch_updates, file, indent=4)
                                else:
                                    continue
                            else:
                                continue
                    else:
                        continue

            except Exception as e:
                print(f"{colorama.Fore.RED} [ERROR] {e} {colorama.Fore.RESET}")
