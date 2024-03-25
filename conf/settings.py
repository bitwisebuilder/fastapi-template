import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Settings:
    DEBUG: bool = os.getenv("DEBUG", False)
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    CORS_ORIGINS = os.getenv("ALLOW_ORIGINS").split(",")

    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_DB = os.getenv("MYSQL_DB")
    MYSQL_PORT = os.getenv("MYSQL_PORT")

    RABBITMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")
    RABBITMQ_HOST = os.getenv("RABBITMQ_DEFAULT_HOST")
    RABBITMQ_PORT = os.getenv("RABBITMQ_DEFAULT_PORT")
    RABBITMQ_VHOST = os.getenv("RABBITMQ_DEFAULT_VHOST")

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = os.getenv("REDIS_DB")

    SECRET_KEY = os.getenv("SECRET_KEY")

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    ACCESS_TOKEN_EXPIRY_IN_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRY_IN_MINUTES", 60)
    REFRESH_TOKEN_EXPIRY_IN_DAYS = os.getenv("REFRESH_TOKEN_EXPIRY_IN_DAYS", 7)
