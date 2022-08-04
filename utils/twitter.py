import requests
import json

with open('etc/config.json', 'r', encoding='UTF-8') as config_file:
    config = json.load(config_file)

bearer_token = config["twitter"]["bearer_token"]


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def create_url_user(username):
    usernames = f"usernames={username}"
    user_fields = "user.fields=description,created_at,public_metrics,verified,url,profile_image_url"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def connect_to_endpoint_user(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_user(username):
    url = create_url_user(username)
    json_response = connect_to_endpoint_user(url)
    return json_response["data"][0]
    # print(json.dumps(json_response, indent=4, sort_keys=True))
