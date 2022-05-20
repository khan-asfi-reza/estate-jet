import os
from pathlib import Path

from pydantic import BaseSettings
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL = os.getenv("DATABASE_URL", "DATABASE")
    CORS_ALLOWED_ORIGINS = "*"
    ROOT = Path(__file__).resolve().parent.parent.parent


Config = Settings()