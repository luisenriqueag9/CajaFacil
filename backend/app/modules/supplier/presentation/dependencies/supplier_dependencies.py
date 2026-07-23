from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.supplier.domain.repositories.supplier_repository import SupplierRepository
from app.modules.supplier.data.repositories.supplier_repository_impl import SupplierRepositoryImpl
from app.modules.supplier.application.use_cases import (
    CreateSupplierUseCase,
    UpdateSupplierUseCase,
    GetSupplierByIdUseCase,
    ListSuppliersUseCase,
    DeactivateSupplierUseCase,
    ActivateSupplierUseCase,
)

def get_supplier_repository(db: Session = Depends(get_db)) -> SupplierRepository:
    """FastAPI dependency to retrieve the concrete implementation of SupplierRepository."""
    return SupplierRepositoryImpl(db)

def get_create_supplier_use_case(
    repository: SupplierRepository = Depends(get_supplier_repository)
) -> CreateSupplierUseCase:
    return CreateSupplierUseCase(repository)

def get_update_supplier_use_case(
    repository: SupplierRepository = Depends(get_supplier_repository)
) -> UpdateSupplierUseCase:
    return UpdateSupplierUseCase(repository)

def get_get_supplier_by_id_use_case(
    repository: SupplierRepository = Depends(get_supplier_repository)
) -> GetSupplierByIdUseCase:
    return GetSupplierByIdUseCase(repository)

def get_list_suppliers_use_case(
    repository: SupplierRepository = Depends(get_supplier_repository)
) -> ListSuppliersUseCase:
    return ListSuppliersUseCase(repository)

def get_deactivate_supplier_use_case(
    repository: SupplierRepository = Depends(get_supplier_repository)
) -> DeactivateSupplierUseCase:
    return DeactivateSupplierUseCase(repository)

def get_activate_supplier_use_case(
    repository: SupplierRepository = Depends(get_supplier_repository)
) -> ActivateSupplierUseCase:
    return ActivateSupplierUseCase(repository)
