import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from sqlalchemy.orm import Session

from app.common.exceptions import ValidationException
from app.modules.venta.domain.entities.venta import Venta, DetalleVenta, FormaPagoAceptada
from app.modules.venta.domain.repositories.venta_repository import VentaRepository
from app.modules.venta.domain.events.venta_events import VentaConfirmada
from app.modules.venta.domain.exceptions import CajaCerradaException, ClienteRequeridoParaCreditoException
from app.modules.venta.application.ports.product_lookup import ProductLookup
from app.modules.venta.application.ports.box_lookup import BoxLookup
from app.modules.venta.application.ports.credit_lookup import CreditLookup
from app.modules.venta.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class DetalleVentaCommand:
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    discount: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    subtotal: Decimal
    total: Decimal

@dataclass(frozen=True)
class FormaPagoAceptadaCommand:
    payment_method: str
    amount: Decimal
    transaction_reference: str | None = None

@dataclass(frozen=True)
class ConfirmarVentaCommand:
    company_id: UUID
    box_id: UUID
    user_id: UUID
    client_id: UUID | None
    invoice_number: str | None
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal
    details: list[DetalleVentaCommand]
    payments: list[FormaPagoAceptadaCommand]

class ConfirmarVentaUseCase:
    """
    Application Use Case to register and confirm a Venta.
    Coordinates the Unit of Work, sharing a single SQLite database transaction across repositories.
    """
    def __init__(
        self,
        repository: VentaRepository,
        db: Session,
        event_dispatcher: EventDispatcher,
        product_lookup: ProductLookup,
        box_lookup: BoxLookup,
        credit_lookup: CreditLookup
    ):
        self.repository = repository
        self.db = db
        self.event_dispatcher = event_dispatcher
        self.product_lookup = product_lookup
        self.box_lookup = box_lookup
        self.credit_lookup = credit_lookup

    def execute(self, command: ConfirmarVentaCommand) -> Venta:
        # 1. Validate Box is open and active
        if not self.box_lookup.is_open_and_active(command.company_id, command.box_id):
            raise CajaCerradaException(command.box_id)

        # 2. Validate products are active
        for detail in command.details:
            if not self.product_lookup.exists_and_active(command.company_id, detail.product_id):
                raise ValidationException(
                    f"El producto '{detail.product_id}' no existe o está inactivo en esta empresa."
                )

        # 3. Validate credit line if payment method is CREDITO
        credit_amount = Decimal("0.00")
        has_credit = False
        for pay in command.payments:
            if pay.payment_method == "CREDITO":
                has_credit = True
                credit_amount += pay.amount

        if has_credit:
            if command.client_id is None:
                raise ClienteRequeridoParaCreditoException()
            if not self.credit_lookup.has_active_credit_and_limit(command.company_id, command.client_id, credit_amount):
                raise ValidationException(
                    f"El cliente '{command.client_id}' no tiene línea de crédito activa o su cupo disponible es insuficiente para el monto: {credit_amount}."
                )

        # 4. Construct Domain entities (Runs domain validations/invariants)
        venta_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        details_entities = [
            DetalleVenta(
                id=uuid.uuid4(),
                product_id=d.product_id,
                quantity=d.quantity,
                unit_price=d.unit_price,
                discount=d.discount,
                tax_rate=d.tax_rate,
                tax_amount=d.tax_amount,
                subtotal=d.subtotal,
                total=d.total
            ) for d in command.details
        ]

        payments_entities = [
            FormaPagoAceptada(
                payment_method=p.payment_method,
                amount=p.amount,
                transaction_reference=p.transaction_reference
            ) for p in command.payments
        ]

        venta = Venta(
            id=venta_id,
            company_id=command.company_id,
            box_id=command.box_id,
            user_id=command.user_id,
            client_id=command.client_id,
            invoice_number=command.invoice_number,
            subtotal=command.subtotal,
            discount=command.discount,
            tax=command.tax,
            total=command.total,
            status="CONFIRMADA",
            created_at=now,
            updated_at=now,
            details=details_entities,
            payments=payments_entities
        )

        # 5. Unit of Work coordination (Single SQLite transaction)
        try:
            # We open an inner transaction to rollback only this unit of work if nested,
            # or control transaction directly.
            with self.db.begin_nested():
                # Persist Venta (adds to SQLAlchemy session and flushes, but does not commit)
                created_venta = self.repository.save(venta)

                # Instantiate the event payload
                items_payload = [
                    {
                        "product_id": d.product_id,
                        "quantity": d.quantity,
                        "unit_price": d.unit_price
                    } for d in created_venta.details
                ]
                cash_amount = sum(p.amount for p in created_venta.payments if p.payment_method == "EFECTIVO")
                credit_amount = sum(p.amount for p in created_venta.payments if p.payment_method == "CREDITO")

                event = VentaConfirmada(
                    venta_id=created_venta.id,
                    company_id=created_venta.company_id,
                    box_id=created_venta.box_id,
                    user_id=created_venta.user_id,
                    client_id=created_venta.client_id,
                    invoice_number=created_venta.invoice_number,
                    total=created_venta.total,
                    items=items_payload,
                    cash_amount=cash_amount,
                    credit_amount=credit_amount,
                    occurred_at=created_venta.created_at
                )

                # Dispatch synchronously inside the transaction
                self.event_dispatcher.dispatch(event)
                
            # If everything goes well, commit the outer transaction
            self.db.commit()
            return created_venta
        except Exception as e:
            self.db.rollback()
            raise e
