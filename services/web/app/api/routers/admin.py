import datetime

from app import schemas
from app.core.config import get_settings
from app.core.security import load_user, loginManager, passwordManager
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login", response_model=schemas.AdminLoginAPIResponse)
def login(credentials: OAuth2PasswordRequestForm = Depends()) -> schemas.AdminLoginAPIResponse | None:
    admin = load_user(credentials.username)
    if not admin or not passwordManager.verify(credentials.password, admin.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": loginManager.create_access_token(
            data=dict(sub=admin.username),
            expires=datetime.timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
        "token_type": "bearer",
    }
