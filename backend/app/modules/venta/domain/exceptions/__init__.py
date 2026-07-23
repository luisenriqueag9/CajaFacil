from uuid import UUID
from app.common.exceptions import ValidationException, NotFoundException

class VentaVaciaException(ValidationException):
    def __init__(self):
        super().__init__(
            message="La venta debe contener al menos un detalle de venta.",
            code="VENTA_VACIA"
        )

class CantidadInvalidaException(ValidationException):
    def __init__(self, product_id: UUID, quantity: any):
        super().__init__(
            message=f"La cantidad para el producto '{product_id}' debe ser mayor que cero. Cantidad recibida: {quantity}.",
            code="CANTIDAD_INVALIDA",
            details={"product_id": str(product_id), "quantity": str(quantity)}
        )

class ImporteIncoherenteException(ValidationException):
    def __init__(self, expected: any, actual: any):
        super().__init__(
            message=f"El total de la venta no es coherente con sus detalles e impuestos. Esperado: {expected}, Calculado: {actual}.",
            code="IMPORTE_INCOHERENTE",
            details={"expected": str(expected), "actual": str(actual)}
        )

class PagoInsuficienteException(ValidationException):
    def __init__(self, total_venta: any, total_pago: any):
        super().__init__(
            message=f"La cobertura total del importe no coincide con el total de la venta. Total Venta: {total_venta}, Total Cobrado: {total_pago}.",
            code="PAGO_INSUFICIENTE",
            details={"total_venta": str(total_venta), "total_pago": str(total_pago)}
        )

class ClienteRequeridoParaCreditoException(ValidationException):
    def __init__(self):
        super().__init__(
            message="El cliente es requerido para ventas con forma de pago Crédito.",
            code="CLIENTE_REQUERIDO_PARA_CREDITO"
        )

class VentaInmutableException(ValidationException):
    def __init__(self, venta_id: UUID):
        super().__init__(
            message=f"La venta con id '{venta_id}' es inmutable y no puede modificarse.",
            code="VENTA_INMUTABLE",
            details={"venta_id": str(venta_id)}
        )

class VentaYaAnuladaException(ValidationException):
    def __init__(self, venta_id: UUID):
        super().__init__(
            message=f"La venta con id '{venta_id}' ya se encuentra anulada.",
            code="VENTA_YA_ANULADA",
            details={"venta_id": str(venta_id)}
        )

class UsuarioNoAutorizadoParaAnulacionException(ValidationException):
    def __init__(self, user_id: UUID):
        super().__init__(
            message=f"El usuario '{user_id}' no está autorizador para anular ventas.",
            code="USUARIO_NO_AUTORIZADO_ANULACION",
            details={"user_id": str(user_id)}
        )

class CajaCerradaException(ValidationException):
    def __init__(self, box_id: UUID):
        super().__init__(
            message=f"La caja con id '{box_id}' no está abierta para registrar ventas.",
            code="CAJA_CERRADA",
            details={"box_id": str(box_id)}
        )

class VentaNotFoundException(NotFoundException):
    def __init__(self, venta_id: UUID):
        super().__init__(
            message=f"La venta con id '{venta_id}' no fue encontrada.",
            code="VENTA_NOT_FOUND",
            details={"venta_id": str(venta_id)}
        )
