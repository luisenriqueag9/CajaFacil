import pytest
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from app.modules.compra.domain.aggregates.compra import Compra
from app.modules.compra.domain.entities.detalle_compra import DetalleCompra
from app.modules.compra.domain.value_objects.cantidad import Cantidad
from app.modules.compra.domain.value_objects.dinero import Dinero
from app.modules.compra.domain.value_objects.estado_compra import EstadoCompra
from app.modules.compra.domain.value_objects.numero_compra import NumeroCompra
from app.modules.compra.infrastructure.persistence.mappers.compra_mapper import CompraMapper

def test_mapper_symmetric_cycle():
    # 1. Arrange: Create a domain aggregate Compra with complex state and details
    purchase_id = uuid.uuid4()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product_id_1 = uuid.uuid4()
    product_id_2 = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # Use factory method to create a registered purchase
    items_payload = [
        {"product_id": product_id_1, "quantity": Decimal("10.5000"), "unit_cost": Decimal("25.3000")},
        {"product_id": product_id_2, "quantity": Decimal("5.0000"), "unit_cost": Decimal("100.0000")}
    ]

    original_domain = Compra.register(
        id=purchase_id,
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-TEST-MAPPING",
        payment_condition="CREDITO",
        issue_date=now,
        created_at=now,
        updated_at=now,
        items_payload=items_payload
    )

    # 2. Act: Map domain -> database model
    db_model = CompraMapper.to_db(original_domain)

    # Assert db model attributes are correct primitive values
    assert db_model.id == purchase_id
    assert db_model.company_id == company_id
    assert db_model.supplier_id == supplier_id
    assert db_model.invoice_number == "FACT-TEST-MAPPING"
    assert db_model.payment_condition == "CREDITO"
    assert db_model.status == "REGISTRADA"
    assert len(db_model.details) == 2

    # Map database model -> domain aggregate
    reconstructed_domain = CompraMapper.to_domain(db_model)

    # 3. Assert: Verify the symmetric cycle preserves all states, invariants, and value objects
    assert reconstructed_domain.id == original_domain.id
    assert reconstructed_domain.company_id == original_domain.company_id
    assert reconstructed_domain.supplier_id == original_domain.supplier_id
    assert reconstructed_domain.invoice_number == original_domain.invoice_number
    assert reconstructed_domain.payment_condition == original_domain.payment_condition
    assert reconstructed_domain.status == original_domain.status
    assert reconstructed_domain.created_at == original_domain.created_at
    assert reconstructed_domain.updated_at == original_domain.updated_at
    assert len(reconstructed_domain.items) == len(original_domain.items)

    # Verify totals
    assert reconstructed_domain.subtotal == original_domain.subtotal
    assert reconstructed_domain.tax == original_domain.tax
    assert reconstructed_domain.total == original_domain.total

    # Verify individual items details and types
    item_reconstructed = reconstructed_domain.items[0]
    item_original = original_domain.items[0]

    assert item_reconstructed.id == item_original.id
    assert item_reconstructed.purchase_id == item_original.purchase_id
    assert item_reconstructed.product_id == item_original.product_id
    
    # Types must be proper Value Objects
    assert isinstance(item_reconstructed.quantity, Cantidad)
    assert isinstance(item_reconstructed.unit_cost, Dinero)
    assert item_reconstructed.quantity == item_original.quantity
    assert item_reconstructed.unit_cost == item_original.unit_cost
    assert item_reconstructed.line_total == item_original.line_total
