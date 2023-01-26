import json

import colorama
import requests
from isodate import parse_duration

with open('etc/youtube-config.json', 'r', encoding='UTF-8') as config_file:
    config = json.load(config_file)

# ! WORKING
def convert_usernamne_to_id(username, api_key = config["apiKeyChannelId"]):
    # make request to youtube api with search parameters
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={username}&type=channel&key={api_key}"
    # get response from request
    response = requests.get(url)
    # convert response to json
    data = response.json()
    # start try block
    try:
        # check if request was successful
        if data["items"]:
            # get the user id from the response
            user_id = data['items'][0]['snippet']['channelId']
            # return the user id
            return user_id
        # if no user is found
        else:
            # return error message
            print(f"No channel found for username. maybe typo in username")
            return None
    except KeyError as e:
        print(f"{colorama.Fore.RED} [CONVERT ERROR] {e} {colorama.Fore.RESET}")

# ! WORKING
def get_channel_info(channel_id, api_key = config["apiKeyChannelInfo"]):
    # make request to youtube api for channel info
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={api_key}"
    # get response from request
    response = requests.get(url)
    # convert response to json
    data = response.json()
    # start exception check
    try:
        # check if request was successful
        if response.status_code == 200:
            # check if data is found
            if data["items"]:
                # return the data
                return data["items"]
            else:
                # returns error message if no data is found
                print("No data found. Channel may not exist or typo in username")
                return None
        else:
            # returns error message if request fails
            print(f"{colorama.Fore.RED} [CHANNEL INFO ERROR] {response.status_code} | Message: {response.json()} {colorama.Fore.RESET}")
    # catch exception if data is not found
    except KeyError as e:
        # print error message
        print(f"{colorama.Fore.RED} [CHANNEL INFO ERROR] {e} {colorama.Fore.RESET}")

# ! WORKING
def get_latest_videos(channel_id, api_key = config["apiKeyLastestVideo"]):
    # make request to youtube api with search parameters
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1"
    # get response from request
    response = requests.get(url)
    # convert response to json
    data = response.json()
    # start exception check
    try:
        # check if request was successful
        if response.status_code == 200:
            # check if data is found
            if data["items"]:
                # return the data
                return data["items"]
            else:
                print("No data found. Channel may not exist or typo in username")
                # returns error message if no data is found
                return None
        else:
            # returns error message if request fails
            print(f"{colorama.Fore.RED} [LAST VIDEOS ERROR] {response.status_code} | Message: {response.json()} {colorama.Fore.RESET}")
    # catch exception if data is not found
    except KeyError as e:
        # print error message
        print(f"{colorama.Fore.RED} [LAST VIDEOS ERROR] {e} {colorama.Fore.RESET}")


# ! WORKING 
def is_short(video_id: str, checkTime: int = 60, api_key = config["apiKeyChannelInfo"]):
    # make request to youtube api with search parameters
    url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={api_key}"
    # get response from request
    response = requests.get(url)
    # convert response to json
    data = response.json()
    # get the duration of the video
    video_duration = data['items'][0]['contentDetails']['duration']
    # convert duration to seconds
    duration = parse_duration(video_duration)
    # convert duration to seconds
    total_seconds = int(duration.total_seconds()) 
    # check if video duration is less than the checkTime parameter seconds
    if total_seconds <= int(checkTime):
        # * video is short
        # return true if video is less than checkTime parameter seconds
        return True
    else:
        # * video is no short
        # return false if video is more than checkTime parameter seconds
        return False

# ! seems working
def check_title(video_id: str, sentence: str = "Tjan Reaktion", api_key = config["apiKeyChannelInfo"]):
    # make request to youtube api with search parameters
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    # get response from request
    response = requests.get(url)
    # convert response to json
    data = response.json()
    # get the title of the video
    video_title: str = data['items'][0]['snippet']['title']
    # check if sentence is in the title of the video
    if sentence.lower() in video_title.lower():
        # sentence is in title
        # return true if sentence is in the title of the video
        return True
    else:
        # sentence is not in title
        # return false if sentence is not in the title of the video
        return False
