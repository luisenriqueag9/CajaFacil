from uuid import UUID
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from app.database.repositories import BaseRepository
from app.modules.venta.domain.entities.venta import Venta as DomainVenta
from app.modules.venta.domain.repositories.venta_repository import VentaRepository
from app.modules.venta.data.models import Venta as DBVenta
from app.modules.venta.data.mappers import venta_mapper
from app.modules.venta.domain.exceptions import VentaNotFoundException

class VentaRepositoryImpl(BaseRepository[DBVenta], VentaRepository):
    """
    Concrete implementation of VentaRepository interface using SQLAlchemy.
    Integrates into SQLAlchemy session without committing immediately,
    supporting Unit of Work coordinated by Use Cases.
    """
    def __init__(self, db: Session):
        super().__init__(DBVenta, db)

    def save(self, venta: DomainVenta) -> DomainVenta:
        # Check if record already exists
        statement = select(DBVenta).where(DBVenta.id == venta.id).options(
            joinedload(DBVenta.details),
            joinedload(DBVenta.payments)
        )
        db_venta = self.db.execute(statement).unique().scalar_one_or_none()

        if db_venta is not None:
            # Update existing record
            venta_mapper.update_db_model(db_venta, venta)
            self.db.flush()
            self.db.refresh(db_venta)
            return venta_mapper.to_domain(db_venta)
        else:
            # Create new record
            db_venta = venta_mapper.to_db(venta)
            self.db.add(db_venta)
            self.db.flush()
            # Re-fetch to ensure relationships are correctly populated
            db_venta = self.db.execute(statement).unique().scalar_one()
            return venta_mapper.to_domain(db_venta)

    def get_by_id(self, venta_id: UUID) -> Optional[DomainVenta]:
        statement = select(DBVenta).where(DBVenta.id == venta_id).options(
            joinedload(DBVenta.details),
            joinedload(DBVenta.payments)
        )
        db_venta = self.db.execute(statement).unique().scalar_one_or_none()
        return venta_mapper.to_domain(db_venta) if db_venta else None

    def get_by_invoice_number(self, company_id: UUID, invoice_number: str) -> Optional[DomainVenta]:
        statement = select(DBVenta).where(
            and_(
                DBVenta.company_id == company_id,
                DBVenta.invoice_number == invoice_number
            )
        ).options(
            joinedload(DBVenta.details),
            joinedload(DBVenta.payments)
        )
        db_venta = self.db.execute(statement).unique().scalar_one_or_none()
        return venta_mapper.to_domain(db_venta) if db_venta else None

    def search(self, company_id: UUID, filters: dict) -> List[DomainVenta]:
        statement = select(DBVenta).where(DBVenta.company_id == company_id).options(
            joinedload(DBVenta.details),
            joinedload(DBVenta.payments)
        )

        # Apply optional filters
        if "box_id" in filters and filters["box_id"]:
            statement = statement.where(DBVenta.box_id == filters["box_id"])
        if "user_id" in filters and filters["user_id"]:
            statement = statement.where(DBVenta.user_id == filters["user_id"])
        if "client_id" in filters and filters["client_id"]:
            statement = statement.where(DBVenta.client_id == filters["client_id"])
        if "status" in filters and filters["status"]:
            db_status = venta_mapper.STATUS_TO_DB.get(filters["status"])
            if db_status:
                statement = statement.where(DBVenta.status == db_status)
        if "start_date" in filters and filters["start_date"]:
            statement = statement.where(DBVenta.created_at >= filters["start_date"])
        if "end_date" in filters and filters["end_date"]:
            statement = statement.where(DBVenta.created_at <= filters["end_date"])

        statement = statement.order_by(DBVenta.created_at.desc())
        db_ventas = self.db.execute(statement).unique().scalars().all()
        return [venta_mapper.to_domain(v) for v in db_ventas]
