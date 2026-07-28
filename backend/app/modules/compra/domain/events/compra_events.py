from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import List, Dict, Any

from app.modules.compra.domain.value_objects.cantidad import Cantidad
from app.modules.compra.domain.value_objects.dinero import Dinero

@dataclass(frozen=True)
class CompraRegistrada:
    purchase_id: UUID
    company_id: UUID
    supplier_id: UUID
    total: Dinero
    payment_condition: str
    items: List[Dict[str, Any]]  # list of {"product_id": UUID, "quantity": Cantidad, "unit_cost": Dinero}
    occurred_at: datetime

@dataclass(frozen=True)
class CompraAnulada:
    purchase_id: UUID
    company_id: UUID
    supplier_id: UUID
    occurred_at: datetime
    voided_by: UUID | None = None
    void_reason: str | None = None

@dataclass(frozen=True)
class CompraDevueltaProveedor:
    purchase_id: UUID
    company_id: UUID
    supplier_id: UUID
    items: List[Dict[str, Any]]  # list of {"product_id": UUID, "quantity": Cantidad, "unit_cost": Dinero}
    occurred_at: datetime

@dataclass(frozen=True)
class CostoProductoActualizado:
    company_id: UUID
    product_id: UUID
    new_cost: Dinero
    occurred_at: datetime
