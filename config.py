import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    # API Keys (optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

    # Bot Settings
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "webp", "gif", "bmp"]
    DEFAULT_GENERATION_COUNT = 1

config = Config()
