from uuid import UUID
from fastapi import status
from app.common.exceptions import ValidationException

class CompraYaExisteException(ValidationException):
    """
    Excepcion lanzada cuando ya existe una compra con el mismo numero de factura para el proveedor.
    """
    def __init__(self, invoice_number: str, supplier_id: UUID):
        super().__init__(
            message=f"Ya existe una compra con el numero de factura '{invoice_number}' para el proveedor '{supplier_id}'.",
            code="COMPRA_YA_EXISTE",
            details={
                "invoice_number": invoice_number,
                "supplier_id": str(supplier_id)
            }
        )
        # Override HTTP status code to 409 Conflict for REST compliance
        self.status_code = status.HTTP_409_CONFLICT
