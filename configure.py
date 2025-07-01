import os
from dotenv import load_dotenv

load_dotenv()

class Store:
    # Add your keys and configuration settings here
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")
    TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH")
    TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID")
    MEMOCAST_BOT = os.environ.get("MEMOCAST_BOT")
    ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
