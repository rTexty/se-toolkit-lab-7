import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env.bot.secret'))

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "placeholder_token")
    LMS_API_URL = os.getenv("LMS_API_URL", "http://localhost:42002")
    LMS_API_KEY = os.getenv("LMS_API_KEY", "placeholder_key")

config = Config()
