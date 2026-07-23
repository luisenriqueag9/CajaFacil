from uuid import UUID
from app.common.exceptions import CajaFacilException

class CajaCerradaException(CajaFacilException):
    def __init__(self, caja_id: UUID):
        super().__init__(
            code="CAJA_CERRADA",
            message=f"La sesión de caja '{caja_id}' está cerrada y no admite modificaciones.",
            status_code=400
        )


class CajaYaAbiertaException(CajaFacilException):
    def __init__(self, user_id: UUID):
        super().__init__(
            code="CAJA_YA_ABIERTA",
            message=f"El usuario '{user_id}' ya tiene una sesión de caja activa abierta.",
            status_code=400
        )


class CajaNotFoundException(CajaFacilException):
    def __init__(self, caja_id: UUID):
        super().__init__(
            code="CAJA_NOT_FOUND",
            message=f"Sesión de caja '{caja_id}' no encontrada.",
            status_code=404
        )


class MontoInvalidoException(CajaFacilException):
    def __init__(self, amount: float):
        super().__init__(
            code="MONTO_INVALIDO",
            message=f"El monto de la transacción debe ser estrictamente positivo. Recibido: {amount}.",
            status_code=400
        )


class CajaNoAbiertaException(CajaFacilException):
    def __init__(self, caja_id: UUID):
        super().__init__(
            code="CAJA_NO_ABIERTA",
            message=f"La sesión de caja '{caja_id}' debe estar abierta para realizar esta operación.",
            status_code=400
        )
