import datetime

from sqlalchemy.orm import Session

from iam.users import models
from utils.auth.user import hash_password


def get_user_from_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_from_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_or_none(db: Session, user_id: int = None, email: str = None):
    if user_id:
        user = db.query(models.User).filter(models.User.id == user_id).first()
    else:
        user = db.query(models.User).filter(models.User.email == email).first()
    return user


def create_user(db: Session, user: models.User):
    hashed_password = hash_password(user.password)
    user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
