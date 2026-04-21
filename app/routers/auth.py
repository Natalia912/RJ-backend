

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import create_access_token
from datetime import timedelta
from app.core.config import JWT_CONFIG
from app.schemas.common import Token
from app.db.auth import authenticate_user, create_user as create_user_in_db
from app.core.db_setup import SessionDep
from app.schemas.user import UserLogin, UserCreate


router = APIRouter(prefix="/auth", tags=["auth"])
    
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: UserLogin,
    session: SessionDep
) -> Token:
    user = authenticate_user(session, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=JWT_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"])
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup_for_access_token(
    new_user: UserCreate,
    session: SessionDep
) -> Token:
    user = create_user_in_db(session, new_user)
    access_token_expires = timedelta(minutes=JWT_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"])
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)