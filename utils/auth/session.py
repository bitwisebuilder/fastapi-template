from typing import Optional

import jwt
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from conf.settings import Settings


def decode_token(token: str):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError as err:
        print(err)
        raise HTTPException(status_code=403, detail="Invalid Token")
    except jwt.InvalidTokenError as err:
        print(err)
        raise HTTPException(status_code=403, detail="Invalid token")


class TokenValidator(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[dict]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            return decode_token(credentials.credentials)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Authentication required"
            )
