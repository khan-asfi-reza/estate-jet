import os
from pathlib import Path

from passlib.context import CryptContext
from pydantic import BaseSettings
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL = os.getenv("DATABASE_URL", "DATABASE")
    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "DATABASE")
    PYTEST_DATABASE_URL = os.getenv("PYTEST_DATABASE_URL", "DATABASE")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
    CORS_ALLOWED_ORIGINS = "*"
    ROOT = Path(__file__).resolve().parent.parent.parent


Config = Settings()

PasswordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")