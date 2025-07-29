from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession

from src.utils.db_utils import create_database_session, db_session_context
from src.dto import user_dto
from src.repository.user_repository import UserRepository

import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/users/", response_model=user_dto.UserDTO)
async def create_user(user: user_dto.UserCreateDTO, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await UserRepository().create(user)
    if not res:
        raise HTTPException(status_code=400, detail="User creation failed")
    return res

@router.get("/all-users/", response_model=list[user_dto.UserDTO])
async def get_all_users(db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await UserRepository().get_all()
    if not res:
        raise HTTPException(status_code=404, detail="No users found")
    return res

@router.get("/users/", response_model=user_dto.UserDTO)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    user = await UserRepository().get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=user_dto.UserDTO)
async def update_user(
    user_id: uuid.UUID, user: user_dto.UserUpdateDTO, db: AsyncSession = Depends(create_database_session)
):
    db_session_context.set(db)
    updated_user = await UserRepository().update(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user