from uuid import UUID
from app.common.exceptions import CajaFacilException

class StockInsuficienteException(CajaFacilException):
    def __init__(self, product_id: UUID, current_stock: float, requested: float):
        super().__init__(
            code="STOCK_INSUFICIENTE",
            message=f"Stock insuficiente para el producto '{product_id}'. Existencia actual: {current_stock}, solicitado: {requested}.",
            status_code=400
        )


class ProductoNoManejaInventarioException(CajaFacilException):
    def __init__(self, product_id: UUID):
        super().__init__(
            code="PRODUCTO_NO_MANEJA_INVENTARIO",
            message=f"El producto '{product_id}' tiene deshabilitado el control de inventario.",
            status_code=400
        )


class CantidadInvalidaException(CajaFacilException):
    def __init__(self, quantity: float):
        super().__init__(
            code="CANTIDAD_INVALIDA",
            message=f"La cantidad del movimiento debe ser estrictamente positiva. Recibido: {quantity}.",
            status_code=400
        )


class MovimientoInmutableException(CajaFacilException):
    def __init__(self):
        super().__init__(
            code="MOVIMIENTO_INMUTABLE",
            message="No se permite modificar un movimiento de inventario confirmado.",
            status_code=400
        )


class MovimientoNotFoundException(CajaFacilException):
    def __init__(self, movimiento_id: UUID):
        super().__init__(
            code="MOVIMIENTO_NOT_FOUND",
            message=f"Movimiento de inventario '{movimiento_id}' no encontrado.",
            status_code=404
        )
