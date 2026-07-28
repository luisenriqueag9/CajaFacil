from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from typing import List

from app.common.responses import APIResponse
from app.modules.compra.presentation.api.schemas.compra_schema import (
    RegistrarCompraRequest,
    AnularCompraRequest,
    RegistrarDevolucionProveedorRequest,
    CompraResponse,
)
from app.modules.compra.presentation.api.dependencies.compra_dependencies import (
    get_registrar_compra_use_case,
    get_anular_compra_use_case,
    get_obtener_compra_use_case,
    get_listar_compras_use_case,
    get_registrar_devolucion_use_case,
)
from app.modules.compra.application.use_cases import (
    RegistrarCompraUseCase,
    AnularCompraUseCase,
    ObtenerCompraUseCase,
    ListarComprasUseCase,
    RegistrarDevolucionProveedorUseCase,
)
from app.modules.compra.application.commands import (
    RegistrarCompraCommand,
    DetalleCompraCommand,
    AnularCompraCommand,
    RegistrarDevolucionProveedorCommand,
    DetalleDevolucionCommand,
)
from app.modules.compra.application.queries import (
    ObtenerCompraQuery,
    ListarComprasQuery,
)

router = APIRouter()

@router.post(
    "",
    response_model=APIResponse[CompraResponse],
    status_code=status.HTTP_201_CREATED,
)
def register_purchase(
    request: RegistrarCompraRequest,
    use_case: RegistrarCompraUseCase = Depends(get_registrar_compra_use_case),
) -> APIResponse[CompraResponse]:
    """
    Registrar y confirmar una nueva compra de mercaderia.
    """
    items_command = [
        DetalleCompraCommand(
            product_id=item.product_id,
            quantity=item.quantity,
            unit_cost=item.unit_cost
        )
        for item in request.items
    ]
    
    command = RegistrarCompraCommand(
        company_id=request.company_id,
        supplier_id=request.supplier_id,
        invoice_number=request.invoice_number.strip(),
        payment_condition=request.payment_condition.strip(),
        issue_date=request.issue_date,
        items=items_command
    )

    created_purchase = use_case.execute(command)
    purchase_response = CompraResponse.model_validate(created_purchase)

    return APIResponse(
        success=True,
        message="Compra registrada correctamente.",
        data=purchase_response,
    )

@router.get(
    "",
    response_model=APIResponse[List[CompraResponse]],
    status_code=status.HTTP_200_OK,
)
def list_purchases(
    company_id: UUID = Query(..., description="ID de la empresa obligatoria para listar sus compras"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (BORRADOR/REGISTRADA/ANULADA)"),
    supplier_id: UUID | None = Query(None, description="Filtrar por proveedor especifico"),
    use_case: ListarComprasUseCase = Depends(get_listar_compras_use_case),
) -> APIResponse[List[CompraResponse]]:
    """
    Obtener la lista de compras del negocio filtrada por filtros.
    """
    query = ListarComprasQuery(
        company_id=company_id,
        status=status_filter,
        supplier_id=supplier_id
    )
    purchases = use_case.execute(query)
    purchase_responses = [CompraResponse.model_validate(p) for p in purchases]

    return APIResponse(
        success=True,
        message="Compras obtenidas correctamente.",
        data=purchase_responses,
    )

@router.get(
    "/{purchase_id}",
    response_model=APIResponse[CompraResponse],
    status_code=status.HTTP_200_OK,
)
def get_purchase_by_id(
    purchase_id: UUID,
    use_case: ObtenerCompraUseCase = Depends(get_obtener_compra_use_case),
) -> APIResponse[CompraResponse]:
    """
    Obtener los detalles de una compra por su UUID.
    """
    query = ObtenerCompraQuery(purchase_id=purchase_id)
    purchase = use_case.execute(query)
    purchase_response = CompraResponse.model_validate(purchase)

    return APIResponse(
        success=True,
        message="Compra obtenida correctamente.",
        data=purchase_response,
    )

@router.post(
    "/{purchase_id}/anular",
    response_model=APIResponse[CompraResponse],
    status_code=status.HTTP_200_OK,
)
def annul_purchase(
    purchase_id: UUID,
    request: AnularCompraRequest,
    use_case: AnularCompraUseCase = Depends(get_anular_compra_use_case),
) -> APIResponse[CompraResponse]:
    """
    Anular comercialmente una compra registrada.
    """
    command = AnularCompraCommand(
        purchase_id=purchase_id,
        voided_by=request.voided_by,
        void_reason=request.void_reason or "Anulacion solicitada por API"
    )
    annulled_purchase = use_case.execute(command)
    purchase_response = CompraResponse.model_validate(annulled_purchase)
    
    return APIResponse(
        success=True,
        message="Compra anulada correctamente.",
        data=purchase_response,
    )

@router.post(
    "/{purchase_id}/devolucion",
    response_model=APIResponse[CompraResponse],
    status_code=status.HTTP_200_OK,
)
def return_purchase(
    purchase_id: UUID,
    request: RegistrarDevolucionProveedorRequest,
    use_case: RegistrarDevolucionProveedorUseCase = Depends(get_registrar_devolucion_use_case),
) -> APIResponse[CompraResponse]:
    """
    Registrar la devolucion de mercaderias de una compra al proveedor.
    """
    items_command = [
        DetalleDevolucionCommand(
            product_id=item.product_id,
            quantity=item.quantity
        )
        for item in request.items
    ]
    command = RegistrarDevolucionProveedorCommand(
        purchase_id=purchase_id,
        items=items_command
    )
    updated_purchase = use_case.execute(command)
    purchase_response = CompraResponse.model_validate(updated_purchase)

    return APIResponse(
        success=True,
        message="Devolucion registrada correctamente.",
        data=purchase_response,
    )
