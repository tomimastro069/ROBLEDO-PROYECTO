from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DB_URL: str = os.getenv("DB_URL", "postgresql://user:pass@localhost:5432/foodstore")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
