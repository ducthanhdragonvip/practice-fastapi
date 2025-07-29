from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession

from src.utils.db_utils import create_database_session, db_session_context
from src.dto import user_dto
from src.repository.user_repository import UserRepository

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/users/", response_model=user_dto.UserDTO)
async def create_user(user: user_dto.UserCreateDTO, db: AsyncSession = Depends(create_database_session)):
    db_session_context.set(db)
    res = await UserRepository().create(user)
    return res


