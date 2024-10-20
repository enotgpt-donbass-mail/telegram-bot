import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TelegramToken')
DB_CONNECTION = os.getenv('DbConnection')
AUTH_TOKEN = os.getenv('AuthToken')