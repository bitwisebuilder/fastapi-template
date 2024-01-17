import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DEBUG: bool = os.getenv("DEBUG", False)
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    CORS_ORIGINS = os.getenv("ALLOW_ORIGINS").split(",")

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
