from uuid import UUID
from app.common.exceptions import ValidationException, NotFoundException

class CajaCerradaException(ValidationException):
    def __init__(self, sesion_id: UUID):
        super().__init__(
            message=f"La sesion de caja '{sesion_id}' esta cerrada y no admite modificaciones.",
            code="CAJA_CERRADA"
        )

class CajaYaAbiertaException(ValidationException):
    def __init__(self, user_id: UUID):
        super().__init__(
            message=f"El usuario '{user_id}' ya tiene una sesion de caja activa abierta.",
            code="CAJA_YA_ABIERTA"
        )

class CajaNotFoundException(NotFoundException):
    def __init__(self, caja_id: UUID):
        super().__init__(
            message=f"Caja fisica '{caja_id}' no encontrada.",
            code="CAJA_NOT_FOUND"
        )

class SesionCajaNotFoundException(NotFoundException):
    def __init__(self, sesion_id: UUID):
        super().__init__(
            message=f"Sesion de caja '{sesion_id}' no encontrada.",
            code="SESION_CAJA_NOT_FOUND"
        )

class MontoInvalidoException(ValidationException):
    def __init__(self, amount: float):
        super().__init__(
            message=f"El monto debe ser estrictamente positivo. Recibido: {amount}.",
            code="MONTO_INVALIDO"
        )

class CajaNoAbiertaException(ValidationException):
    def __init__(self, sesion_id: UUID):
        super().__init__(
            message=f"La sesion de caja '{sesion_id}' debe estar abierta para realizar esta operacion.",
            code="CAJA_NO_ABIERTA"
        )
