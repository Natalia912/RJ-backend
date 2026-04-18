from typing_extensions import Annotated
from fastapi import APIRouter, status, Depends
from app.schemas.common import CreateResponse
from app.core.db_setup import SessionDep
from app.db.composition import (
    create_composition as db_create_composition,
    delete_composition as db_delete_composition,
    get_compositions as db_get_compositions,
    update_composition as db_update_composition,
)
from app.db.auth import get_current_active_user
from app.models.user import User
from app.schemas.composition import CompositionNew, Composition as CompositionSchema, CompositionUpdate

router = APIRouter(prefix="/compositions", tags=["compositions"])

@router.get('/', response_model=list[CompositionSchema])
def get_compositions(session: SessionDep, current_user: Annotated[User, Depends(get_current_active_user)]):
    return db_get_compositions(session, current_user.id)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_composition(session: SessionDep, current_user: Annotated[User, Depends(get_current_active_user)], data: CompositionNew):
    db_create_composition(session, current_user.id, data)
    return CreateResponse(message="Composition created successfully!")

@router.put("/{composition_id}", status_code=status.HTTP_200_OK)
def update_composition(composition_id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_active_user)], data: CompositionUpdate):
    db_update_composition(session, composition_id, current_user.id, data)
    return CreateResponse(message="Composition updated successfully!")

@router.delete("/{composition_id}", status_code=status.HTTP_200_OK)
def delete_composition(composition_id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_active_user)]):
    db_delete_composition(session, composition_id, current_user.id)
    return CreateResponse(message="Composition deleted successfully!")
