from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.modules.venta.application.ports.movimiento_inventario_repository import MovimientoInventarioRepository
from app.modules.venta.application.ports.movimiento_caja_repository import MovimientoCajaRepository
from app.modules.venta.application.ports.credito_repository import CreditoRepository

from app.modules.venta.data.models import DBMovimientoInventario, DBMovimientoCaja, DBCredito

class MockMovimientoInventarioRepositoryImpl(MovimientoInventarioRepository):
    def __init__(self, db: Session):
        self.db = db

    def registrar_movimiento(
        self,
        company_id: UUID,
        product_id: UUID,
        quantity: Decimal,
        tipo: str,
        concept: str,
        reference_id: UUID
    ) -> None:
        db_mov = DBMovimientoInventario(
            id=uuid4(),
            company_id=company_id,
            product_id=product_id,
            quantity=quantity,
            tipo=tipo,
            concept=concept,
            reference_id=reference_id,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(db_mov)
        self.db.flush()


class MockMovimientoCajaRepositoryImpl(MovimientoCajaRepository):
    def __init__(self, db: Session):
        self.db = db

    def registrar_movimiento(
        self,
        company_id: UUID,
        box_id: UUID,
        user_id: UUID,
        amount: Decimal,
        tipo: str,
        concept: str,
        reference_id: UUID
    ) -> None:
        db_mov = DBMovimientoCaja(
            id=uuid4(),
            company_id=company_id,
            box_id=box_id,
            user_id=user_id,
            amount=amount,
            tipo=tipo,
            concept=concept,
            reference_id=reference_id,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(db_mov)
        self.db.flush()


class MockCreditoRepositoryImpl(CreditoRepository):
    def __init__(self, db: Session):
        self.db = db

    def registrar_deuda(
        self,
        company_id: UUID,
        client_id: UUID,
        amount: Decimal,
        reference_id: UUID
    ) -> None:
        db_cred = DBCredito(
            id=uuid4(),
            company_id=company_id,
            client_id=client_id,
            amount=amount,
            reference_id=reference_id,
            status="ACTIVO",
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(db_cred)
        self.db.flush()

    def reversar_deuda(
        self,
        company_id: UUID,
        client_id: UUID,
        amount: Decimal,
        reference_id: UUID
    ) -> None:
        statement = select(DBCredito).where(
            and_(
                DBCredito.company_id == company_id,
                DBCredito.client_id == client_id,
                DBCredito.reference_id == reference_id
            )
        )
        db_cred = self.db.execute(statement).scalars().first()
        if db_cred:
            db_cred.status = "ANULADO"
            self.db.flush()
