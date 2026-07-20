from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    SQLAlchemy 2.0 Unified Reusable Base Repository.
    Provides generic data access logic decoupled from domain entities.
    """
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: UUID) -> ModelType | None:
        """Retrieve a single database record by its UUID primary key using db.get()."""
        return self.db.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Retrieve a paginated sequence of database records using SQLAlchemy 2.0 syntax."""
        stmt = select(self.model).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def create(self, obj_in: ModelType) -> ModelType:
        """Add a new database record to the current session and flush changes."""
        self.db.add(obj_in)
        self.db.flush()
        return obj_in

    def delete_physical(self, obj: ModelType) -> None:
        """Remove a database record physically from the database session and flush."""
        self.db.delete(obj)
        self.db.flush()
