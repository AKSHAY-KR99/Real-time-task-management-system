import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")


MAIL_USERNAME=os.getenv("MAIL_FROM", "secret")
MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "secret")
MAIL_FROM=os.getenv("MAIL_FROM", "secret")
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=587
MAIL_TLS=True
MAIL_SSL=False