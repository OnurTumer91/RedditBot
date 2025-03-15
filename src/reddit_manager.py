import praw
from config.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)


def fetch_top_post(subreddit: str, sort: str = "hot"):
    sub = reddit.subreddit(subreddit)

    # Choose the sorting method
    if sort.lower() == "top":
        post = next(sub.top(limit=1))
    elif sort.lower() == "new":
        post = next(sub.new(limit=1))
    elif sort.lower() == "rising":
        post = next(sub.rising(limit=1))
    elif sort.lower() == "random":
        post = sub.random()
        if post is None:
            post = next(sub.hot(limit=1))
    else:  # default to hot
        post = next(sub.hot(limit=1))

    # Retrieve basic post info
    title = post.title
    url = post.url
    score = post.score  # Upvote count

    # Fetch image preview if available
    image_url = None
    if hasattr(post, "preview"):
        try:
            image_url = post.preview["images"][0]["source"]["url"]
        except Exception:
            image_url = None

    # Get the post text (selftext) if available and limit its length
    selftext = post.selftext if hasattr(post, "selftext") else ""
    if selftext and len(selftext) > 500:
        selftext = selftext[:500] + "..."

    # Check if the post is a video and get the fallback video URL
    is_video = post.is_video
    video_url = None
    if is_video and post.media and "reddit_video" in post.media:
        video_url = post.media["reddit_video"]["fallback_url"]

    # Get the top comment
    top_comment = ""
    try:
        post.comments.replace_more(limit=0)
        if post.comments:
            best_comment = post.comments[0]
            top_comment = best_comment.body
            if len(top_comment) > 300:
                top_comment = top_comment[:300] + "..."
    except Exception:
        top_comment = "No top comment available."

    return {
        "title": title,
        "url": url,
        "score": score,
        "image_url": image_url,
        "is_video": is_video,
        "video_url": video_url,
        "selftext": selftext,
        "top_comment": top_comment,
    }
