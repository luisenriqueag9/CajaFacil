from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID
import uuid
from typing import Union, List

from app.modules.compra.domain.exceptions.compra_invalida_exception import CompraInvalidaException
from app.modules.compra.domain.entities.detalle_compra import DetalleCompra
from app.modules.compra.domain.value_objects.estado_compra import EstadoCompra
from app.modules.compra.domain.value_objects.numero_compra import NumeroCompra
from app.modules.compra.domain.value_objects.cantidad import Cantidad
from app.modules.compra.domain.value_objects.dinero import Dinero

@dataclass
class Compra:
    id: UUID
    company_id: UUID
    supplier_id: UUID
    invoice_number: Union[NumeroCompra, str]
    payment_condition: str
    issue_date: datetime
    status: Union[EstadoCompra, str]
    created_at: datetime
    updated_at: datetime
    items: List[DetalleCompra] = field(default_factory=list)
    _events: list = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        # Coerce values to Value Objects
        if not isinstance(self.invoice_number, NumeroCompra):
            self.invoice_number = NumeroCompra(self.invoice_number)
        if not isinstance(self.status, EstadoCompra):
            self.status = EstadoCompra(self.status)

        # Enforce that all items are initialized using DetalleCompra entity
        for i, item in enumerate(self.items):
            if not isinstance(item, DetalleCompra):
                if isinstance(item, dict):
                    self.items[i] = DetalleCompra(**item)
                else:
                    raise CompraInvalidaException("Los items de la compra deben ser instancias de DetalleCompra.")

        self.validate()

    def validate(self) -> None:
        if not self.company_id:
            raise CompraInvalidaException("La compra debe pertenecer a una empresa (company_id es requerido).")
        if not self.supplier_id:
            raise CompraInvalidaException("El proveedor es obligatorio.")
        
        valid_conditions = {"CONTADO", "CREDITO"}
        if self.payment_condition not in valid_conditions:
            raise CompraInvalidaException(
                f"Condicion de pago '{self.payment_condition}' invalida. Debe ser CONTADO o CREDITO."
            )

        # Validate each item internally
        for item in self.items:
            item.validate()

    def registrar_evento(self, event) -> None:
        self._events.append(event)

    def limpiar_eventos(self) -> None:
        self._events.clear()

    @property
    def eventos(self) -> list:
        return self._events

    @classmethod
    def create_draft(
        cls, 
        id: UUID, 
        company_id: UUID, 
        supplier_id: UUID, 
        invoice_number: Union[NumeroCompra, str], 
        payment_condition: str, 
        issue_date: datetime,
        created_at: datetime,
        updated_at: datetime
    ) -> "Compra":
        """
        Metodo factory para inicializar una compra en estado BORRADOR.
        """
        return cls(
            id=id,
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number=invoice_number,
            payment_condition=payment_condition,
            issue_date=issue_date,
            status=EstadoCompra.borrador(),
            created_at=created_at,
            updated_at=updated_at,
            items=[]
        )

    @classmethod
    def register(
        cls, 
        id: UUID, 
        company_id: UUID, 
        supplier_id: UUID, 
        invoice_number: Union[NumeroCompra, str], 
        payment_condition: str, 
        issue_date: datetime,
        created_at: datetime,
        updated_at: datetime,
        items_payload: list
    ) -> "Compra":
        """
        Metodo factory para registrar y confirmar una compra directamente con sus lineas.
        """
        # Populate details check
        if not items_payload:
            raise CompraInvalidaException("Una compra registrada no puede crearse sin lineas de detalle.")

        compra = cls(
            id=id,
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number=invoice_number,
            payment_condition=payment_condition,
            issue_date=issue_date,
            status=EstadoCompra.registrada(),
            created_at=created_at,
            updated_at=updated_at,
            items=[]
        )

        # Apply V1 consolidator business policy: collapse duplicate products in items payload
        consolidated = {}
        for item in items_payload:
            product_id = item["product_id"]
            qty_val = item["quantity"].valor if isinstance(item["quantity"], Cantidad) else Decimal(str(item["quantity"]))
            cost_val = item["unit_cost"].monto if isinstance(item["unit_cost"], Dinero) else Decimal(str(item["unit_cost"]))
            
            if product_id in consolidated:
                prev_qty, prev_cost = consolidated[product_id]
                total_qty = prev_qty + qty_val
                if total_qty > Decimal("0.0000"):
                    weighted_cost = ((prev_qty * prev_cost) + (qty_val * cost_val)) / total_qty
                else:
                    weighted_cost = cost_val
                consolidated[product_id] = (total_qty, weighted_cost)
            else:
                consolidated[product_id] = (qty_val, cost_val)

        for prod_id, (qty, cost) in consolidated.items():
            detail = DetalleCompra(
                id=uuid.uuid4(),
                purchase_id=id,
                product_id=prod_id,
                quantity=Cantidad(qty),
                unit_cost=Dinero(cost)
            )
            compra.items.append(detail)

        compra.validate()

        # Record CompraRegistrada domain event
        from app.modules.compra.domain.events.compra_events import CompraRegistrada
        event_items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_cost": item.unit_cost
            }
            for item in compra.items
        ]
        evento_compra = CompraRegistrada(
            purchase_id=compra.id,
            company_id=compra.company_id,
            supplier_id=compra.supplier_id,
            total=compra.total,
            payment_condition=compra.payment_condition,
            items=event_items,
            occurred_at=created_at
        )
        compra.registrar_evento(evento_compra)

        return compra

    def add_item(self, product_id: UUID, quantity: Union[Cantidad, Decimal, int, float], unit_cost: Union[Dinero, Decimal, int, float]) -> None:
        if self.status.valor != "BORRADOR":
            raise CompraInvalidaException("No se pueden anadir items a una compra que no este en estado BORRADOR.")
        
        vo_quantity = quantity if isinstance(quantity, Cantidad) else Cantidad(quantity)
        vo_unit_cost = unit_cost if isinstance(unit_cost, Dinero) else Dinero(unit_cost)

        for item in self.items:
            if item.product_id == product_id:
                total_qty = item.quantity.valor + vo_quantity.valor
                if total_qty > Decimal("0.0000"):
                    weighted_cost = ((item.quantity.valor * item.unit_cost.monto) + (vo_quantity.valor * vo_unit_cost.monto)) / total_qty
                else:
                    weighted_cost = vo_unit_cost.monto
                item.quantity = Cantidad(total_qty)
                item.unit_cost = Dinero(weighted_cost)
                item.validate()
                return

        detail = DetalleCompra(
            id=uuid.uuid4(),
            purchase_id=self.id,
            product_id=product_id,
            quantity=vo_quantity,
            unit_cost=vo_unit_cost
        )
        self.items.append(detail)

    def remove_item(self, product_id: UUID) -> None:
        if self.status.valor != "BORRADOR":
            raise CompraInvalidaException("No se pueden remover items de una compra que no este en estado BORRADOR.")
        self.items = [item for item in self.items if item.product_id != product_id]

    def confirm(self, timestamp: datetime = None) -> None:
        if self.status.valor != "BORRADOR":
            raise CompraInvalidaException("La compra ya se encuentra registrada o anulada.")
        if not self.items:
            raise CompraInvalidaException("No se puede registrar una compra sin lineas de detalle.")
        self.status = EstadoCompra.registrada()
        actual_timestamp = timestamp or datetime.now()
        self.updated_at = actual_timestamp
        self.validate()

        # Record CompraRegistrada domain event
        from app.modules.compra.domain.events.compra_events import CompraRegistrada
        event_items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_cost": item.unit_cost
            }
            for item in self.items
        ]
        evento_compra = CompraRegistrada(
            purchase_id=self.id,
            company_id=self.company_id,
            supplier_id=self.supplier_id,
            total=self.total,
            payment_condition=self.payment_condition,
            items=event_items,
            occurred_at=actual_timestamp
        )
        self.registrar_evento(evento_compra)

    def annul(self, timestamp: datetime = None, voided_by: UUID = None, void_reason: str = None) -> None:
        if self.status.valor != "REGISTRADA":
            raise CompraInvalidaException("Solo se pueden anular compras en estado REGISTRADA.")
        self.status = EstadoCompra.anulada()
        actual_timestamp = timestamp or datetime.now()
        self.updated_at = actual_timestamp
        self.validate()

        # Record CompraAnulada domain event
        from app.modules.compra.domain.events.compra_events import CompraAnulada
        evento_anulacion = CompraAnulada(
            purchase_id=self.id,
            company_id=self.company_id,
            supplier_id=self.supplier_id,
            occurred_at=actual_timestamp,
            voided_by=voided_by,
            void_reason=void_reason
        )
        self.registrar_evento(evento_anulacion)

    def devolver_proveedor(self, timestamp: datetime = None, items_returned: list = None) -> None:
        """
        Registra una devolucion al proveedor, disparando el evento CompraDevueltaProveedor.
        """
        if self.status.valor != "REGISTRADA":
            raise CompraInvalidaException("Solo se pueden realizar devoluciones sobre compras en estado REGISTRADA.")
        
        actual_timestamp = timestamp or datetime.now()
        items_returned = items_returned or []
        
        event_items = []
        for item in items_returned:
            prod_id = item["product_id"]
            qty_val = item["quantity"].valor if isinstance(item["quantity"], Cantidad) else Decimal(str(item["quantity"]))
            
            matching_detail = next((d for d in self.items if d.product_id == prod_id), None)
            if not matching_detail:
                raise CompraInvalidaException(f"El producto '{prod_id}' no pertenece a las lineas de esta compra.")
            
            if qty_val > matching_detail.quantity.valor:
                raise CompraInvalidaException(
                    f"La cantidad a devolver ({qty_val}) supera la cantidad comprada ({matching_detail.quantity.valor}) para el producto '{prod_id}'."
                )

            event_items.append({
                "product_id": prod_id,
                "quantity": Cantidad(qty_val),
                "unit_cost": matching_detail.unit_cost
            })

        # Record CompraDevueltaProveedor event
        from app.modules.compra.domain.events.compra_events import CompraDevueltaProveedor
        evento_devolucion = CompraDevueltaProveedor(
            purchase_id=self.id,
            company_id=self.company_id,
            supplier_id=self.supplier_id,
            items=event_items,
            occurred_at=actual_timestamp
        )
        self.registrar_evento(evento_devolucion)

    @property
    def subtotal(self) -> Dinero:
        """Suma de las lineas de detalle utilizando VO Dinero."""
        return sum((item.line_total for item in self.items), Dinero.cero())

    @property
    def tax(self) -> Dinero:
        """Impuesto (ej. 0% por defecto en compras)."""
        return Dinero.cero()

    @property
    def total(self) -> Dinero:
        """Suma de subtotal y tax en VO Dinero."""
        return self.subtotal.sumar(self.tax)
