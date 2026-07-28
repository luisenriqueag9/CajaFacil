from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_
from app.database.repositories.base import BaseRepository
from app.modules.compra.domain.aggregates.compra import Compra
from app.modules.compra.domain.repositories.compra_repository import CompraRepository
from app.modules.compra.infrastructure.persistence.models.compra_model import Compra as DBOCompra
from app.modules.compra.infrastructure.persistence.mappers.compra_mapper import CompraMapper
from app.modules.compra.domain.exceptions.compra_no_encontrada_exception import CompraNoEncontradaException

class CompraRepositoryImpl(BaseRepository[DBOCompra], CompraRepository):
    """
    Implementacion concreta de la interfaz CompraRepository utilizando SQLAlchemy.
    """
    def __init__(self, db: Session):
        super().__init__(DBOCompra, db)

    def create(self, compra: Compra) -> Compra:
        db_purchase = CompraMapper.to_db(compra)
        # Adds object to sqlalchemy session
        self.db.add(db_purchase)
        self.db.flush()
        # Re-fetch with details relationship pre-loaded
        statement = select(DBOCompra).where(DBOCompra.id == compra.id).options(joinedload(DBOCompra.details))
        db_purchase = self.db.execute(statement).unique().scalar_one()
        return CompraMapper.to_domain(db_purchase)

    def get_by_id(self, purchase_id: UUID) -> Compra | None:
        statement = select(DBOCompra).where(DBOCompra.id == purchase_id).options(joinedload(DBOCompra.details))
        db_purchase = self.db.execute(statement).unique().scalar_one_or_none()
        return CompraMapper.to_domain(db_purchase) if db_purchase else None

    def get_by_invoice_number(
        self, 
        company_id: UUID, 
        supplier_id: UUID, 
        invoice_number: str
    ) -> Compra | None:
        statement = select(DBOCompra).where(
            and_(
                DBOCompra.company_id == company_id,
                DBOCompra.supplier_id == supplier_id,
                DBOCompra.invoice_number == invoice_number
            )
        ).options(joinedload(DBOCompra.details))
        
        db_purchase = self.db.execute(statement).unique().scalar_one_or_none()
        return CompraMapper.to_domain(db_purchase) if db_purchase else None

    def get_all(
        self, 
        company_id: UUID, 
        status: str | None = None, 
        supplier_id: UUID | None = None
    ) -> list[Compra]:
        statement = select(DBOCompra).where(DBOCompra.company_id == company_id).options(joinedload(DBOCompra.details))
        if status:
            statement = statement.where(DBOCompra.status == status)
        if supplier_id:
            statement = statement.where(DBOCompra.supplier_id == supplier_id)
            
        statement = statement.order_by(DBOCompra.created_at.desc())
        db_purchases = self.db.execute(statement).unique().scalars().all()
        return [CompraMapper.to_domain(p) for p in db_purchases]

    def update(self, compra: Compra) -> Compra:
        statement = select(DBOCompra).where(DBOCompra.id == compra.id).options(joinedload(DBOCompra.details))
        db_purchase = self.db.execute(statement).unique().scalar_one_or_none()
        if not db_purchase:
            raise CompraNoEncontradaException(compra.id)

        CompraMapper.update_db_model(db_purchase, compra)
        self.db.flush()
        self.db.refresh(db_purchase)
        return CompraMapper.to_domain(db_purchase)
