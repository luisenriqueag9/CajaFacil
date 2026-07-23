from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from app.database.repositories import BaseRepository
from app.modules.category.domain.entities.category import Category as DomainCategory
from app.modules.category.domain.repositories.category_repository import CategoryRepository
from app.modules.category.data.models import Category as DBCategory
from app.modules.category.data.mappers import category_mapper
from app.modules.category.domain.exceptions.category_not_found_exception import CategoryNotFoundException

class CategoryRepositoryImpl(BaseRepository[DBCategory], CategoryRepository):
    """
    Concrete implementation of CategoryRepository interface using SQLAlchemy.
    """
    def __init__(self, db: Session):
        super().__init__(DBCategory, db)

    def create(self, category: DomainCategory) -> DomainCategory:
        db_category = category_mapper.to_db(category)
        db_category = super().create(db_category)
        self.db.refresh(db_category)
        return category_mapper.to_domain(db_category)

    def get_by_id(self, category_id: UUID) -> DomainCategory | None:
        db_category = super().get_by_id(category_id)
        return category_mapper.to_domain(db_category) if db_category else None

    def get_by_name(self, company_id: UUID, name: str) -> DomainCategory | None:
        statement = select(DBCategory).where(
            and_(
                DBCategory.company_id == company_id,
                func.lower(DBCategory.name) == func.lower(name)
            )
        )
        db_category = self.db.execute(statement).scalar_one_or_none()
        return category_mapper.to_domain(db_category) if db_category else None

    def get_all(self, company_id: UUID, status: str | None = None) -> list[DomainCategory]:
        statement = select(DBCategory).where(DBCategory.company_id == company_id)
        if status:
            statement = statement.where(DBCategory.status == status)
        
        statement = statement.order_by(DBCategory.name)
        db_categories = self.db.execute(statement).scalars().all()
        return [category_mapper.to_domain(c) for c in db_categories]

    def update(self, category: DomainCategory) -> DomainCategory:
        db_category = super().get_by_id(category.id)
        if not db_category:
            raise CategoryNotFoundException(category.id)

        category_mapper.update_db_model(db_category, category)
        self.db.flush()
        self.db.refresh(db_category)
        return category_mapper.to_domain(db_category)

    def get_default_category(self, company_id: UUID) -> DomainCategory | None:
        statement = select(DBCategory).where(
            and_(
                DBCategory.company_id == company_id,
                DBCategory.protected == True
            )
        )
        db_category = self.db.execute(statement).scalar_one_or_none()
        return category_mapper.to_domain(db_category) if db_category else None
