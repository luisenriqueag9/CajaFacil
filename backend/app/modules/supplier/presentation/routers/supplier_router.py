import uuid
from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.supplier.domain.entities.supplier import Supplier
from app.modules.supplier.presentation.dependencies.supplier_dependencies import (
    get_create_supplier_use_case,
    get_update_supplier_use_case,
    get_get_supplier_by_id_use_case,
    get_list_suppliers_use_case,
    get_deactivate_supplier_use_case,
    get_activate_supplier_use_case,
)
from app.modules.supplier.presentation.dto import (
    SupplierCreateRequest,
    SupplierUpdateRequest,
    SupplierResponse,
)
from app.modules.supplier.application.use_cases import (
    CreateSupplierUseCase,
    UpdateSupplierUseCase,
    GetSupplierByIdUseCase,
    ListSuppliersUseCase,
    DeactivateSupplierUseCase,
    ActivateSupplierUseCase,
)

router = APIRouter()

@router.post(
    "/",
    response_model=ApiResponse[SupplierResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_supplier(
    request: SupplierCreateRequest,
    use_case: CreateSupplierUseCase = Depends(get_create_supplier_use_case),
) -> ApiResponse[SupplierResponse]:
    """
    Registrar un nuevo proveedor en la empresa.
    """
    supplier_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # Iniciar la entidad de dominio usando la factoría y pasarla al caso de uso
    supplier_entity = Supplier.register(
        id=supplier_id,
        company_id=request.company_id,
        name=request.name,
        tax_id=request.tax_id,
        contact_name=request.contact_name,
        phone=request.phone,
        email=request.email,
        created_at=now,
        updated_at=now,
    )

    created_supplier = use_case.execute(supplier_entity)
    supplier_response = SupplierResponse.model_validate(created_supplier)

    return ApiResponse(
        success=True,
        message="Proveedor creado correctamente.",
        data=supplier_response,
    )

@router.get(
    "/",
    response_model=ApiResponse[list[SupplierResponse]],
    status_code=status.HTTP_200_OK,
)
def list_suppliers(
    company_id: UUID = Query(..., description="ID de la empresa obligatoria para listar sus proveedores"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (ACTIVO/INACTIVO)"),
    use_case: ListSuppliersUseCase = Depends(get_list_suppliers_use_case),
) -> ApiResponse[list[SupplierResponse]]:
    """
    Obtener todos los proveedores de una empresa.
    """
    suppliers = use_case.execute(company_id=company_id, status=status_filter)
    supplier_responses = [SupplierResponse.model_validate(s) for s in suppliers]

    return ApiResponse(
        success=True,
        message="Proveedores obtenidos correctamente.",
        data=supplier_responses,
    )

@router.get(
    "/{supplier_id}",
    response_model=ApiResponse[SupplierResponse],
    status_code=status.HTTP_200_OK,
)
def get_supplier_by_id(
    supplier_id: UUID,
    use_case: GetSupplierByIdUseCase = Depends(get_get_supplier_by_id_use_case),
) -> ApiResponse[SupplierResponse]:
    """
    Obtener los detalles de un proveedor por su UUID.
    """
    supplier = use_case.execute(supplier_id)
    supplier_response = SupplierResponse.model_validate(supplier)

    return ApiResponse(
        success=True,
        message="Proveedor obtenido correctamente.",
        data=supplier_response,
    )

@router.put(
    "/{supplier_id}",
    response_model=ApiResponse[SupplierResponse],
    status_code=status.HTTP_200_OK,
)
def update_supplier(
    supplier_id: UUID,
    request: SupplierUpdateRequest,
    use_case: UpdateSupplierUseCase = Depends(get_update_supplier_use_case),
) -> ApiResponse[SupplierResponse]:
    """
    Actualizar datos editables y de contacto de un proveedor.
    """
    updated_supplier = use_case.execute(
        supplier_id=supplier_id,
        updates=request.model_dump(exclude_unset=True),
    )
    supplier_response = SupplierResponse.model_validate(updated_supplier)

    return ApiResponse(
        success=True,
        message="Proveedor actualizado correctamente.",
        data=supplier_response,
    )

@router.patch(
    "/{supplier_id}/deactivate",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def deactivate_supplier(
    supplier_id: UUID,
    use_case: DeactivateSupplierUseCase = Depends(get_deactivate_supplier_use_case),
) -> ApiResponse[bool]:
    """
    Desactivar administrativamente un proveedor (Soft Delete).
    """
    success = use_case.execute(supplier_id)
    return ApiResponse(
        success=success,
        message="Proveedor desactivado correctamente.",
        data=success,
    )

@router.patch(
    "/{supplier_id}/activate",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def activate_supplier(
    supplier_id: UUID,
    use_case: ActivateSupplierUseCase = Depends(get_activate_supplier_use_case),
) -> ApiResponse[bool]:
    """
    Activar administrativamente un proveedor.
    """
    success = use_case.execute(supplier_id)
    return ApiResponse(
        success=success,
        message="Proveedor activado correctamente.",
        data=success,
    )
