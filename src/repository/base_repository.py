from typing import TypeVar, Generic, Any

from src.utils.db_utils import db_session_context
import logging
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

logger = logging.getLogger(__name__)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository class for CRUD operations.
    """

    def __init__(self, model: ModelType):
        self.model = model

    async def get_all(self) -> list[ModelType]:
        """
        Retrieve all records from the database.
        """
        db = db_session_context.get()
        return await db.execute(self.model.__table__.select()).scalars().all()

    async def get_by_id(self, id: Any) -> ModelType | None:
        """
        Retrieve a record by its ID.
        """
        db = db_session_context.get()
        return await db.query(self.model).filter(self.model.id == id).first()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record in the database.
        """
        db = db_session_context.get()
        obj = self.model(**obj_in.dict())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        logger.debug(f"Created new object: {obj}")
        return obj

    async def update(self, id: Any, obj_in: UpdateSchemaType) -> ModelType | None:
        """
        Update an existing record in the database.
        """
        db = db_session_context.get()
        obj = await self.get_by_id(id)
        if not obj:
            return None
        for key, value in obj_in.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete(self, id: Any) -> ModelType | None:
        """
        Delete a record from the database.
        """
        db = db_session_context.get()
        obj = await self.get_by_id(id)
        if not obj:
            return None
        await db.delete(obj)
        await db.commit()
        return obj
