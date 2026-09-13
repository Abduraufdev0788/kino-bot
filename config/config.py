import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
CHANNELS = [ch.strip() for ch in os.getenv("CHANNELS", "").split(",") if ch.strip()]
YOUTUBE_CHANNEL = os.getenv("YOUTUBE_CHANNEL")

ADMIN_ID = os.getenv("ADMIN_ID")
