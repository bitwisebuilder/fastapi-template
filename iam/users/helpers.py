import datetime
from secrets import token_hex

import jwt

from conf.settings import Settings


def create_access_token(user, secret_key, algorithm):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = current_time + datetime.timedelta(
        days=Settings.REFRESH_TOKEN_EXPIRY_IN_DAYS
    )
    access_token_payload = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_superuser": user.is_superuser,
        "is_active": user.is_active,
        "exp": expiry_time,
        "iat": current_time,
        "jti": token_hex(16),
    }
    access_token = jwt.encode(access_token_payload, secret_key, algorithm=algorithm)
    return access_token


def create_refresh_token(user, secret_key, algorithm):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = current_time + datetime.timedelta(
        days=Settings.REFRESH_TOKEN_EXPIRY_IN_DAYS
    )
    refresh_token_payload = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_superuser": user.is_superuser,
        "is_active": user.is_active,
        "exp": expiry_time,
        "iat": current_time,
        "jti": token_hex(16),
    }
    refresh_token = jwt.encode(refresh_token_payload, secret_key, algorithm=algorithm)
    return refresh_token


def create_tokens(user):
    secret_key = Settings.SECRET_KEY
    algorithm = "HS256"
    access_token = create_access_token(user, secret_key, algorithm)
    refresh_token = create_refresh_token(user, secret_key, algorithm)
    return access_token, refresh_token
