from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from conf.db.dependencies import get_db
from iam.routes.v1 import schemas
from iam.users import crud
from utils.auth.user import valid_password

router = APIRouter()


@router.post("/auth/login/", response_model=schemas.UserLoginResponse)
def login(body: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_or_none(db, email=body.email)
    if user is None or not valid_password(user, body.password):
        raise HTTPException(status_code=401, detail="Provided credentials don't match")
    response = schemas.UserLoginResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    response.access_token = response.generate_access_token()
    response.refresh_token = response.generate_refresh_token()
    return response


@router.post("/auth/register/", response_model=schemas.User)
def register(body: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_or_none(db, email=body.email)
    if user is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = crud.create_user(db, user=body)
    return db_user
