from uuid import UUID
from decimal import Decimal
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.database.session import get_db
from app.modules.venta.domain.repositories.venta_repository import VentaRepository
from app.modules.venta.data.repositories.venta_repository_impl import VentaRepositoryImpl

from app.modules.venta.application.ports.product_lookup import ProductLookup
from app.modules.venta.application.ports.box_lookup import BoxLookup
from app.modules.venta.application.ports.credit_lookup import CreditLookup
from app.common.event_dispatcher import EventDispatcher

from app.modules.product.data.models import Product as DBProduct

from app.modules.venta.application.use_cases import (
    ConfirmarVentaUseCase,
    AnularVentaUseCase,
    GetVentaByIdUseCase,
    ListSalesUseCase
)

class ProductLookupImpl(ProductLookup):
    """
    Delegates product verification to the Product SQLAlchemy model.
    """
    def __init__(self, db: Session):
        self.db = db

    def exists_and_active(self, company_id: UUID, product_id: UUID) -> bool:
        statement = select(DBProduct).where(
            and_(
                DBProduct.id == product_id,
                DBProduct.company_id == company_id
            )
        )
        db_product = self.db.execute(statement).scalar_one_or_none()
        return db_product is not None and db_product.status == "ACTIVO"


class BoxLookupImpl(BoxLookup):
    """
    Stub lookup for Box registers since Box module is not yet implemented.
    Always returns True for valid box_id.
    """
    def is_open_and_active(self, company_id: UUID, box_id: UUID) -> bool:
        return True


class CreditLookupImpl(CreditLookup):
    """
    Look up client credit line using CreditoRepository interface.
    """
    def __init__(self, credit_repository):
        self.credit_repository = credit_repository

    def has_active_credit_and_limit(self, company_id: UUID, client_id: UUID, required_amount: Decimal) -> bool:
        credit = self.credit_repository.get_by_client_id(company_id, client_id)
        if not credit:
            return False
            
        if credit.status.valor != "ACTIVO":
            return False
            
        available = credit.credit_limit.monto - credit.balance.monto
        return available >= required_amount


def get_venta_repository(db: Session = Depends(get_db)) -> VentaRepository:
    return VentaRepositoryImpl(db)

def get_product_lookup(db: Session = Depends(get_db)) -> ProductLookup:
    return ProductLookupImpl(db)

def get_box_lookup() -> BoxLookup:
    return BoxLookupImpl()

def get_credit_lookup(db: Session = Depends(get_db)) -> CreditLookup:
    from app.modules.credito.infrastructure.persistence.repositories.credito_repository_impl import CreditoRepositoryImpl
    repo = CreditoRepositoryImpl(db)
    return CreditLookupImpl(repo)

from app.modules.venta.application.ports.movimiento_inventario_repository import MovimientoInventarioRepository
from app.modules.venta.application.ports.movimiento_caja_repository import MovimientoCajaRepository
from app.modules.venta.application.ports.credito_repository import CreditoRepository

class MovimientoCajaRepositoryAdapter(MovimientoCajaRepository):
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
        from app.modules.caja.infrastructure.persistence.repositories.sesion_caja_repository_impl import SesionCajaRepositoryImpl
        repo = SesionCajaRepositoryImpl(self.db)
        
        sesion = repo.get_active_by_caja(company_id, box_id)
        if not sesion:
            from app.modules.caja.domain.exceptions import CajaNoAbiertaException
            raise CajaNoAbiertaException(box_id)
            
        import uuid
        from datetime import datetime, timezone
        sesion.registrar_movimiento(
            id=uuid.uuid4(),
            type=tipo,
            amount=amount,
            payment_method="EFECTIVO",
            concept=concept,
            origin_context="Ventas",
            origin_document_id=reference_id,
            timestamp=datetime.now(timezone.utc)
        )
        repo.update(sesion)

class CreditoRepositoryAdapter(CreditoRepository):
    def __init__(self, db: Session):
        self.db = db

    def registrar_deuda(
        self,
        company_id: UUID,
        client_id: UUID,
        amount: Decimal,
        reference_id: UUID
    ) -> None:
        pass

    def reversar_deuda(
        self,
        company_id: UUID,
        client_id: UUID,
        amount: Decimal,
        reference_id: UUID
    ) -> None:
        pass

def get_event_dispatcher(db: Session = Depends(get_db)) -> EventDispatcher:
    """
    Generates a request-scoped EventDispatcher, subscribing handlers bound to
    the current request database Session. This guarantees that all handler operations
    participate sychronously within the exact same database transaction.
    """
    from app.modules.venta.application.handlers.venta_confirmada_handlers import VentaEventHandler
    from app.modules.venta.domain.events.venta_events import VentaConfirmada, VentaAnulada

    # 1. Instantiate adapters utilizing the current request database session
    from app.modules.inventario.data.repositories.venta_inventario_repository_adapter import VentaInventoryRepositoryAdapter
    inv_repo = VentaInventoryRepositoryAdapter(db)
    caja_repo = MovimientoCajaRepositoryAdapter(db)
    cred_repo = CreditoRepositoryAdapter(db)

    # 2. Instantiate handlers
    handler = VentaEventHandler(inv_repo, caja_repo, cred_repo)

    # 3. Create request-scoped EventDispatcher
    dispatcher = EventDispatcher()
    dispatcher.subscribe(VentaConfirmada, handler.handle_confirmada)
    dispatcher.subscribe(VentaAnulada, handler.handle_anulada)
    return dispatcher

def get_confirmar_venta_use_case(
    repository: VentaRepository = Depends(get_venta_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    product_lookup: ProductLookup = Depends(get_product_lookup),
    box_lookup: BoxLookup = Depends(get_box_lookup),
    credit_lookup: CreditLookup = Depends(get_credit_lookup)
) -> ConfirmarVentaUseCase:
    return ConfirmarVentaUseCase(
        repository=repository,
        db=db,
        event_dispatcher=event_dispatcher,
        product_lookup=product_lookup,
        box_lookup=box_lookup,
        credit_lookup=credit_lookup
    )

def get_anular_venta_use_case(
    repository: VentaRepository = Depends(get_venta_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> AnularVentaUseCase:
    return AnularVentaUseCase(
        repository=repository,
        db=db,
        event_dispatcher=event_dispatcher
    )

def get_get_venta_by_id_use_case(
    repository: VentaRepository = Depends(get_venta_repository)
) -> GetVentaByIdUseCase:
    return GetVentaByIdUseCase(repository)

def get_list_sales_use_case(
    repository: VentaRepository = Depends(get_venta_repository)
) -> ListSalesUseCase:
    return ListSalesUseCase(repository)
