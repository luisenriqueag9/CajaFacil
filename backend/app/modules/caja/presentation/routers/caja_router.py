from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.caja.application.use_cases import (
    AbrirCajaUseCase,
    AbrirCajaCommand,
    RegistrarMovimientoCajaUseCase,
    RegistrarMovimientoCajaCommand,
    RegistrarArqueoCajaUseCase,
    RegistrarArqueoCajaCommand,
    CerrarCajaUseCase,
    CerrarCajaCommand,
    ObtenerSaldoCajaUseCase,
    ObtenerCajaActivaUseCase
)
from app.modules.caja.presentation.dependencies.caja_dependencies import (
    get_abrir_caja_use_case,
    get_registrar_movimiento_use_case,
    get_registrar_arqueo_use_case,
    get_cerrar_caja_use_case,
    get_obtener_saldo_use_case,
    get_obtener_caja_activa_use_case
)
from app.modules.caja.presentation.dto import (
    AbrirCajaRequest,
    RegistrarMovimientoCajaRequest,
    RegistrarArqueoCajaRequest,
    CerrarCajaRequest,
    CajaResponse,
    MovimientoCajaResponse,
    ArqueoCajaResponse,
    SaldoBreakdownResponse
)

router = APIRouter()

@router.post(
    "/",
    response_model=ApiResponse[CajaResponse],
    status_code=status.HTTP_201_CREATED,
)
def abrir_caja(
    request: AbrirCajaRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: AbrirCajaUseCase = Depends(get_abrir_caja_use_case)
) -> ApiResponse[CajaResponse]:
    """
    Inicia una nueva sesión/turno de caja declarando un fondo de dinero inicial.
    """
    command = AbrirCajaCommand(
        company_id=company_id,
        user_id=request.user_id,
        opening_balance=request.opening_balance
    )

    caja_ent = use_case.execute(command)
    response_dto = CajaResponse.model_validate(caja_ent)

    return ApiResponse(
        success=True,
        message="Sesión de caja abierta correctamente.",
        data=response_dto
    )


@router.post(
    "/{caja_id}/movimientos",
    response_model=ApiResponse[MovimientoCajaResponse],
    status_code=status.HTTP_201_CREATED,
)
def registrar_movimiento(
    caja_id: UUID,
    request: RegistrarMovimientoCajaRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: RegistrarMovimientoCajaUseCase = Depends(get_registrar_movimiento_use_case)
) -> ApiResponse[MovimientoCajaResponse]:
    """
    Registra una transacción individual de dinero (ingreso/egreso) en una sesión de caja abierta.
    """
    command = RegistrarMovimientoCajaCommand(
        company_id=company_id,
        caja_id=caja_id,
        type=request.type,
        amount=request.amount,
        payment_method=request.payment_method,
        concept=request.concept,
        origin_document_id=request.origin_document_id
    )

    mov_ent = use_case.execute(command)
    response_dto = MovimientoCajaResponse.model_validate(mov_ent)

    return ApiResponse(
        success=True,
        message="Movimiento de caja registrado correctamente.",
        data=response_dto
    )


@router.post(
    "/{caja_id}/arqueos",
    response_model=ApiResponse[ArqueoCajaResponse],
    status_code=status.HTTP_201_CREATED,
)
def registrar_arqueo(
    caja_id: UUID,
    request: RegistrarArqueoCajaRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: RegistrarArqueoCajaUseCase = Depends(get_registrar_arqueo_use_case)
) -> ApiResponse[ArqueoCajaResponse]:
    """
    Ejecuta un cuadre intermedio contando físicamente el dinero en el cajón y calculando discrepancias.
    """
    command = RegistrarArqueoCajaCommand(
        company_id=company_id,
        caja_id=caja_id,
        physical_amount=request.physical_amount,
        supervisor_id=request.supervisor_id
    )

    arq_ent = use_case.execute(command)
    response_dto = ArqueoCajaResponse.model_validate(arq_ent)

    return ApiResponse(
        success=True,
        message="Arqueo de caja registrado correctamente.",
        data=response_dto
    )


@router.post(
    "/{caja_id}/cerrar",
    response_model=ApiResponse[CajaResponse],
    status_code=status.HTTP_200_OK,
)
def cerrar_caja(
    caja_id: UUID,
    request: CerrarCajaRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: CerrarCajaUseCase = Depends(get_cerrar_caja_use_case)
) -> ApiResponse[CajaResponse]:
    """
    Finaliza el turno de caja de un cajero registrando su arqueo de cierre e inhabilitando más cobros.
    """
    command = CerrarCajaCommand(
        company_id=company_id,
        caja_id=caja_id,
        physical_amount=request.physical_amount,
        supervisor_id=request.supervisor_id
    )

    caja_ent = use_case.execute(command)
    response_dto = CajaResponse.model_validate(caja_ent)

    return ApiResponse(
        success=True,
        message="Sesión de caja cerrada correctamente.",
        data=response_dto
    )


@router.get(
    "/{caja_id}/saldo",
    response_model=ApiResponse[SaldoBreakdownResponse],
    status_code=status.HTTP_200_OK,
)
def obtener_saldo(
    caja_id: UUID,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: ObtenerSaldoCajaUseCase = Depends(get_obtener_saldo_use_case)
) -> ApiResponse[SaldoBreakdownResponse]:
    """
    Muestra la sumatoria esperada de dinero en el sistema con desglose por medio de pago.
    """
    breakdown = use_case.execute(company_id=company_id, caja_id=caja_id)
    response_dto = SaldoBreakdownResponse(**breakdown)

    return ApiResponse(
        success=True,
        message="Saldo de caja obtenido correctamente.",
        data=response_dto
    )


@router.get(
    "/activa",
    response_model=ApiResponse[CajaResponse | None],
    status_code=status.HTTP_200_OK,
)
def obtener_caja_activa(
    user_id: UUID = Query(..., description="Cashier User UUID"),
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: ObtenerCajaActivaUseCase = Depends(get_obtener_caja_activa_use_case)
) -> ApiResponse[CajaResponse | None]:
    """
    Obtiene la sesión de caja activa abierta actualmente para un cajero.
    Retorna nulo si no tiene sesión abierta.
    """
    caja_ent = use_case.execute(company_id=company_id, user_id=user_id)
    response_dto = CajaResponse.model_validate(caja_ent) if caja_ent else None

    return ApiResponse(
        success=True,
        message="Caja activa obtenida correctamente.",
        data=response_dto
    )
