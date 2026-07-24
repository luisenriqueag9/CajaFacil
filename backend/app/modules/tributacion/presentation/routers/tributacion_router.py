from uuid import UUID
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.tributacion.application.use_cases import (
    CrearConfiguracionTributariaUseCase,
    CrearConfiguracionTributariaCommand,
    TasaInput,
    ActivarConfiguracionTributariaUseCase,
    ObtenerConfiguracionActivaUseCase,
    CalcularImpuestoTransaccionUseCase
)
from app.modules.tributacion.presentation.dependencies.tributacion_dependencies import (
    get_crear_configuracion_use_case,
    get_activar_configuracion_use_case,
    get_obtener_configuracion_activa_use_case,
    get_calcular_impuesto_use_case
)
from app.modules.tributacion.presentation.dto import (
    CrearConfiguracionRequest,
    ConfiguracionTributariaResponse,
    CotizarItemsRequest,
    DesgloseImpuestoResponse
)

router = APIRouter()

@router.post(
    "/",
    response_model=ApiResponse[ConfiguracionTributariaResponse],
    status_code=status.HTTP_201_CREATED,
)
def crear_configuracion(
    request: CrearConfiguracionRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: CrearConfiguracionTributariaUseCase = Depends(get_crear_configuracion_use_case)
) -> ApiResponse[ConfiguracionTributariaResponse]:
    """
    Registra una nueva versión de configuración tributaria con sus respectivas tasas.
    Nace en estado inactivo.
    """
    command = CrearConfiguracionTributariaCommand(
        company_id=company_id,
        name=request.name,
        calculation_type=request.calculation_type,
        rates=[
            TasaInput(name=r.name, code=r.code, rate_percentage=r.rate_percentage)
            for r in request.rates
        ]
    )

    config_ent = use_case.execute(command)
    response_dto = ConfiguracionTributariaResponse.model_validate(config_ent)

    return ApiResponse(
        success=True,
        message="Configuración tributaria creada correctamente.",
        data=response_dto
    )


@router.post(
    "/{configuracion_id}/activar",
    response_model=ApiResponse[ConfiguracionTributariaResponse],
    status_code=status.HTTP_200_OK,
)
def activar_configuracion(
    configuracion_id: UUID,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: ActivarConfiguracionTributariaUseCase = Depends(get_activar_configuracion_use_case)
) -> ApiResponse[ConfiguracionTributariaResponse]:
    """
    Activa una versión impositiva específica y devalúa la versión anterior del tenant.
    """
    config_ent = use_case.execute(company_id=company_id, configuracion_id=configuracion_id)
    response_dto = ConfiguracionTributariaResponse.model_validate(config_ent)

    return ApiResponse(
        success=True,
        message="Configuración tributaria activada correctamente.",
        data=response_dto
    )


@router.get(
    "/activa",
    response_model=ApiResponse[ConfiguracionTributariaResponse | None],
    status_code=status.HTTP_200_OK,
)
def obtener_configuracion_activa(
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: ObtenerConfiguracionActivaUseCase = Depends(get_obtener_configuracion_activa_use_case)
) -> ApiResponse[ConfiguracionTributariaResponse | None]:
    """
    Obtiene la configuración impositiva activa vigente para una empresa.
    """
    config_ent = use_case.execute(company_id=company_id)
    response_dto = ConfiguracionTributariaResponse.model_validate(config_ent) if config_ent else None

    return ApiResponse(
        success=True,
        message="Configuración tributaria activa obtenida correctamente.",
        data=response_dto
    )


@router.post(
    "/calcular",
    response_model=ApiResponse[list[DesgloseImpuestoResponse]],
    status_code=status.HTTP_200_OK,
)
def calcular_impuestos(
    request: CotizarItemsRequest,
    company_id: UUID = Query(..., description="Company Tenant UUID"),
    use_case: CalcularImpuestoTransaccionUseCase = Depends(get_calcular_impuesto_use_case)
) -> ApiResponse[list[DesgloseImpuestoResponse]]:
    """
    Ejecuta el Motor Tributario de forma stateless para cotizar un desglose impositivo
    de ítems utilizando la configuración activa del tenant.
    """
    items_raw = [
        {"price": item.price, "quantity": item.quantity, "tax_category": item.tax_category}
        for item in request.items
    ]

    desgloses = use_case.execute(company_id=company_id, items=items_raw)
    response_dtos = [DesgloseImpuestoResponse.model_validate(d) for d in desgloses]

    return ApiResponse(
        success=True,
        message="Impuestos calculados correctamente.",
        data=response_dtos
    )
