from typing_extensions import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from app.core.db_setup import SessionDep
from app.schemas.common import CreateResponse
from app.schemas.user import UserCreate, TokenData, UserResponse
from app.models.user import User,UserPublic
from app.core.auth import decode_access_token, get_password_hash, oauth2_scheme
from sqlmodel import select
from app.db.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(newUser: UserCreate, session: SessionDep) -> CreateResponse:
    if session.exec(select(User).where(User.email == newUser.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(newUser.password)
    userToUpdate = newUser.model_copy(update={"hashed_password": hashed_password})
    db_user = User.model_validate(userToUpdate)
    session.add(db_user)
    session.commit()
    return CreateResponse(message="User created successfully!")

@router.get("/", response_model=list[UserPublic])
def read_users(session: SessionDep, offset: int = 0, limit: int = 100):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users
