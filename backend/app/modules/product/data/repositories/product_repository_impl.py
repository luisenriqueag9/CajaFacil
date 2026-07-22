from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_
from app.database.repositories import BaseRepository
from app.modules.product.domain.entities.product import Product as DomainProduct
from app.modules.product.domain.repositories.product_repository import ProductRepository
from app.modules.product.data.models import Product as DBProduct
from app.modules.product.data.mappers import product_mapper
from app.modules.product.domain.exceptions.product_not_found_exception import ProductNotFoundException

class ProductRepositoryImpl(BaseRepository[DBProduct], ProductRepository):
    """
    Concrete implementation of the ProductRepository using SQLAlchemy and SQLite/PostgreSQL.
    Inherits generic CRUD operations from BaseRepository.
    """
    def __init__(self, db: Session):
        super().__init__(DBProduct, db)

    def create(self, product: DomainProduct) -> DomainProduct:
        db_product = product_mapper.to_db(product)
        db_product = super().create(db_product)
        self.db.refresh(db_product)
        return product_mapper.to_domain(db_product)

    def get_by_id(self, product_id: UUID) -> DomainProduct | None:
        db_product = super().get_by_id(product_id)
        return product_mapper.to_domain(db_product) if db_product else None

    def get_by_internal_code(self, company_id: UUID, internal_code: str) -> DomainProduct | None:
        statement = select(DBProduct).where(
            and_(
                DBProduct.company_id == company_id,
                DBProduct.internal_code == internal_code
            )
        )
        db_product = self.db.execute(statement).scalar_one_or_none()
        return product_mapper.to_domain(db_product) if db_product else None

    def get_by_barcode(self, company_id: UUID, barcode: str) -> DomainProduct | None:
        statement = select(DBProduct).where(
            and_(
                DBProduct.company_id == company_id,
                DBProduct.barcode == barcode
            )
        )
        db_product = self.db.execute(statement).scalar_one_or_none()
        return product_mapper.to_domain(db_product) if db_product else None

    def get_all(
        self,
        company_id: UUID,
        category_id: UUID | None = None,
        brand_id: UUID | None = None,
        status: str | None = None,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[DomainProduct]:
        # Enforce multi-tenancy by filtering on company_id first
        query = select(DBProduct).where(DBProduct.company_id == company_id)

        # Apply domain relational filters
        if category_id:
            query = query.where(DBProduct.category_id == category_id)
        if brand_id:
            query = query.where(DBProduct.brand_id == brand_id)
        
        # Apply status filter using Mapper translation (centralized logic)
        if status:
            db_status = product_mapper.to_db_status(status)
            query = query.where(DBProduct.status == db_status)

        # Apply search string matching across name, barcode, and internal_code
        if search:
            search_clause = f"%{search}%"
            query = query.where(
                or_(
                    DBProduct.name.ilike(search_clause),
                    DBProduct.barcode.ilike(search_clause),
                    DBProduct.internal_code.ilike(search_clause)
                )
            )

        # Order by name (stable sort)
        query = query.order_by(DBProduct.name)

        # Apply pagination limits
        query = query.offset(offset).limit(limit)
        
        db_products = self.db.execute(query).scalars().all()
        return [product_mapper.to_domain(p) for p in db_products]

    def update(self, product: DomainProduct) -> DomainProduct:
        db_product = super().get_by_id(product.id)
        if not db_product:
            raise ProductNotFoundException(product.id)
        
        product_mapper.update_db_model(db_product, product)
        self.db.flush()
        self.db.refresh(db_product)
        return product_mapper.to_domain(db_product)
