from typing_extensions import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from app.core.db_setup import SessionDep
from app.schemas.common import CreateResponse
from app.schemas.user import UserCreate
from app.models.user import User, UserPublic
from sqlmodel import select
from app.db.auth import get_current_active_user, create_user as create_user_in_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(newUser: UserCreate, session: SessionDep) -> CreateResponse:
    create_user_in_db(session, newUser)
    return CreateResponse(message="User created successfully!")

@router.get("/", response_model=list[UserPublic])
def read_users(session: SessionDep, offset: int = 0, limit: int = 100):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users
