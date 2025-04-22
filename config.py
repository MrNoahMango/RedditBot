from dotenv import load_dotenv
import os

load_dotenv()  # Load .env into environment variables

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PRIVILEGED_USER_IDS = list(map(int, os.getenv("PRIVILEGED_USER_IDS").split(',')))
