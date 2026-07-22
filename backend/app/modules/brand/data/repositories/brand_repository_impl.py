from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from app.database.repositories import BaseRepository
from app.modules.brand.domain.entities.brand import Brand as DomainBrand
from app.modules.brand.domain.repositories.brand_repository import BrandRepository
from app.modules.brand.data.models import Brand as DBBrand
from app.modules.brand.data.mappers import brand_mapper
from app.modules.brand.domain.exceptions.brand_not_found_exception import BrandNotFoundException

class BrandRepositoryImpl(BaseRepository[DBBrand], BrandRepository):
    """
    Concrete implementation of BrandRepository interface using SQLAlchemy.
    """
    def __init__(self, db: Session):
        super().__init__(DBBrand, db)

    def create(self, brand: DomainBrand) -> DomainBrand:
        db_brand = brand_mapper.to_db(brand)
        db_brand = super().create(db_brand)
        self.db.refresh(db_brand)
        return brand_mapper.to_domain(db_brand)

    def get_by_id(self, brand_id: UUID) -> DomainBrand | None:
        db_brand = super().get_by_id(brand_id)
        return brand_mapper.to_domain(db_brand) if db_brand else None

    def get_by_name(self, company_id: UUID, name: str) -> DomainBrand | None:
        statement = select(DBBrand).where(
            and_(
                DBBrand.company_id == company_id,
                func.lower(DBBrand.name) == func.lower(name)
            )
        )
        db_brand = self.db.execute(statement).scalar_one_or_none()
        return brand_mapper.to_domain(db_brand) if db_brand else None

    def get_all(self, company_id: UUID, status: str | None = None) -> list[DomainBrand]:
        statement = select(DBBrand).where(DBBrand.company_id == company_id)
        if status:
            statement = statement.where(DBBrand.status == status)
        
        statement = statement.order_by(DBBrand.name)
        db_brands = self.db.execute(statement).scalars().all()
        return [brand_mapper.to_domain(b) for b in db_brands]

    def update(self, brand: DomainBrand) -> DomainBrand:
        db_brand = super().get_by_id(brand.id)
        if not db_brand:
            raise BrandNotFoundException(brand.id)

        brand_mapper.update_db_model(db_brand, brand)
        self.db.flush()
        self.db.refresh(db_brand)
        return brand_mapper.to_domain(db_brand)

    def delete(self, brand_id: UUID) -> bool:
        db_brand = super().get_by_id(brand_id)
        if db_brand:
            self.db.delete(db_brand)
            self.db.flush()
            return True
        return False
