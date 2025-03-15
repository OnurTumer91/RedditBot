import os
from dotenv import load_dotenv

# Load env variables to avoid sharing API keys in the code
load_dotenv(override=True)  # Override in case a new token was to be generated

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
print("DISCORD_TOKEN loaded:", DISCORD_TOKEN)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
