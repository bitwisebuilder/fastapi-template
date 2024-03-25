from datetime import datetime

from pydantic import BaseModel

from conf.settings import Settings
from iam.users.helpers import create_access_token
from iam.users.helpers import create_refresh_token


class LoginRequest(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserUpdate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class User(UserBase):
    id: int
    first_name: str
    last_name: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class UserLoginResponse(User):
    access_token: str | None = None
    refresh_token: str | None = None

    def generate_access_token(self):
        return create_access_token(self, Settings.SECRET_KEY, "HS256")

    def generate_refresh_token(self):
        return create_refresh_token(self, Settings.SECRET_KEY, "HS256")
