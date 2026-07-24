from uuid import UUID
from app.common.exceptions import CajaFacilException

class ConfiguracionInvalidaException(CajaFacilException):
    def __init__(self, message: str):
        super().__init__(
            code="CONFIGURACION_INVALIDA",
            message=message,
            status_code=400
        )


class ConfiguracionNotFoundException(CajaFacilException):
    def __init__(self, config_id: UUID):
        super().__init__(
            code="CONFIGURACION_NOT_FOUND",
            message=f"Configuración tributaria '{config_id}' no encontrada.",
            status_code=404
        )


class ConfiguracionExpiradaException(CajaFacilException):
    def __init__(self, config_id: UUID):
        super().__init__(
            code="CONFIGURACION_EXPIRADA",
            message=f"La configuración tributaria '{config_id}' ha expirado y no se puede modificar.",
            status_code=400
        )


class SolapamientoConfiguracionException(CajaFacilException):
    def __init__(self, company_id: UUID):
        super().__init__(
            code="SOLAPAMIENTO_CONFIGURACION",
            message=f"La empresa '{company_id}' ya cuenta con una configuración tributaria activa.",
            status_code=400
        )
