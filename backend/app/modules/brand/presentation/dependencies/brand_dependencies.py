from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.brand.domain.repositories.brand_repository import BrandRepository
from app.modules.brand.data.repositories.brand_repository_impl import BrandRepositoryImpl
from app.modules.brand.application.use_cases import (
    CreateBrandUseCase,
    UpdateBrandUseCase,
    GetBrandByIdUseCase,
    ListBrandsUseCase,
    DeactivateBrandUseCase,
    ActivateBrandUseCase,
    DeleteBrandUseCase,
)

def get_brand_repository(db: Session = Depends(get_db)) -> BrandRepository:
    """FastAPI dependency to retrieve the concrete implementation of BrandRepository."""
    return BrandRepositoryImpl(db)

def get_create_brand_use_case(
    repository: BrandRepository = Depends(get_brand_repository)
) -> CreateBrandUseCase:
    return CreateBrandUseCase(repository)

def get_update_brand_use_case(
    repository: BrandRepository = Depends(get_brand_repository)
) -> UpdateBrandUseCase:
    return UpdateBrandUseCase(repository)

def get_get_brand_by_id_use_case(
    repository: BrandRepository = Depends(get_brand_repository)
) -> GetBrandByIdUseCase:
    return GetBrandByIdUseCase(repository)

def get_list_brands_use_case(
    repository: BrandRepository = Depends(get_brand_repository)
) -> ListBrandsUseCase:
    return ListBrandsUseCase(repository)

def get_deactivate_brand_use_case(
    repository: BrandRepository = Depends(get_brand_repository)
) -> DeactivateBrandUseCase:
    return DeactivateBrandUseCase(repository)

def get_activate_brand_use_case(
    repository: BrandRepository = Depends(get_brand_repository)
) -> ActivateBrandUseCase:
    return ActivateBrandUseCase(repository)

def get_delete_brand_use_case(
    repository: BrandRepository = Depends(get_brand_repository)
) -> DeleteBrandUseCase:
    return DeleteBrandUseCase(repository)
