import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",  # имя переменной обязательно в кавычках
        "postgresql+psycopg2://postgres:password@localhost:5432/football_betting?client_encoding=utf8"
    )
    FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY", "ef098c42956545159b5b8c7b2164ba81")
    FOOTBALL_COMPETITION = os.getenv("FOOTBALL_COMPETITION", "PL")
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", 8080))
    FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", 1))

settings = Settings()
