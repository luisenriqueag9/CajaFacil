from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from typing import List

from app.common.responses import APIResponse
from app.modules.credito.presentation.api.schemas.credito_schema import (
    AbrirCuentaCreditoRequest,
    ActualizarLimiteCreditoRequest,
    CreditoResponse,
)
from app.modules.credito.presentation.api.dependencies.credito_dependencies import (
    get_abrir_cuenta_use_case,
    get_actualizar_limite_use_case,
    get_inactivar_cuenta_use_case,
    get_obtener_credito_use_case,
    get_listar_creditos_use_case,
)
from app.modules.credito.application.use_cases import (
    AbrirCuentaCreditoUseCase,
    ActualizarLimiteCreditoUseCase,
    InactivarCuentaCreditoUseCase,
    ObtenerCreditoUseCase,
    ListarCreditosUseCase,
)
from app.modules.credito.application.commands import (
    AbrirCuentaCreditoCommand,
    ActualizarLimiteCreditoCommand,
    InactivarCuentaCreditoCommand,
)
from app.modules.credito.application.queries import (
    ObtenerCreditoQuery,
    ListarCreditosQuery,
)

router = APIRouter()

@router.post(
    "",
    response_model=APIResponse[CreditoResponse],
    status_code=status.HTTP_201_CREATED,
)
def open_credit_account(
    request: AbrirCuentaCreditoRequest,
    use_case: AbrirCuentaCreditoUseCase = Depends(get_abrir_cuenta_use_case),
) -> APIResponse[CreditoResponse]:
    """
    Abrir una nueva cuenta de credito para un cliente.
    """
    command = AbrirCuentaCreditoCommand(
        company_id=request.company_id,
        client_id=request.client_id,
        credit_limit=request.credit_limit
    )
    created_credit = use_case.execute(command)
    response_data = CreditoResponse.model_validate(created_credit)

    return APIResponse(
        success=True,
        message="Cuenta de credito abierta correctamente.",
        data=response_data,
    )

@router.get(
    "",
    response_model=APIResponse[List[CreditoResponse]],
    status_code=status.HTTP_200_OK,
)
def list_credit_accounts(
    company_id: UUID = Query(..., description="ID de la empresa para filtrar"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (ACTIVO/SUSPENDIDO)"),
    use_case: ListarCreditosUseCase = Depends(get_listar_creditos_use_case),
) -> APIResponse[List[CreditoResponse]]:
    """
    Listar las cuentas de credito de la empresa.
    """
    query = ListarCreditosQuery(
        company_id=company_id,
        status=status_filter
    )
    credits = use_case.execute(query)
    response_data = [CreditoResponse.model_validate(c) for c in credits]

    return APIResponse(
        success=True,
        message="Cuentas de credito obtenidas correctamente.",
        data=response_data,
    )

@router.get(
    "/{credit_id}",
    response_model=APIResponse[CreditoResponse],
    status_code=status.HTTP_200_OK,
)
def get_credit_account_by_id(
    credit_id: UUID,
    use_case: ObtenerCreditoUseCase = Depends(get_obtener_credito_use_case),
) -> APIResponse[CreditoResponse]:
    """
    Obtener los detalles de una cuenta de credito por su UUID.
    """
    query = ObtenerCreditoQuery(credit_id=credit_id)
    credit = use_case.execute(query)
    response_data = CreditoResponse.model_validate(credit)

    return APIResponse(
        success=True,
        message="Cuenta de credito obtenida correctamente.",
        data=response_data,
    )

@router.put(
    "/{credit_id}/limite",
    response_model=APIResponse[CreditoResponse],
    status_code=status.HTTP_200_OK,
)
def update_credit_limit(
    credit_id: UUID,
    request: ActualizarLimiteCreditoRequest,
    use_case: ActualizarLimiteCreditoUseCase = Depends(get_actualizar_limite_use_case),
) -> APIResponse[CreditoResponse]:
    """
    Actualizar el limite de credito autorizado.
    """
    command = ActualizarLimiteCreditoCommand(
        credit_id=credit_id,
        new_limit=request.new_limit
    )
    updated_credit = use_case.execute(command)
    response_data = CreditoResponse.model_validate(updated_credit)

    return APIResponse(
        success=True,
        message="Limite de credito actualizado correctamente.",
        data=response_data,
    )

@router.post(
    "/{credit_id}/inactivar",
    response_model=APIResponse[CreditoResponse],
    status_code=status.HTTP_200_OK,
)
def suspend_credit_account(
    credit_id: UUID,
    use_case: InactivarCuentaCreditoUseCase = Depends(get_inactivar_cuenta_use_case),
) -> APIResponse[CreditoResponse]:
    """
    Suspender una cuenta de credito.
    """
    command = InactivarCuentaCreditoCommand(credit_id=credit_id)
    updated_credit = use_case.execute(command)
    response_data = CreditoResponse.model_validate(updated_credit)

    return APIResponse(
        success=True,
        message="Cuenta de credito suspendida correctamente.",
        data=response_data,
    )
