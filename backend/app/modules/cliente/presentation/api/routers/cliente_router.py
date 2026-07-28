from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from typing import List

from app.common.responses import APIResponse
from app.modules.cliente.presentation.api.schemas.cliente_schema import (
    RegistrarClienteRequest,
    ActualizarClienteRequest,
    ClienteResponse,
)
from app.modules.cliente.presentation.api.dependencies.cliente_dependencies import (
    get_registrar_cliente_use_case,
    get_actualizar_cliente_use_case,
    get_inactivar_cliente_use_case,
    get_obtener_cliente_use_case,
    get_listar_clientes_use_case,
)
from app.modules.cliente.application.use_cases import (
    RegistrarClienteUseCase,
    ActualizarClienteUseCase,
    InactivarClienteUseCase,
    ObtenerClienteUseCase,
    ListarClientesUseCase,
)
from app.modules.cliente.application.commands import (
    RegistrarClienteCommand,
    ActualizarClienteCommand,
    InactivarClienteCommand,
)
from app.modules.cliente.application.queries import (
    ObtenerClienteQuery,
    ListarClientesQuery,
)

router = APIRouter()

@router.post(
    "",
    response_model=APIResponse[ClienteResponse],
    status_code=status.HTTP_201_CREATED,
)
def register_client(
    request: RegistrarClienteRequest,
    use_case: RegistrarClienteUseCase = Depends(get_registrar_cliente_use_case),
) -> APIResponse[ClienteResponse]:
    """
    Registrar un nuevo cliente en el sistema.
    """
    command = RegistrarClienteCommand(
        company_id=request.company_id,
        name=request.name,
        tax_id=request.tax_id,
        phone=request.phone,
        email=request.email
    )
    created_client = use_case.execute(command)
    response_data = ClienteResponse.model_validate(created_client)

    return APIResponse(
        success=True,
        message="Cliente registrado correctamente.",
        data=response_data,
    )

@router.get(
    "",
    response_model=APIResponse[List[ClienteResponse]],
    status_code=status.HTTP_200_OK,
)
def list_clients(
    company_id: UUID = Query(..., description="ID de la empresa obligatoria para filtrar"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (ACTIVO/INACTIVO)"),
    use_case: ListarClientesUseCase = Depends(get_listar_clientes_use_case),
) -> APIResponse[List[ClienteResponse]]:
    """
    Listar los clientes de la empresa.
    """
    query = ListarClientesQuery(
        company_id=company_id,
        status=status_filter
    )
    clients = use_case.execute(query)
    response_data = [ClienteResponse.model_validate(c) for c in clients]

    return APIResponse(
        success=True,
        message="Clientes obtenidos correctamente.",
        data=response_data,
    )

@router.get(
    "/{client_id}",
    response_model=APIResponse[ClienteResponse],
    status_code=status.HTTP_200_OK,
)
def get_client_by_id(
    client_id: UUID,
    use_case: ObtenerClienteUseCase = Depends(get_obtener_cliente_use_case),
) -> APIResponse[ClienteResponse]:
    """
    Obtener los detalles de un cliente por su UUID.
    """
    query = ObtenerClienteQuery(client_id=client_id)
    client = use_case.execute(query)
    response_data = ClienteResponse.model_validate(client)

    return APIResponse(
        success=True,
        message="Cliente obtenido correctamente.",
        data=response_data,
    )

@router.put(
    "/{client_id}",
    response_model=APIResponse[ClienteResponse],
    status_code=status.HTTP_200_OK,
)
def update_client(
    client_id: UUID,
    request: ActualizarClienteRequest,
    use_case: ActualizarClienteUseCase = Depends(get_actualizar_cliente_use_case),
) -> APIResponse[ClienteResponse]:
    """
    Actualizar la informacion de un cliente existente.
    """
    command = ActualizarClienteCommand(
        client_id=client_id,
        name=request.name,
        tax_id=request.tax_id,
        phone=request.phone,
        email=request.email
    )
    updated_client = use_case.execute(command)
    response_data = ClienteResponse.model_validate(updated_client)

    return APIResponse(
        success=True,
        message="Cliente actualizado correctamente.",
        data=response_data,
    )

@router.post(
    "/{client_id}/inactivar",
    response_model=APIResponse[ClienteResponse],
    status_code=status.HTTP_200_OK,
)
def deactivate_client(
    client_id: UUID,
    use_case: InactivarClienteUseCase = Depends(get_inactivar_cliente_use_case),
) -> APIResponse[ClienteResponse]:
    """
    Inactivar comercialmente un cliente del sistema.
    """
    command = InactivarClienteCommand(client_id=client_id)
    updated_client = use_case.execute(command)
    response_data = ClienteResponse.model_validate(updated_client)

    return APIResponse(
        success=True,
        message="Cliente inactivado correctamente.",
        data=response_data,
    )
