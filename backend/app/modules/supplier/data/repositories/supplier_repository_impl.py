from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from app.database.repositories import BaseRepository
from app.modules.supplier.domain.entities.supplier import Supplier as DomainSupplier
from app.modules.supplier.domain.repositories.supplier_repository import SupplierRepository
from app.modules.supplier.data.models import Supplier as DBSupplier
from app.modules.supplier.data.mappers import supplier_mapper
from app.modules.supplier.domain.exceptions.supplier_not_found_exception import SupplierNotFoundException

class SupplierRepositoryImpl(BaseRepository[DBSupplier], SupplierRepository):
    """
    Concrete implementation of SupplierRepository interface using SQLAlchemy.
    """
    def __init__(self, db: Session):
        super().__init__(DBSupplier, db)

    def create(self, supplier: DomainSupplier) -> DomainSupplier:
        db_supplier = supplier_mapper.to_db(supplier)
        db_supplier = super().create(db_supplier)
        self.db.refresh(db_supplier)
        return supplier_mapper.to_domain(db_supplier)

    def get_by_id(self, supplier_id: UUID) -> DomainSupplier | None:
        db_supplier = super().get_by_id(supplier_id)
        return supplier_mapper.to_domain(db_supplier) if db_supplier else None

    def get_by_tax_id(self, company_id: UUID, tax_id: str) -> DomainSupplier | None:
        statement = select(DBSupplier).where(
            and_(
                DBSupplier.company_id == company_id,
                func.lower(DBSupplier.tax_id) == func.lower(tax_id)
            )
        )
        db_supplier = self.db.execute(statement).scalar_one_or_none()
        return supplier_mapper.to_domain(db_supplier) if db_supplier else None

    def get_all(self, company_id: UUID, status: str | None = None) -> list[DomainSupplier]:
        statement = select(DBSupplier).where(DBSupplier.company_id == company_id)
        if status:
            statement = statement.where(DBSupplier.status == status)
        
        statement = statement.order_by(DBSupplier.name)
        db_suppliers = self.db.execute(statement).scalars().all()
        return [supplier_mapper.to_domain(s) for s in db_suppliers]

    def update(self, supplier: DomainSupplier) -> DomainSupplier:
        db_supplier = super().get_by_id(supplier.id)
        if not db_supplier:
            raise SupplierNotFoundException(supplier.id)

        supplier_mapper.update_db_model(db_supplier, supplier)
        self.db.flush()
        self.db.refresh(db_supplier)
        return supplier_mapper.to_domain(db_supplier)
