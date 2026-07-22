from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.product.domain.repositories.product_repository import ProductRepository
from app.modules.product.data.repositories.product_repository_impl import ProductRepositoryImpl
from app.modules.product.application.use_cases import (
    CreateProductUseCase,
    UpdateProductUseCase,
    DeactivateProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
)

def get_product_repository(db: Session = Depends(get_db)) -> ProductRepository:
    """FastAPI dependency to retrieve the concrete implementation of ProductRepository."""
    return ProductRepositoryImpl(db)

def get_create_product_use_case(
    repository: ProductRepository = Depends(get_product_repository)
) -> CreateProductUseCase:
    return CreateProductUseCase(repository)

def get_update_product_use_case(
    repository: ProductRepository = Depends(get_product_repository)
) -> UpdateProductUseCase:
    return UpdateProductUseCase(repository)

def get_deactivate_product_use_case(
    repository: ProductRepository = Depends(get_product_repository)
) -> DeactivateProductUseCase:
    return DeactivateProductUseCase(repository)

def get_product_use_case(
    repository: ProductRepository = Depends(get_product_repository)
) -> GetProductUseCase:
    return GetProductUseCase(repository)

def get_list_products_use_case(
    repository: ProductRepository = Depends(get_product_repository)
) -> ListProductsUseCase:
    return ListProductsUseCase(repository)
