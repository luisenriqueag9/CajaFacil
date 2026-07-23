from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.category.domain.repositories.category_repository import CategoryRepository
from app.modules.category.data.repositories.category_repository_impl import CategoryRepositoryImpl
from app.modules.category.application.use_cases import (
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    GetCategoryByIdUseCase,
    ListCategoriesUseCase,
    DeactivateCategoryUseCase,
    ActivateCategoryUseCase,
    InitializeDefaultCategoryUseCase,
    GetDefaultCategoryUseCase,
)

def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    """FastAPI dependency to retrieve the concrete implementation of CategoryRepository."""
    return CategoryRepositoryImpl(db)

def get_create_category_use_case(
    repository: CategoryRepository = Depends(get_category_repository)
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(repository)

def get_update_category_use_case(
    repository: CategoryRepository = Depends(get_category_repository)
) -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase(repository)

def get_get_category_by_id_use_case(
    repository: CategoryRepository = Depends(get_category_repository)
) -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase(repository)

def get_list_categories_use_case(
    repository: CategoryRepository = Depends(get_category_repository)
) -> ListCategoriesUseCase:
    return ListCategoriesUseCase(repository)

def get_deactivate_category_use_case(
    repository: CategoryRepository = Depends(get_category_repository)
) -> DeactivateCategoryUseCase:
    return DeactivateCategoryUseCase(repository)

def get_activate_category_use_case(
    repository: CategoryRepository = Depends(get_category_repository)
) -> ActivateCategoryUseCase:
    return ActivateCategoryUseCase(repository)

def get_initialize_default_category_use_case(
    repository: CategoryRepository = Depends(get_category_repository)
) -> InitializeDefaultCategoryUseCase:
    return InitializeDefaultCategoryUseCase(repository)

def get_get_default_category_use_case(
    repository: CategoryRepository = Depends(get_category_repository)
) -> GetDefaultCategoryUseCase:
    return GetDefaultCategoryUseCase(repository)
