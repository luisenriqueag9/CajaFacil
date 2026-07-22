import uuid
from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.brand.domain.entities.brand import Brand
from app.modules.brand.presentation.dependencies.brand_dependencies import (
    get_create_brand_use_case,
    get_update_brand_use_case,
    get_get_brand_by_id_use_case,
    get_list_brands_use_case,
    get_deactivate_brand_use_case,
    get_activate_brand_use_case,
    get_delete_brand_use_case,
)
from app.modules.brand.presentation.dto import (
    BrandCreateRequest,
    BrandUpdateRequest,
    BrandResponse,
)
from app.modules.brand.application.use_cases import (
    CreateBrandUseCase,
    UpdateBrandUseCase,
    GetBrandByIdUseCase,
    ListBrandsUseCase,
    DeactivateBrandUseCase,
    ActivateBrandUseCase,
    DeleteBrandUseCase,
)

router = APIRouter()

@router.post(
    "/",
    response_model=ApiResponse[BrandResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_brand(
    request: BrandCreateRequest,
    use_case: CreateBrandUseCase = Depends(get_create_brand_use_case),
) -> ApiResponse[BrandResponse]:
    """
    Registrar una nueva marca en el catálogo.
    """
    brand_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    brand_entity = Brand(
        id=brand_id,
        company_id=request.company_id,
        name=request.name,
        status=request.status,
        created_at=now,
        updated_at=now,
    )

    created_brand = use_case.execute(brand_entity)
    brand_response = BrandResponse.model_validate(created_brand)

    return ApiResponse(
        success=True,
        message="Marca creada correctamente.",
        data=brand_response,
    )

@router.get(
    "/",
    response_model=ApiResponse[list[BrandResponse]],
    status_code=status.HTTP_200_OK,
)
def list_brands(
    company_id: UUID = Query(..., description="ID de la empresa obligatoria para listar sus marcas"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (ACTIVO/INACTIVO)"),
    use_case: ListBrandsUseCase = Depends(get_list_brands_use_case),
) -> ApiResponse[list[BrandResponse]]:
    """
    Obtener todas las marcas pertenecientes a una empresa.
    """
    brands = use_case.execute(company_id=company_id, status=status_filter)
    brand_responses = [BrandResponse.model_validate(b) for b in brands]

    return ApiResponse(
        success=True,
        message="Marcas obtenidas correctamente.",
        data=brand_responses,
    )

@router.get(
    "/{brand_id}",
    response_model=ApiResponse[BrandResponse],
    status_code=status.HTTP_200_OK,
)
def get_brand_by_id(
    brand_id: UUID,
    use_case: GetBrandByIdUseCase = Depends(get_get_brand_by_id_use_case),
) -> ApiResponse[BrandResponse]:
    """
    Obtener los detalles de una marca por su UUID.
    """
    brand = use_case.execute(brand_id)
    brand_response = BrandResponse.model_validate(brand)

    return ApiResponse(
        success=True,
        message="Marca obtenida correctamente.",
        data=brand_response,
    )

@router.put(
    "/{brand_id}",
    response_model=ApiResponse[BrandResponse],
    status_code=status.HTTP_200_OK,
)
def update_brand(
    brand_id: UUID,
    request: BrandUpdateRequest,
    use_case: UpdateBrandUseCase = Depends(get_update_brand_use_case),
) -> ApiResponse[BrandResponse]:
    """
    Actualizar datos editables de una marca existente.
    """
    updated_brand = use_case.execute(
        brand_id=brand_id,
        updates=request.model_dump(exclude_unset=True),
    )
    brand_response = BrandResponse.model_validate(updated_brand)

    return ApiResponse(
        success=True,
        message="Marca actualizada correctamente.",
        data=brand_response,
    )

@router.patch(
    "/{brand_id}/deactivate",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def deactivate_brand(
    brand_id: UUID,
    use_case: DeactivateBrandUseCase = Depends(get_deactivate_brand_use_case),
) -> ApiResponse[bool]:
    """
    Desactivar administrativamente una marca.
    """
    success = use_case.execute(brand_id)
    return ApiResponse(
        success=success,
        message="Marca desactivada correctamente.",
        data=success,
    )

@router.patch(
    "/{brand_id}/activate",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def activate_brand(
    brand_id: UUID,
    use_case: ActivateBrandUseCase = Depends(get_activate_brand_use_case),
) -> ApiResponse[bool]:
    """
    Activar administrativamente una marca.
    """
    success = use_case.execute(brand_id)
    return ApiResponse(
        success=success,
        message="Marca activada correctamente.",
        data=success,
    )

@router.delete(
    "/{brand_id}",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def delete_brand(
    brand_id: UUID,
    use_case: DeleteBrandUseCase = Depends(get_delete_brand_use_case),
) -> ApiResponse[bool]:
    """
    Eliminar físicamente una marca si no tiene productos asociados.
    """
    success = use_case.execute(brand_id)
    return ApiResponse(
        success=success,
        message="Marca eliminada correctamente.",
        data=success,
    )
