from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.venta.domain.exceptions import (
    VentaVaciaException,
    CantidadInvalidaException,
    ImporteIncoherenteException,
    PagoInsuficienteException,
    ClienteRequeridoParaCreditoException,
    ValidationException
)

@dataclass
class DetalleVenta:
    id: UUID
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    discount: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    subtotal: Decimal
    total: Decimal

    def validate(self) -> None:
        if self.quantity <= Decimal("0.00"):
            raise CantidadInvalidaException(self.product_id, self.quantity)
        if self.unit_price < Decimal("0.00"):
            raise ValidationException("El precio unitario no puede ser negativo.")
        if self.discount < Decimal("0.00"):
            raise ValidationException("El descuento no puede ser negativo.")
        if self.tax_rate < Decimal("0.00"):
            raise ValidationException("La tasa de impuesto no puede ser negativa.")
        
        # Recalculate subtotal and total
        expected_subtotal = (self.quantity * self.unit_price).quantize(Decimal("0.01"))
        expected_total = (expected_subtotal - self.discount + self.tax_amount).quantize(Decimal("0.01"))
        
        if abs(self.subtotal - expected_subtotal) > Decimal("0.01"):
            raise ValidationException(f"El subtotal de la línea para {self.product_id} no cuadra. Esperado: {expected_subtotal}, Real: {self.subtotal}")
        if abs(self.total - expected_total) > Decimal("0.01"):
            raise ValidationException(f"El total de la línea para {self.product_id} no cuadra. Esperado: {expected_total}, Real: {self.total}")

@dataclass(frozen=True)
class FormaPagoAceptada:
    payment_method: str  # EFECTIVO, TARJETA, CREDITO
    amount: Decimal
    transaction_reference: str | None = None

    def validate(self) -> None:
        if self.amount <= Decimal("0.00"):
            raise ValidationException("El monto de la forma de pago debe ser mayor que cero.")
        if self.payment_method not in {"EFECTIVO", "TARJETA", "CREDITO"}:
            raise ValidationException(f"Forma de pago '{self.payment_method}' no válida.")

@dataclass
class Venta:
    id: UUID
    company_id: UUID
    box_id: UUID
    user_id: UUID
    client_id: UUID | None
    invoice_number: str | None
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal
    status: str  # CONFIRMADA, ANULADA
    created_at: datetime
    updated_at: datetime
    details: list[DetalleVenta] = field(default_factory=list)
    payments: list[FormaPagoAceptada] = field(default_factory=list)

    # Auditoría de anulación
    voided_by: UUID | None = None
    voided_at: datetime | None = None
    void_reason: str | None = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """
        Validates all business invariants of the Venta aggregate root.
        """
        # Status validation
        if self.status not in {"CONFIRMADA", "ANULADA"}:
            raise ValidationException(f"Estado de venta '{self.status}' no permitido.")

        # Existence validation
        if not self.details:
            raise VentaVaciaException()

        # Lines validation
        calc_subtotal = Decimal("0.00")
        calc_discount = Decimal("0.00")
        calc_tax = Decimal("0.00")
        calc_total = Decimal("0.00")

        for item in self.details:
            item.validate()
            calc_subtotal += item.subtotal
            calc_discount += item.discount
            calc_tax += item.tax_amount
            calc_total += item.total

        # Round values for exact comparison
        calc_subtotal = calc_subtotal.quantize(Decimal("0.01"))
        calc_discount = calc_discount.quantize(Decimal("0.01"))
        calc_tax = calc_tax.quantize(Decimal("0.01"))
        calc_total = calc_total.quantize(Decimal("0.01"))

        # Coherence validation
        if abs(self.subtotal - calc_subtotal) > Decimal("0.01"):
            raise ImporteIncoherenteException(self.subtotal, calc_subtotal)
        if abs(self.discount - calc_discount) > Decimal("0.01"):
            raise ImporteIncoherenteException(self.discount, calc_discount)
        if abs(self.tax - calc_tax) > Decimal("0.01"):
            raise ImporteIncoherenteException(self.tax, calc_tax)
        if abs(self.total - calc_total) > Decimal("0.01"):
            raise ImporteIncoherenteException(self.total, calc_total)

        # Payment validation
        total_payment = Decimal("0.00")
        has_credit = False
        for pay in self.payments:
            pay.validate()
            total_payment += pay.amount
            if pay.payment_method == "CREDITO":
                has_credit = True

        total_payment = total_payment.quantize(Decimal("0.01"))
        if abs(self.total - total_payment) > Decimal("0.01"):
            raise PagoInsuficienteException(self.total, total_payment)

        # Credit validation
        if has_credit and self.client_id is None:
            raise ClienteRequeridoParaCreditoException()

        # Voiding validation
        if self.status == "ANULADA":
            if not self.voided_by:
                raise ValidationException("Una venta anulada requiere registrar el usuario supervisor (voided_by).")
            if not self.voided_at:
                raise ValidationException("Una venta anulada requiere registrar la fecha de anulación (voided_at).")
            if not self.void_reason or not self.void_reason.strip():
                raise ValidationException("Una venta anulada requiere registrar una justificación (void_reason).")

    def anular(self, supervisor_id: UUID, reason: str, timestamp: datetime) -> None:
        """
        Transitions the sale to the ANULADA state with supervisor auditing details.
        """
        if self.status == "ANULADA":
            from app.modules.venta.domain.exceptions import VentaYaAnuladaException
            raise VentaYaAnuladaException(self.id)

        self.status = "ANULADA"
        self.voided_by = supervisor_id
        self.voided_at = timestamp
        self.void_reason = reason
        self.updated_at = timestamp
        self.validate()
