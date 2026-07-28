from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.modules.compra.domain.repositories.compra_repository import CompraRepository
from app.modules.compra.infrastructure.persistence.repositories.compra_repository_impl import CompraRepositoryImpl
from app.modules.compra.application.ports.unit_of_work import UnitOfWork
from app.modules.compra.infrastructure.unit_of_work.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork

from app.modules.compra.application.ports.supplier_lookup import SupplierLookup
from app.modules.compra.application.ports.product_lookup import ProductLookup

# Lookups dependencies from other modules
from app.modules.supplier.data.repositories.supplier_repository_impl import SupplierRepositoryImpl
from app.modules.product.data.repositories.product_repository_impl import ProductRepositoryImpl

from app.modules.compra.application.use_cases import (
    RegistrarCompraUseCase,
    AnularCompraUseCase,
    ObtenerCompraUseCase,
    ListarComprasUseCase,
    RegistrarDevolucionProveedorUseCase,
)
from app.common.event_dispatcher import EventDispatcher

class SupplierLookupImpl(SupplierLookup):
    def __init__(self, db: Session):
        self.repo = SupplierRepositoryImpl(db)

    def exists_and_active(self, company_id: UUID, supplier_id: UUID) -> bool:
        supplier = self.repo.get_by_id(supplier_id)
        return (
            supplier is not None 
            and supplier.company_id == company_id 
            and supplier.status == "ACTIVO"
        )

class ProductLookupImpl(ProductLookup):
    def __init__(self, db: Session):
        self.repo = ProductRepositoryImpl(db)

    def exists_and_active(self, company_id: UUID, product_id: UUID) -> bool:
        product = self.repo.get_by_id(product_id)
        return (
            product is not None 
            and product.company_id == company_id 
            and product.status == "ACTIVO"
        )

def get_compra_repository(db: Session = Depends(get_db)) -> CompraRepository:
    return CompraRepositoryImpl(db)

def get_unit_of_work(db: Session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(db)

def get_supplier_lookup(db: Session = Depends(get_db)) -> SupplierLookup:
    return SupplierLookupImpl(db)

def get_product_lookup(db: Session = Depends(get_db)) -> ProductLookup:
    return ProductLookupImpl(db)

def get_event_dispatcher() -> EventDispatcher:
    return EventDispatcher()

def get_registrar_compra_use_case(
    repository: CompraRepository = Depends(get_compra_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    supplier_lookup: SupplierLookup = Depends(get_supplier_lookup),
    product_lookup: ProductLookup = Depends(get_product_lookup),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> RegistrarCompraUseCase:
    return RegistrarCompraUseCase(
        repository=repository,
        uow=uow,
        supplier_lookup=supplier_lookup,
        product_lookup=product_lookup,
        event_dispatcher=event_dispatcher
    )

def get_anular_compra_use_case(
    repository: CompraRepository = Depends(get_compra_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> AnularCompraUseCase:
    return AnularCompraUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )

def get_obtener_compra_use_case(
    repository: CompraRepository = Depends(get_compra_repository)
) -> ObtenerCompraUseCase:
    return ObtenerCompraUseCase(repository)

def get_listar_compras_use_case(
    repository: CompraRepository = Depends(get_compra_repository)
) -> ListarComprasUseCase:
    return ListarComprasUseCase(repository)

def get_registrar_devolucion_use_case(
    repository: CompraRepository = Depends(get_compra_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> RegistrarDevolucionProveedorUseCase:
    return RegistrarDevolucionProveedorUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )
