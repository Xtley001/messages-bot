import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration for XAMPP
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),  # XAMPP MySQL runs on localhost
    "user": os.getenv("DB_USER", "root"),       # Default username for XAMPP MySQL
    "password": os.getenv("DB_PASSWORD", ""),   # No password
    "database": os.getenv("DB_NAME", "church_bot")
}

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


# Website URL
WEBSITE_URL = "enter website url"
SITEMAP_URL = f"{WEBSITE_URL}/wp-sitemap.xml"
