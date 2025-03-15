# Initializes reddit API
import praw
from config.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT


reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)


def fetch_top_post(subreddit: str):
    subreddit = reddit.subreddit(subreddit)  # Fetch the subreddit
    top_post = next(subreddit.hot(limit=1))  # Fetch the top post
    return top_post.title, top_post.url  # Return the post title and URL
