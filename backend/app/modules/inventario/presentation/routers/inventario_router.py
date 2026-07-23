from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.inventario.application.use_cases import (
    RegistrarMovimientoUseCase,
    RegistrarMovimientoCommand,
    RegistrarMermaUseCase,
    RegistrarMermaCommand,
    RegistrarAjusteUseCase,
    RegistrarAjusteCommand,
    ObtenerStockProductoUseCase,
    ListarMovimientosUseCase
)
from app.modules.inventario.presentation.dependencies.inventario_dependencies import (
    get_registrar_movimiento_use_case,
    get_registrar_merma_use_case,
    get_registrar_ajuste_use_case,
    get_obtener_stock_producto_use_case,
    get_listar_movimientos_use_case
)
from app.modules.inventario.presentation.dto import (
    RegistrarMovimientoRequest,
    RegistrarMermaRequest,
    RegistrarAjusteRequest,
    MovimientoInventarioResponse,
    StockResponse
)

router = APIRouter()

@router.post(
    "/movimientos",
    response_model=ApiResponse[MovimientoInventarioResponse],
    status_code=status.HTTP_201_CREATED,
)
def registrar_movimiento(
    request: RegistrarMovimientoRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: RegistrarMovimientoUseCase = Depends(get_registrar_movimiento_use_case)
) -> ApiResponse[MovimientoInventarioResponse]:
    """
    Registra un movimiento ordinario de entrada o salida física de inventario.
    """
    command = RegistrarMovimientoCommand(
        company_id=company_id,
        product_id=request.product_id,
        type=request.type,
        concept=request.concept,
        quantity=request.quantity,
        created_by=request.created_by,
        origin_document_id=request.origin_document_id,
        notes=request.notes
    )

    mov_ent = use_case.execute(command)
    response_dto = MovimientoInventarioResponse.model_validate(mov_ent)

    return ApiResponse(
        success=True,
        message="Movimiento de inventario registrado correctamente.",
        data=response_dto
    )


@router.post(
    "/mermas",
    response_model=ApiResponse[MovimientoInventarioResponse],
    status_code=status.HTTP_201_CREATED,
)
def registrar_merma(
    request: RegistrarMermaRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: RegistrarMermaUseCase = Depends(get_registrar_merma_use_case)
) -> ApiResponse[MovimientoInventarioResponse]:
    """
    Registra la pérdida física (merma) de unidades de un producto con justificación.
    """
    command = RegistrarMermaCommand(
        company_id=company_id,
        product_id=request.product_id,
        quantity=request.quantity,
        reason=request.reason,
        created_by=request.created_by,
        description=request.description
    )

    mov_ent = use_case.execute(command)
    response_dto = MovimientoInventarioResponse.model_validate(mov_ent)

    return ApiResponse(
        success=True,
        message="Merma de inventario registrada correctamente.",
        data=response_dto
    )


@router.post(
    "/ajustes",
    response_model=ApiResponse[MovimientoInventarioResponse],
    status_code=status.HTTP_201_CREATED,
)
def registrar_ajuste(
    request: RegistrarAjusteRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: RegistrarAjusteUseCase = Depends(get_registrar_ajuste_use_case)
) -> ApiResponse[MovimientoInventarioResponse]:
    """
    Registra una corrección física (ajuste) tras una auditoría de conteo de inventario.
    """
    command = RegistrarAjusteCommand(
        company_id=company_id,
        product_id=request.product_id,
        physical_quantity=request.physical_quantity,
        supervisor_id=request.supervisor_id,
        notes=request.notes
    )

    mov_ent = use_case.execute(command)
    response_dto = MovimientoInventarioResponse.model_validate(mov_ent)

    return ApiResponse(
        success=True,
        message="Ajuste de inventario registrado correctamente.",
        data=response_dto
    )


@router.get(
    "/productos/{product_id}/stock",
    response_model=ApiResponse[StockResponse],
    status_code=status.HTTP_200_OK,
)
def obtener_stock(
    product_id: UUID,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: ObtenerStockProductoUseCase = Depends(get_obtener_stock_producto_use_case)
) -> ApiResponse[StockResponse]:
    """
    Consulta la existencia neta disponible actual de un producto.
    """
    stock_value = use_case.execute(company_id=company_id, product_id=product_id)
    response_dto = StockResponse(product_id=product_id, stock=stock_value)

    return ApiResponse(
        success=True,
        message="Stock del producto obtenido correctamente.",
        data=response_dto
    )


@router.get(
    "/movimientos",
    response_model=ApiResponse[list[MovimientoInventarioResponse]],
    status_code=status.HTTP_200_OK,
)
def listar_movimientos(
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    product_id: UUID | None = Query(None, description="Optional product filter"),
    type: str | None = Query(None, description="Optional type filter (ENTRADA, SALIDA)"),
    concept: str | None = Query(None, description="Optional concept filter"),
    created_by: UUID | None = Query(None, description="Optional user filter"),
    start_date: datetime | None = Query(None, description="Optional start datetime filter"),
    end_date: datetime | None = Query(None, description="Optional end datetime filter"),
    use_case: ListarMovimientosUseCase = Depends(get_listar_movimientos_use_case)
) -> ApiResponse[list[MovimientoInventarioResponse]]:
    """
    Consulta el historial de movimientos físicos (Kardex) aplicando filtros y tenant.
    """
    filters = {
        "product_id": product_id,
        "type": type,
        "concept": concept,
        "created_by": created_by,
        "start_date": start_date,
        "end_date": end_date
    }

    movimientos = use_case.execute(company_id=company_id, filters=filters)
    response_dtos = [MovimientoInventarioResponse.model_validate(m) for m in movimientos]

    return ApiResponse(
        success=True,
        message="Historial de movimientos obtenido correctamente.",
        data=response_dtos
    )
