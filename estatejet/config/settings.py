import os
from pathlib import Path

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "DATABASE")
PYTEST_DATABASE_URL = os.getenv("PYTEST_DATABASE_URL", "sqlite://memory")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
CORS_ALLOWED_ORIGINS = "*"
ROOT = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'SUPER_SECRET_KEY_THAT_NONE_KNOWS')
REFRESH_KEY = os.getenv('REFRESH_KEY', 'SUPER_SECRET_KEY_THAT_NONE_KNOWS')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

INSTALLED_APPS = [
    'apps.users'
]

PasswordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2Scheme = OAuth2PasswordBearer(tokenUrl="token")
