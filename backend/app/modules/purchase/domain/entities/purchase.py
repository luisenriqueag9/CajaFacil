from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import uuid
from app.modules.purchase.domain.exceptions.invalid_purchase_exception import InvalidPurchaseException
from app.modules.purchase.domain.entities.purchase_detail import PurchaseDetail

@dataclass
class Purchase:
    id: UUID
    company_id: UUID
    supplier_id: UUID
    invoice_number: str
    payment_condition: str
    issue_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    items: list[PurchaseDetail] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.validate()

    @classmethod
    def create_draft(
        cls, 
        id: UUID, 
        company_id: UUID, 
        supplier_id: UUID, 
        invoice_number: str, 
        payment_condition: str, 
        issue_date: datetime,
        created_at: datetime,
        updated_at: datetime
    ) -> "Purchase":
        """
        Factory method to initialize a purchase in DRAFT status.
        """
        return cls(
            id=id,
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number=invoice_number,
            payment_condition=payment_condition,
            issue_date=issue_date,
            status="BORRADOR",
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
        invoice_number: str, 
        payment_condition: str, 
        issue_date: datetime,
        created_at: datetime,
        updated_at: datetime,
        items_payload: list[dict]
    ) -> "Purchase":
        """
        Factory method to register and confirm a purchase directly with its items.
        """
        purchase = cls(
            id=id,
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number=invoice_number,
            payment_condition=payment_condition,
            issue_date=issue_date,
            status="CONFIRMADA",
            created_at=created_at,
            updated_at=updated_at,
            items=[]
        )
        
        # Populate details
        if not items_payload:
            raise InvalidPurchaseException("Una compra confirmada no puede crearse sin líneas de detalle.")

        # Apply V1 consolidator business policy: collapse duplicate products in items payload
        consolidated = {}
        for item in items_payload:
            product_id = item["product_id"]
            quantity = float(item["quantity"])
            unit_cost = float(item["unit_cost"])
            
            if product_id in consolidated:
                prev_qty, prev_cost = consolidated[product_id]
                total_qty = prev_qty + quantity
                if total_qty > 0:
                    weighted_cost = ((prev_qty * prev_cost) + (quantity * unit_cost)) / total_qty
                else:
                    weighted_cost = unit_cost
                consolidated[product_id] = (total_qty, weighted_cost)
            else:
                consolidated[product_id] = (quantity, unit_cost)

        for prod_id, (qty, cost) in consolidated.items():
            detail = PurchaseDetail(
                id=uuid.uuid4(),
                purchase_id=id,
                product_id=prod_id,
                quantity=qty,
                unit_cost=cost
            )
            purchase.items.append(detail)

        purchase.validate()
        return purchase

    def add_item(self, product_id: UUID, quantity: float, unit_cost: float) -> None:
        if self.status != "BORRADOR":
            raise InvalidPurchaseException("No se pueden añadir ítems a una compra que no esté en estado BORRADOR.")
        
        # Check if product is already in items, consolidate according to V1 policy
        for item in self.items:
            if item.product_id == product_id:
                total_qty = item.quantity + quantity
                if total_qty > 0:
                    weighted_cost = ((item.quantity * item.unit_cost) + (quantity * unit_cost)) / total_qty
                else:
                    weighted_cost = unit_cost
                item.quantity = total_qty
                item.unit_cost = weighted_cost
                item.validate()
                return

        detail = PurchaseDetail(
            id=uuid.uuid4(),
            purchase_id=self.id,
            product_id=product_id,
            quantity=quantity,
            unit_cost=unit_cost
        )
        self.items.append(detail)

    def remove_item(self, product_id: UUID) -> None:
        if self.status != "BORRADOR":
            raise InvalidPurchaseException("No se pueden remover ítems de una compra que no esté en estado BORRADOR.")
        self.items = [item for item in self.items if item.product_id != product_id]

    def confirm(self) -> None:
        if self.status != "BORRADOR":
            raise InvalidPurchaseException("La compra ya se encuentra confirmada o anulada.")
        if not self.items:
            raise InvalidPurchaseException("No se puede confirmar una compra sin líneas de detalle.")
        self.status = "CONFIRMADA"
        self.validate()

    def annul(self) -> None:
        if self.status != "CONFIRMADA":
            raise InvalidPurchaseException("Solo se pueden anular compras en estado CONFIRMADA.")
        self.status = "ANULADA"
        self.validate()

    def validate(self) -> None:
        if not self.company_id:
            raise InvalidPurchaseException("La compra debe pertenecer a una empresa (company_id es requerido).")
        if not self.supplier_id:
            raise InvalidPurchaseException("El proveedor es obligatorio.")
        if not self.invoice_number or not self.invoice_number.strip():
            raise InvalidPurchaseException("El número de factura no puede estar vacío.")
        
        valid_conditions = {"CONTADO", "CREDITO"}
        if self.payment_condition not in valid_conditions:
            raise InvalidPurchaseException(
                f"Condición de pago '{self.payment_condition}' inválida. Debe ser CONTADO o CREDITO."
            )
            
        valid_statuses = {"BORRADOR", "CONFIRMADA", "ANULADA"}
        if self.status not in valid_statuses:
            raise InvalidPurchaseException(
                f"Estado '{self.status}' no permitido."
            )

    @property
    def subtotal(self) -> float:
        """Derived value representing sum of lines."""
        return sum(item.line_total for item in self.items)

    @property
    def tax(self) -> float:
        """Derived value representing tax (e.g. 15% standard rate)."""
        return 0.0

    @property
    def total(self) -> float:
        """Derived value representing grand total (subtotal + tax)."""
        return self.subtotal + self.tax
