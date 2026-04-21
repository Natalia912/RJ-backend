from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from typing_extensions import Annotated

from sqlmodel import select
from app.core.db_setup import SessionDep
from app.models.user import User
from app.core.auth import verify_password, decode_access_token, oauth2_scheme, get_password_hash
from app.schemas.user import TokenData, UserCreate


def create_user(session: SessionDep, new_user: UserCreate) -> User:
    if session.exec(select(User).where(User.email == new_user.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(new_user.password)
    user_to_update = new_user.model_copy(update={"hashed_password": hashed_password})
    db_user = User.model_validate(user_to_update)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def authenticate_user(session: SessionDep, email: str, password: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

    
async def get_current_active_user(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token.credentials)
    print(payload)
    if payload is None:
        raise credentials_exception
    email = payload.get("sub")
    print(email)
    if email is None:
        raise credentials_exception
    token_data = TokenData(email=email)

    statement = select(User).where(User.email == token_data.email)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user