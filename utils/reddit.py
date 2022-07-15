import praw
import random


reddit = praw.Reddit(
    client_id="e3WCWP0by7A_vptAGIULKA",
    client_secret="lqutAcUFkFkdsSHxICYkqKRjyubYPw",
    user_agent="pythonpraw",
    check_for_async=False
)


def get_memes():
    posts = []

    subreddits = ["funnymemes", "meme", "dankmemes", "historymemes", "Showerthoughts", "DadJokes"]
    subreddit = random.choice(subreddits)

    for post in reddit.subreddit(subreddit).hot(limit=100):
        if (post.url).endswith(('.jpg', '.png', '.jpeg')):
            posts.append(post.url)
            print(posts)
        else:
            posts.append(post.title + '\n' + post.selftext)
            print(posts)
        if len(posts) > 0:
            print(posts)
            return random.choice(posts)
        else:
            return "No memes found!"
