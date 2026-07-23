from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.modules.inventario.domain.exceptions import CantidadInvalidaException

@dataclass
class Merma:
    id: UUID
    reason: str  # ROTURA, VENCIMIENTO, ROBO, OTRO
    description: str | None = None

    def __post_init__(self) -> None:
        if self.reason not in {"ROTURA", "VENCIMIENTO", "ROBO", "OTRO"}:
            raise ValueError(f"Motivo de merma inválido: {self.reason}")


@dataclass
class AjusteInventario:
    id: UUID
    physical_quantity: Decimal
    system_quantity: Decimal
    difference: Decimal


@dataclass
class MovimientoInventario:
    id: UUID
    company_id: UUID
    product_id: UUID
    type: str  # ENTRADA, SALIDA
    concept: str  # COMPRA, VENTA, ANULACION_VENTA, MERMA, AJUSTE, DEVOLUCION_PROVEEDOR, INVENTARIO_INICIAL
    quantity: Decimal
    origin_document_id: UUID | None
    created_at: datetime
    created_by: UUID
    notes: str | None = None
    merma: Merma | None = None
    ajuste: AjusteInventario | None = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        # Quantity validation
        if self.quantity <= Decimal("0.0000"):
            raise CantidadInvalidaException(float(self.quantity))

        # Type validation
        if self.type not in {"ENTRADA", "SALIDA"}:
            raise ValueError(f"Tipo de movimiento inválido: {self.type}")

        # Concept validation
        valid_concepts = {
            "COMPRA", "VENTA", "ANULACION_VENTA", "MERMA", "AJUSTE", 
            "DEVOLUCION_PROVEEDOR", "INVENTARIO_INICIAL"
        }
        if self.concept not in valid_concepts:
            raise ValueError(f"Concepto de movimiento inválido: {self.concept}")

        # Conditional entities validations
        if self.concept == "MERMA" and self.merma is None:
            raise ValueError("Un movimiento por concepto MERMA debe incluir su entidad de detalle Merma.")

        if self.concept == "AJUSTE" and self.ajuste is None:
            raise ValueError("Un movimiento por concepto AJUSTE debe incluir su entidad de detalle AjusteInventario.")
