import pytest
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.database.session import get_db

# Import models to register them in Sqlite metadata
from app.modules.company.data.models import Company
from app.modules.supplier.data.models import Supplier
from app.modules.product.data.models import Product
from app.modules.brand.data.models import Brand
from app.modules.category.data.models import Category
from app.modules.unit.data.models import Unit
from app.modules.compra.infrastructure.persistence.models.compra_model import Compra, DetalleCompra

@pytest.fixture(name="db_session")
def db_session_fixture():
    # Use StaticPool to share the in-memory SQLite connection across threads
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Prepopulate tables
    comp_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    supp_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    brand_id = uuid.UUID("33333333-3333-3333-3333-33333333333c")
    cat_id = uuid.UUID("44444444-4444-4444-4444-44444444444d")
    unit_id = uuid.UUID("55555555-5555-5555-5555-55555555555e")
    prod_id = uuid.UUID("66666666-6666-6666-6666-66666666666f")

    session.add(Company(
        id=comp_id,
        business_name="Empresa Test",
        trade_name="Empresa Test",
        tax_id="12345678-9",
        email="test@empresa.com",
        currency="USD",
        timezone="UTC",
        status="ACTIVE"
    ))
    session.add(Supplier(
        id=supp_id,
        company_id=comp_id,
        name="Proveedor Test",
        tax_id="8888-8",
        status="ACTIVO"
    ))
    session.add(Brand(id=brand_id, company_id=comp_id, name="Marca Test", status="ACTIVE"))
    session.add(Category(id=cat_id, company_id=comp_id, name="Cat Test", status="ACTIVE"))
    session.add(Unit(id=unit_id, company_id=comp_id, code="UN01", name="Unit Test", abbreviation="UN", allows_decimal=True, status="ACTIVE"))
    session.add(Product(
        id=prod_id,
        company_id=comp_id,
        internal_code="PROD-01",
        name="Producto Test",
        category_id=cat_id,
        brand_id=brand_id,
        unit_id=unit_id,
        cost=Decimal("10.00"),
        price=Decimal("15.00"),
        tax_rate=Decimal("15.00"),
        status="ACTIVO"
    ))
    session.commit()
    yield session
    session.close()

@pytest.fixture(name="client")
def client_fixture(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_purchase_api_lifecycle(client):
    company_id = "11111111-1111-1111-1111-11111111111a"
    supplier_id = "22222222-2222-2222-2222-22222222222b"
    product_id = "66666666-6666-6666-6666-66666666666f"

    # 1. Creacion exitosa (POST /api/v1/compras)
    payload = {
        "company_id": company_id,
        "supplier_id": supplier_id,
        "invoice_number": "FACT-1001",
        "payment_condition": "CREDITO",
        "issue_date": datetime.now(timezone.utc).isoformat(),
        "items": [
            {
                "product_id": product_id,
                "quantity": 10.0000,
                "unit_cost": 25.0000
            }
        ]
    }
    
    response = client.post("/api/v1/compras", json=payload)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["message"] == "Compra registrada correctamente."
    
    compra = json_data["data"]
    purchase_id = compra["id"]
    assert compra["status"] == "REGISTRADA"
    assert float(compra["total"]) == 250.0

    # 2. Conflicto por duplicidad (409 Conflict)
    # Volver a registrar la misma factura para el mismo proveedor debe fallar con 409
    response_dup = client.post("/api/v1/compras", json=payload)
    assert response_dup.status_code == 409
    assert response_dup.json()["success"] is False
    assert response_dup.json()["error_code"] == "COMPRA_YA_EXISTE"

    # 3. Errores de validacion (422 Unprocesssable Entity)
    invalid_payload = payload.copy()
    invalid_payload["invoice_number"] = "" # Invalid empty string
    response_val = client.post("/api/v1/compras", json=invalid_payload)
    assert response_val.status_code == 422

    # 4. Consulta (GET /api/v1/compras/{id})
    response_get = client.get(f"/api/v1/compras/{purchase_id}")
    assert response_get.status_code == 200
    assert response_get.json()["success"] is True
    assert response_get.json()["data"]["id"] == purchase_id

    # Recurso inexistente (404 Not Found)
    non_existent_uuid = str(uuid.uuid4())
    response_404 = client.get(f"/api/v1/compras/{non_existent_uuid}")
    assert response_404.status_code == 404
    assert response_404.json()["success"] is False
    assert response_404.json()["error_code"] == "COMPRA_NO_ENCONTRADA"

    # 5. Listado (GET /api/v1/compras)
    response_list = client.get(f"/api/v1/compras?company_id={company_id}")
    assert response_list.status_code == 200
    assert response_list.json()["success"] is True
    assert len(response_list.json()["data"]) == 1

    # 6. Devolucion (POST /api/v1/compras/{id}/devolucion)
    return_payload = {
        "items": [
            {
                "product_id": product_id,
                "quantity": 4.0000
            }
        ]
    }
    response_ret = client.post(f"/api/v1/compras/{purchase_id}/devolucion", json=return_payload)
    assert response_ret.status_code == 200
    assert response_ret.json()["success"] is True
    assert response_ret.json()["data"]["status"] == "REGISTRADA"

    # Devolución por excedente (400 Bad Request / Validation error)
    excess_payload = {
        "items": [
            {
                "product_id": product_id,
                "quantity": 11.0000 # Total returned would be 11, exceeding the purchased 10
            }
        ]
    }
    response_excess = client.post(f"/api/v1/compras/{purchase_id}/devolucion", json=excess_payload)
    assert response_excess.status_code == 400
    assert response_excess.json()["success"] is False

    # 7. Anulación (POST /api/v1/compras/{id}/anular)
    annul_payload = {
        "void_reason": "Anulacion por pruebas"
    }
    response_annul = client.post(f"/api/v1/compras/{purchase_id}/anular", json=annul_payload)
    assert response_annul.status_code == 200
    assert response_annul.json()["success"] is True
    assert response_annul.json()["data"]["status"] == "ANULADA"
