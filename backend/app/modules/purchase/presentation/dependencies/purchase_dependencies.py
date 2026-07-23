from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.logger import logger

from app.modules.purchase.domain.repositories.purchase_repository import PurchaseRepository
from app.modules.purchase.data.repositories.purchase_repository_impl import PurchaseRepositoryImpl

from app.modules.purchase.application.ports.supplier_lookup import SupplierLookup
from app.modules.purchase.application.ports.product_lookup import ProductLookup
from app.modules.purchase.application.ports.event_publisher import EventPublisher

from app.modules.supplier.data.repositories.supplier_repository_impl import SupplierRepositoryImpl
from app.modules.product.data.repositories.product_repository_impl import ProductRepositoryImpl

from app.modules.purchase.application.use_cases import (
    RegisterPurchaseUseCase,
    AnnulPurchaseUseCase,
    GetPurchaseByIdUseCase,
    ListPurchasesUseCase,
)

class SupplierLookupImpl(SupplierLookup):
    """
    Port implementation delegating lookup to the Supplier concrete repository.
    """
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
    """
    Port implementation delegating lookup to the Product concrete repository.
    """
    def __init__(self, db: Session):
        self.repo = ProductRepositoryImpl(db)

    def exists_and_active(self, company_id: UUID, product_id: UUID) -> bool:
        product = self.repo.get_by_id(product_id)
        return (
            product is not None 
            and product.company_id == company_id 
            and product.status == "ACTIVO"
        )

class LogEventPublisher(EventPublisher):
    """
    Port implementation that logs published events for auditing.
    """
    def publish(self, event: object) -> None:
        logger.info(f"[Event Dispatcher] Published: {event.__class__.__name__} -> {event}")


def get_purchase_repository(db: Session = Depends(get_db)) -> PurchaseRepository:
    return PurchaseRepositoryImpl(db)

def get_supplier_lookup(db: Session = Depends(get_db)) -> SupplierLookup:
    return SupplierLookupImpl(db)

def get_product_lookup(db: Session = Depends(get_db)) -> ProductLookup:
    return ProductLookupImpl(db)

def get_event_publisher() -> EventPublisher:
    return LogEventPublisher()

def get_register_purchase_use_case(
    repository: PurchaseRepository = Depends(get_purchase_repository),
    supplier_lookup: SupplierLookup = Depends(get_supplier_lookup),
    product_lookup: ProductLookup = Depends(get_product_lookup),
    event_publisher: EventPublisher = Depends(get_event_publisher)
) -> RegisterPurchaseUseCase:
    return RegisterPurchaseUseCase(repository, supplier_lookup, product_lookup, event_publisher)

def get_annul_purchase_use_case(
    repository: PurchaseRepository = Depends(get_purchase_repository),
    event_publisher: EventPublisher = Depends(get_event_publisher)
) -> AnnulPurchaseUseCase:
    return AnnulPurchaseUseCase(repository, event_publisher)

def get_get_purchase_by_id_use_case(
    repository: PurchaseRepository = Depends(get_purchase_repository)
) -> GetPurchaseByIdUseCase:
    return GetPurchaseByIdUseCase(repository)

def get_list_purchases_use_case(
    repository: PurchaseRepository = Depends(get_purchase_repository)
) -> ListPurchasesUseCase:
    return ListPurchasesUseCase(repository)
