import uuid
from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.category.domain.entities.category import Category
from app.modules.category.presentation.dependencies.category_dependencies import (
    get_create_category_use_case,
    get_update_category_use_case,
    get_get_category_by_id_use_case,
    get_list_categories_use_case,
    get_deactivate_category_use_case,
    get_activate_category_use_case,
    get_get_default_category_use_case,
)
from app.modules.category.presentation.dto import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryResponse,
)
from app.modules.category.application.use_cases import (
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    GetCategoryByIdUseCase,
    ListCategoriesUseCase,
    DeactivateCategoryUseCase,
    ActivateCategoryUseCase,
    GetDefaultCategoryUseCase,
)

router = APIRouter()

@router.post(
    "/",
    response_model=ApiResponse[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    request: CategoryCreateRequest,
    use_case: CreateCategoryUseCase = Depends(get_create_category_use_case),
) -> ApiResponse[CategoryResponse]:
    """
    Registrar una nueva categoría personalizada.
    """
    category_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # Iniciar la entidad de dominio y pasarla al caso de uso
    category_entity = Category.register(
        id=category_id,
        company_id=request.company_id,
        name=request.name,
        created_at=now,
        updated_at=now,
    )

    created_category = use_case.execute(category_entity)
    category_response = CategoryResponse.model_validate(created_category)

    return ApiResponse(
        success=True,
        message="Categoría creada correctamente.",
        data=category_response,
    )

@router.get(
    "/",
    response_model=ApiResponse[list[CategoryResponse]],
    status_code=status.HTTP_200_OK,
)
def list_categories(
    company_id: UUID = Query(..., description="ID de la empresa obligatoria para listar sus categorías"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (ACTIVO/INACTIVO)"),
    use_case: ListCategoriesUseCase = Depends(get_list_categories_use_case),
) -> ApiResponse[list[CategoryResponse]]:
    """
    Obtener todas las categorías de una empresa.
    """
    categories = use_case.execute(company_id=company_id, status=status_filter)
    category_responses = [CategoryResponse.model_validate(c) for c in categories]

    return ApiResponse(
        success=True,
        message="Categorías obtenidas correctamente.",
        data=category_responses,
    )

@router.get(
    "/default",
    response_model=ApiResponse[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
def get_default_category(
    company_id: UUID = Query(..., description="ID de la empresa para obtener su categoría por defecto"),
    use_case: GetDefaultCategoryUseCase = Depends(get_get_default_category_use_case),
) -> ApiResponse[CategoryResponse]:
    """
    Obtener la categoría por defecto ('Sin Clasificar') de la empresa.
    """
    category = use_case.execute(company_id)
    category_response = CategoryResponse.model_validate(category)

    return ApiResponse(
        success=True,
        message="Categoría por defecto obtenida correctamente.",
        data=category_response,
    )

@router.get(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
def get_category_by_id(
    category_id: UUID,
    use_case: GetCategoryByIdUseCase = Depends(get_get_category_by_id_use_case),
) -> ApiResponse[CategoryResponse]:
    """
    Obtener los detalles de una categoría por su UUID.
    """
    category = use_case.execute(category_id)
    category_response = CategoryResponse.model_validate(category)

    return ApiResponse(
        success=True,
        message="Categoría obtenida correctamente.",
        data=category_response,
    )

@router.put(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
def update_category(
    category_id: UUID,
    request: CategoryUpdateRequest,
    use_case: UpdateCategoryUseCase = Depends(get_update_category_use_case),
) -> ApiResponse[CategoryResponse]:
    """
    Actualizar el nombre o estado de una categoría.
    """
    updated_category = use_case.execute(
        category_id=category_id,
        updates=request.model_dump(exclude_unset=True),
    )
    category_response = CategoryResponse.model_validate(updated_category)

    return ApiResponse(
        success=True,
        message="Categoría actualizada correctamente.",
        data=category_response,
    )

@router.patch(
    "/{category_id}/deactivate",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def deactivate_category(
    category_id: UUID,
    use_case: DeactivateCategoryUseCase = Depends(get_deactivate_category_use_case),
) -> ApiResponse[bool]:
    """
    Desactivar administrativamente una categoría (Soft Delete).
    """
    success = use_case.execute(category_id)
    return ApiResponse(
        success=success,
        message="Categoría desactivada correctamente.",
        data=success,
    )

@router.patch(
    "/{category_id}/activate",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def activate_category(
    category_id: UUID,
    use_case: ActivateCategoryUseCase = Depends(get_activate_category_use_case),
) -> ApiResponse[bool]:
    """
    Activar administrativamente una categoría.
    """
    success = use_case.execute(category_id)
    return ApiResponse(
        success=success,
        message="Categoría activada correctamente.",
        data=success,
    )
