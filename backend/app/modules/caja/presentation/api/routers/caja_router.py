from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from typing import List

from app.common.responses import APIResponse
from app.modules.caja.presentation.api.schemas.caja_schema import (
    AbrirSesionRequest,
    RegistrarMovimientoRequest,
    RegistrarArqueoRequest,
    SesionResponse,
    MovimientoResponse,
    ArqueoResponse,
)
from app.modules.caja.presentation.dependencies.caja_dependencies import (
    get_abrir_sesion_use_case,
    get_cerrar_sesion_use_case,
    get_registrar_movimiento_use_case,
    get_registrar_arqueo_use_case,
    get_anular_movimiento_use_case,
    get_obtener_sesion_use_case,
    get_listar_sesiones_use_case,
)
from app.modules.caja.application.use_cases import (
    AbrirSesionUseCase,
    CerrarSesionUseCase,
    RegistrarMovimientoUseCase,
    RegistrarArqueoUseCase,
    AnularMovimientoUseCase,
    ObtenerSesionUseCase,
    ListarSesionesUseCase,
)
from app.modules.caja.application.commands import (
    AbrirSesionCommand,
    CerrarSesionCommand,
    RegistrarMovimientoCommand,
    RegistrarArqueoCommand,
    AnularMovimientoCommand,
)
from app.modules.caja.application.queries import (
    ObtenerSesionQuery,
    ListarSesionesQuery,
)

router = APIRouter()

@router.post(
    "/sesiones",
    response_model=APIResponse[SesionResponse],
    status_code=status.HTTP_201_CREATED,
)
def abrir_sesion(
    request: AbrirSesionRequest,
    use_case: AbrirSesionUseCase = Depends(get_abrir_sesion_use_case),
) -> APIResponse[SesionResponse]:
    """
    Inicia una nueva sesion/turno de caja declarando un fondo de dinero inicial.
    """
    command = AbrirSesionCommand(
        caja_id=request.caja_id,
        company_id=request.company_id,
        user_id=request.user_id,
        opening_balance=request.opening_balance
    )
    sesion = use_case.execute(command)
    response_dto = SesionResponse.model_validate(sesion)

    return APIResponse(
        success=True,
        message="Sesion de caja abierta correctamente.",
        data=response_dto
    )

@router.post(
    "/sesiones/{sesion_id}/movimientos",
    response_model=APIResponse[SesionResponse],
    status_code=status.HTTP_201_CREATED,
)
def registrar_movimiento(
    sesion_id: UUID,
    request: RegistrarMovimientoRequest,
    use_case: RegistrarMovimientoUseCase = Depends(get_registrar_movimiento_use_case),
) -> APIResponse[SesionResponse]:
    """
    Registra un ingreso o egreso en la sesion de caja.
    """
    command = RegistrarMovimientoCommand(
        sesion_id=sesion_id,
        type=request.type,
        amount=request.amount,
        payment_method=request.payment_method,
        concept=request.concept,
        origin_context=request.origin_context,
        origin_document_id=request.origin_document_id
    )
    sesion = use_case.execute(command)
    response_dto = SesionResponse.model_validate(sesion)

    return APIResponse(
        success=True,
        message="Movimiento de caja registrado correctamente.",
        data=response_dto
    )

@router.post(
    "/sesiones/{sesion_id}/arqueos",
    response_model=APIResponse[SesionResponse],
    status_code=status.HTTP_201_CREATED,
)
def registrar_arqueo(
    sesion_id: UUID,
    request: RegistrarArqueoRequest,
    use_case: RegistrarArqueoUseCase = Depends(get_registrar_arqueo_use_case),
) -> APIResponse[SesionResponse]:
    """
    Realiza una auditoria de arqueo sobre el dinero de la sesion.
    """
    command = RegistrarArqueoCommand(
        sesion_id=sesion_id,
        physical_amount=request.physical_amount,
        supervisor_id=request.supervisor_id
    )
    sesion = use_case.execute(command)
    response_dto = SesionResponse.model_validate(sesion)

    return APIResponse(
        success=True,
        message="Arqueo de caja registrado correctamente.",
        data=response_dto
    )

@router.post(
    "/sesiones/{sesion_id}/cerrar",
    response_model=APIResponse[SesionResponse],
    status_code=status.HTTP_200_OK,
)
def cerrar_sesion(
    sesion_id: UUID,
    use_case: CerrarSesionUseCase = Depends(get_cerrar_sesion_use_case),
) -> APIResponse[SesionResponse]:
    """
    Cierra definitivamente la sesion/turno.
    """
    command = CerrarSesionCommand(sesion_id=sesion_id)
    sesion = use_case.execute(command)
    response_dto = SesionResponse.model_validate(sesion)

    return APIResponse(
        success=True,
        message="Sesion de caja cerrada correctamente.",
        data=response_dto
    )

@router.post(
    "/sesiones/{sesion_id}/movimientos/{movimiento_id}/anular",
    response_model=APIResponse[SesionResponse],
    status_code=status.HTTP_200_OK,
)
def anular_movimiento(
    sesion_id: UUID,
    movimiento_id: UUID,
    use_case: AnularMovimientoUseCase = Depends(get_anular_movimiento_use_case),
) -> APIResponse[SesionResponse]:
    """
    Anula un movimiento mediante contramovimiento.
    """
    command = AnularMovimientoCommand(sesion_id=sesion_id, movimiento_id=movimiento_id)
    sesion = use_case.execute(command)
    response_dto = SesionResponse.model_validate(sesion)

    return APIResponse(
        success=True,
        message="Movimiento anulado correctamente.",
        data=response_dto
    )

@router.get(
    "/sesiones/{sesion_id}",
    response_model=APIResponse[SesionResponse],
    status_code=status.HTTP_200_OK,
)
def obtener_sesion(
    sesion_id: UUID,
    use_case: ObtenerSesionUseCase = Depends(get_obtener_sesion_use_case),
) -> APIResponse[SesionResponse]:
    """
    Obtiene los detalles completos de una sesion de caja.
    """
    query = ObtenerSesionQuery(sesion_id=sesion_id)
    sesion = use_case.execute(query)
    response_dto = SesionResponse.model_validate(sesion)

    return APIResponse(
        success=True,
        message="Sesion de caja obtenida correctamente.",
        data=response_dto
    )

@router.get(
    "/sesiones",
    response_model=APIResponse[List[SesionResponse]],
    status_code=status.HTTP_200_OK,
)
def listar_sesiones(
    company_id: UUID = Query(..., description="ID de la empresa para filtrar"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (ABIERTA/CERRADA)"),
    use_case: ListarSesionesUseCase = Depends(get_listar_sesiones_use_case),
) -> APIResponse[List[SesionResponse]]:
    """
    Lista las sesiones de caja de la empresa.
    """
    query = ListarSesionesQuery(company_id=company_id, status=status_filter)
    sesiones = use_case.execute(query)
    response_dto = [SesionResponse.model_validate(s) for s in sesiones]

    return APIResponse(
        success=True,
        message="Sesiones de caja obtenidas correctamente.",
        data=response_dto
    )
