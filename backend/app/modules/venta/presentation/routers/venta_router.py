from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.venta.application.use_cases import (
    ConfirmarVentaUseCase,
    ConfirmarVentaCommand,
    DetalleVentaCommand,
    FormaPagoAceptadaCommand,
    AnularVentaUseCase,
    AnularVentaCommand,
    GetVentaByIdUseCase,
    ListSalesUseCase
)
from app.modules.venta.presentation.dependencies.venta_dependencies import (
    get_confirmar_venta_use_case,
    get_anular_venta_use_case,
    get_get_venta_by_id_use_case,
    get_list_sales_use_case
)
from app.modules.venta.presentation.dto import (
    ConfirmarVentaRequest,
    AnularVentaRequest,
    VentaResponse
)

router = APIRouter()

@router.post(
    "/",
    response_model=ApiResponse[VentaResponse],
    status_code=status.HTTP_201_CREATED,
)
def confirmar_venta(
    request: ConfirmarVentaRequest,
    use_case: ConfirmarVentaUseCase = Depends(get_confirmar_venta_use_case)
) -> ApiResponse[VentaResponse]:
    """
    Registra y confirma una transacción comercial (Venta) de forma atómica.
    """
    command = ConfirmarVentaCommand(
        company_id=request.company_id,
        box_id=request.box_id,
        user_id=request.user_id,
        client_id=request.client_id,
        invoice_number=request.invoice_number,
        subtotal=request.subtotal,
        discount=request.discount,
        tax=request.tax,
        total=request.total,
        details=[
            DetalleVentaCommand(
                product_id=d.product_id,
                quantity=d.quantity,
                unit_price=d.unit_price,
                discount=d.discount,
                tax_rate=d.tax_rate,
                tax_amount=d.tax_amount,
                subtotal=d.subtotal,
                total=d.total
            ) for d in request.details
        ],
        payments=[
            FormaPagoAceptadaCommand(
                payment_method=p.payment_method,
                amount=p.amount,
                transaction_reference=p.transaction_reference
            ) for p in request.payments
        ]
    )

    venta_ent = use_case.execute(command)
    response_dto = VentaResponse.model_validate(venta_ent)

    return ApiResponse(
        success=True,
        message="Venta confirmada correctamente.",
        data=response_dto
    )


@router.post(
    "/{venta_id}/anular",
    response_model=ApiResponse[VentaResponse],
    status_code=status.HTTP_200_OK,
)
def anular_venta(
    venta_id: UUID,
    request: AnularVentaRequest,
    use_case: AnularVentaUseCase = Depends(get_anular_venta_use_case)
) -> ApiResponse[VentaResponse]:
    """
    Anula comercialmente una venta confirmada y reversa de forma atómica sus efectos.
    """
    command = AnularVentaCommand(
        venta_id=venta_id,
        supervisor_id=request.supervisor_id,
        reason=request.reason
    )

    venta_ent = use_case.execute(command)
    response_dto = VentaResponse.model_validate(venta_ent)

    return ApiResponse(
        success=True,
        message="Venta anulada correctamente.",
        data=response_dto
    )


@router.get(
    "/{venta_id}",
    response_model=ApiResponse[VentaResponse],
    status_code=status.HTTP_200_OK,
)
def obtener_venta(
    venta_id: UUID,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: GetVentaByIdUseCase = Depends(get_get_venta_by_id_use_case)
) -> ApiResponse[VentaResponse]:
    """
    Obtiene los detalles completos de una venta por su identificador.
    """
    venta_ent = use_case.execute(company_id=company_id, venta_id=venta_id)
    response_dto = VentaResponse.model_validate(venta_ent)

    return ApiResponse(
        success=True,
        message="Venta obtenida correctamente.",
        data=response_dto
    )


@router.get(
    "/",
    response_model=ApiResponse[list[VentaResponse]],
    status_code=status.HTTP_200_OK,
)
def listar_ventas(
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    box_id: UUID | None = Query(None, description="Optional Box UUID filter"),
    user_id: UUID | None = Query(None, description="Optional Cajero UUID filter"),
    client_id: UUID | None = Query(None, description="Optional Client UUID filter"),
    status: str | None = Query(None, description="Optional Status filter (CONFIRMADA, ANULADA)"),
    start_date: datetime | None = Query(None, description="Optional start datetime filter"),
    end_date: datetime | None = Query(None, description="Optional end datetime filter"),
    use_case: ListSalesUseCase = Depends(get_list_sales_use_case)
) -> ApiResponse[list[VentaResponse]]:
    """
    Busca e historial de ventas aplicando aislamiento multi-tenant.
    """
    filters = {
        "box_id": box_id,
        "user_id": user_id,
        "client_id": client_id,
        "status": status,
        "start_date": start_date,
        "end_date": end_date
    }

    ventas = use_case.execute(company_id=company_id, filters=filters)
    response_dtos = [VentaResponse.model_validate(v) for v in ventas]

    return ApiResponse(
        success=True,
        message="Historial de ventas obtenido correctamente.",
        data=response_dtos
    )
