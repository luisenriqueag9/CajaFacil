from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_
from app.database.repositories import BaseRepository
from app.modules.purchase.domain.entities.purchase import Purchase as DomainPurchase
from app.modules.purchase.domain.repositories.purchase_repository import PurchaseRepository
from app.modules.purchase.data.models import Purchase as DBPurchase
from app.modules.purchase.data.mappers import purchase_mapper
from app.modules.purchase.domain.exceptions.purchase_not_found_exception import PurchaseNotFoundException

class PurchaseRepositoryImpl(BaseRepository[DBPurchase], PurchaseRepository):
    """
    Concrete implementation of PurchaseRepository interface using SQLAlchemy.
    """
    def __init__(self, db: Session):
        super().__init__(DBPurchase, db)

    def create(self, purchase: DomainPurchase) -> DomainPurchase:
        db_purchase = purchase_mapper.to_db(purchase)
        db_purchase = super().create(db_purchase)
        self.db.flush()
        # Re-fetch with details relationship pre-loaded
        statement = select(DBPurchase).where(DBPurchase.id == purchase.id).options(joinedload(DBPurchase.details))
        db_purchase = self.db.execute(statement).unique().scalar_one()
        return purchase_mapper.to_domain(db_purchase)

    def get_by_id(self, purchase_id: UUID) -> DomainPurchase | None:
        statement = select(DBPurchase).where(DBPurchase.id == purchase_id).options(joinedload(DBPurchase.details))
        db_purchase = self.db.execute(statement).unique().scalar_one_or_none()
        return purchase_mapper.to_domain(db_purchase) if db_purchase else None

    def get_by_invoice_number(
        self, 
        company_id: UUID, 
        supplier_id: UUID, 
        invoice_number: str
    ) -> DomainPurchase | None:
        statement = select(DBPurchase).where(
            and_(
                DBPurchase.company_id == company_id,
                DBPurchase.supplier_id == supplier_id,
                DBPurchase.invoice_number == invoice_number
            )
        ).options(joinedload(DBPurchase.details))
        
        db_purchase = self.db.execute(statement).unique().scalar_one_or_none()
        return purchase_mapper.to_domain(db_purchase) if db_purchase else None

    def get_all(
        self, 
        company_id: UUID, 
        status: str | None = None, 
        supplier_id: UUID | None = None
    ) -> list[DomainPurchase]:
        statement = select(DBPurchase).where(DBPurchase.company_id == company_id).options(joinedload(DBPurchase.details))
        if status:
            statement = statement.where(DBPurchase.status == status)
        if supplier_id:
            statement = statement.where(DBPurchase.supplier_id == supplier_id)
            
        statement = statement.order_by(DBPurchase.created_at.desc())
        db_purchases = self.db.execute(statement).unique().scalars().all()
        return [purchase_mapper.to_domain(p) for p in db_purchases]

    def update(self, purchase: DomainPurchase) -> DomainPurchase:
        statement = select(DBPurchase).where(DBPurchase.id == purchase.id).options(joinedload(DBPurchase.details))
        db_purchase = self.db.execute(statement).unique().scalar_one_or_none()
        if not db_purchase:
            raise PurchaseNotFoundException(purchase.id)

        purchase_mapper.update_db_model(db_purchase, purchase)
        self.db.flush()
        self.db.refresh(db_purchase)
        return purchase_mapper.to_domain(db_purchase)
