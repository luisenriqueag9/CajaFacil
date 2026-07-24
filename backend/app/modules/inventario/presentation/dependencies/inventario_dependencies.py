from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.database.session import get_db
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository
from app.modules.inventario.data.repositories.movimiento_repository_impl import MovimientoInventarioRepositoryImpl

from app.modules.inventario.domain.repositories.existencia_repository import ExistenciaRepository
from app.modules.inventario.data.repositories.existencia_repository_impl import ExistenciaRepositoryImpl

from app.modules.inventario.application.ports.product_lookup import ProductLookup, ProductDetails
from app.modules.inventario.application.event_dispatcher import EventDispatcher

from app.modules.product.data.models import Product as DBProduct

from app.modules.inventario.application.ports.stock_checker import StockCheckerPort
from app.modules.inventario.application.ports.stock_checker_impl import StockCheckerImpl

from app.modules.inventario.application.use_cases import (
    RegistrarMovimientoUseCase,
    RegistrarMermaUseCase,
    RegistrarAjusteUseCase,
    ObtenerStockProductoUseCase,
    ListarMovimientosUseCase,
    ConsultarExistenciaUseCase,
    RecalcularExistenciaDesdeKardexUseCase
)

class ProductLookupImpl(ProductLookup):
    """
    Concrete implementation of ProductLookup retrieving metadata from the database model.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_details(self, company_id: UUID, product_id: UUID) -> ProductDetails:
        statement = select(DBProduct).where(
            and_(
                DBProduct.id == product_id,
                DBProduct.company_id == company_id
            )
        )
        db_product = self.db.execute(statement).scalar_one_or_none()
        if db_product is None:
            return ProductDetails(exists=False, active=False, controls_stock=False, allows_negative=False)

        # Map status (database ACTIVE translates to active=True)
        is_active = (db_product.status == "ACTIVE")
        return ProductDetails(
            exists=True,
            active=is_active,
            controls_stock=db_product.controls_stock,
            allows_negative=False  # Default False as it's not present in Product entity database fields yet
        )


def get_movimiento_repository(db: Session = Depends(get_db)) -> MovimientoInventarioRepository:
    return MovimientoInventarioRepositoryImpl(db)

def get_existencia_repository(db: Session = Depends(get_db)) -> ExistenciaRepository:
    return ExistenciaRepositoryImpl(db)

def get_product_lookup(db: Session = Depends(get_db)) -> ProductLookup:
    return ProductLookupImpl(db)

def get_event_dispatcher() -> EventDispatcher:
    """
    Provides an EventDispatcher instance.
    During development, this can be request-scoped or singleton.
    """
    return EventDispatcher()

def get_registrar_movimiento_use_case(
    repository: MovimientoInventarioRepository = Depends(get_movimiento_repository),
    existencia_repository: ExistenciaRepository = Depends(get_existencia_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    product_lookup: ProductLookup = Depends(get_product_lookup)
) -> RegistrarMovimientoUseCase:
    return RegistrarMovimientoUseCase(
        repository=repository,
        existencia_repository=existencia_repository,
        db=db,
        event_dispatcher=event_dispatcher,
        product_lookup=product_lookup
    )

def get_registrar_merma_use_case(
    repository: MovimientoInventarioRepository = Depends(get_movimiento_repository),
    existencia_repository: ExistenciaRepository = Depends(get_existencia_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    product_lookup: ProductLookup = Depends(get_product_lookup)
) -> RegistrarMermaUseCase:
    return RegistrarMermaUseCase(
        repository=repository,
        existencia_repository=existencia_repository,
        db=db,
        event_dispatcher=event_dispatcher,
        product_lookup=product_lookup
    )

def get_registrar_ajuste_use_case(
    repository: MovimientoInventarioRepository = Depends(get_movimiento_repository),
    existencia_repository: ExistenciaRepository = Depends(get_existencia_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    product_lookup: ProductLookup = Depends(get_product_lookup)
) -> RegistrarAjusteUseCase:
    return RegistrarAjusteUseCase(
        repository=repository,
        existencia_repository=existencia_repository,
        db=db,
        event_dispatcher=event_dispatcher,
        product_lookup=product_lookup
    )

def get_obtener_stock_producto_use_case(
    repository: ExistenciaRepository = Depends(get_existencia_repository),
    product_lookup: ProductLookup = Depends(get_product_lookup)
) -> ObtenerStockProductoUseCase:
    return ObtenerStockProductoUseCase(
        repository=repository,
        product_lookup=product_lookup
    )

def get_listar_movimientos_use_case(
    repository: MovimientoInventarioRepository = Depends(get_movimiento_repository)
) -> ListarMovimientosUseCase:
    return ListarMovimientosUseCase(repository)

def get_consultar_existencia_use_case(
    repository: ExistenciaRepository = Depends(get_existencia_repository),
    product_lookup: ProductLookup = Depends(get_product_lookup)
) -> ConsultarExistenciaUseCase:
    return ConsultarExistenciaUseCase(
        repository=repository,
        product_lookup=product_lookup
    )

def get_recalcular_existencia_use_case(
    existencia_repository: ExistenciaRepository = Depends(get_existencia_repository),
    movimiento_repository: MovimientoInventarioRepository = Depends(get_movimiento_repository),
    product_lookup: ProductLookup = Depends(get_product_lookup),
    db: Session = Depends(get_db)
) -> RecalcularExistenciaDesdeKardexUseCase:
    return RecalcularExistenciaDesdeKardexUseCase(
        existencia_repository=existencia_repository,
        movimiento_repository=movimiento_repository,
        product_lookup=product_lookup,
        db=db
    )

def get_stock_checker_port(
    existencia_repository: ExistenciaRepository = Depends(get_existencia_repository),
    product_lookup: ProductLookup = Depends(get_product_lookup)
) -> StockCheckerPort:
    return StockCheckerImpl(
        existencia_repository=existencia_repository,
        product_lookup=product_lookup
    )
