from uuid import UUID
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.product.presentation.dependencies.product_dependencies import (
    get_create_product_use_case,
    get_update_product_use_case,
    get_deactivate_product_use_case,
    get_product_use_case,
    get_list_products_use_case,
)
from app.modules.product.presentation.dto import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
)
from app.modules.product.application.use_cases import (
    CreateProductUseCase,
    CreateProductCommand,
    UpdateProductUseCase,
    DeactivateProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
)

router = APIRouter()

@router.post(
    "/",
    response_model=ApiResponse[ProductResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    request: CreateProductRequest,
    use_case: CreateProductUseCase = Depends(get_create_product_use_case),
) -> ApiResponse[ProductResponse]:
    """
    Registrar un nuevo producto en el catálogo.
    """
    # Router only maps parameters into a Command DTO, decoupling from domain instantiation
    command = CreateProductCommand(
        company_id=request.company_id,
        internal_code=request.internal_code,
        barcode=request.barcode,
        name=request.name,
        description=request.description,
        category_id=request.category_id,
        brand_id=request.brand_id,
        unit_id=request.unit_id,
        cost=request.cost,
        price=request.price,
        tax_rate=request.tax_rate,
        controls_stock=request.controls_stock,
        allows_decimal=request.allows_decimal,
        is_perishable=request.is_perishable,
        minimum_stock=request.minimum_stock,
        status=request.status,
    )

    created_product = use_case.execute(command)
    response_data = ProductResponse.model_validate(created_product)

    return ApiResponse(
        success=True,
        message="Producto creado correctamente.",
        data=response_data,
    )

@router.get(
    "/",
    response_model=ApiResponse[list[ProductResponse]],
    status_code=status.HTTP_200_OK,
)
def list_products(
    company_id: UUID = Query(..., description="ID de la empresa (tenant) obligatoria"),
    category_id: UUID | None = Query(None, description="Filtrar por categoría"),
    brand_id: UUID | None = Query(None, description="Filtrar por marca"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (ACTIVO/INACTIVO)"),
    search: str | None = Query(None, description="Buscar por nombre, código interno o código de barras"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de paginación"),
    offset: int = Query(0, ge=0, description="Offset de paginación"),
    use_case: ListProductsUseCase = Depends(get_list_products_use_case),
) -> ApiResponse[list[ProductResponse]]:
    """
    Listar y buscar productos con filtros avanzados y paginación obligatoria por empresa.
    """
    products = use_case.execute(
        company_id=company_id,
        category_id=category_id,
        brand_id=brand_id,
        status=status_filter,
        search=search,
        limit=limit,
        offset=offset,
    )

    response_data = [ProductResponse.model_validate(p) for p in products]

    return ApiResponse(
        success=True,
        message="Productos obtenidos correctamente.",
        data=response_data,
    )

@router.get(
    "/{product_id}",
    response_model=ApiResponse[ProductResponse],
    status_code=status.HTTP_200_OK,
)
def get_product(
    product_id: UUID,
    use_case: GetProductUseCase = Depends(get_product_use_case),
) -> ApiResponse[ProductResponse]:
    """
    Obtener los detalles de un producto por su UUID.
    """
    product = use_case.execute(product_id)
    response_data = ProductResponse.model_validate(product)

    return ApiResponse(
        success=True,
        message="Producto obtenido correctamente.",
        data=response_data,
    )

@router.put(
    "/{product_id}",
    response_model=ApiResponse[ProductResponse],
    status_code=status.HTTP_200_OK,
)
def update_product(
    product_id: UUID,
    request: UpdateProductRequest,
    use_case: UpdateProductUseCase = Depends(get_update_product_use_case),
) -> ApiResponse[ProductResponse]:
    """
    Actualizar datos editables de un producto existente.
    """
    updated_product = use_case.execute(
        product_id=product_id,
        updates=request.model_dump(exclude_unset=True),
    )
    response_data = ProductResponse.model_validate(updated_product)

    return ApiResponse(
        success=True,
        message="Producto actualizado correctamente.",
        data=response_data,
    )

@router.delete(
    "/{product_id}",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def deactivate_product(
    product_id: UUID,
    use_case: DeactivateProductUseCase = Depends(get_deactivate_product_use_case),
) -> ApiResponse[bool]:
    """
    Inactivar un producto del catálogo (soft-delete).
    """
    success = use_case.execute(product_id)

    return ApiResponse(
        success=success,
        message="Producto inactivado correctamente." if success else "No se pudo inactivar el producto.",
        data=success,
    )
