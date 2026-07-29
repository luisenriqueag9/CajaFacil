import pytest
import uuid
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.modules.company.data.models import Company
from app.modules.category.data.models import Category
from app.modules.brand.data.models import Brand
from app.modules.unit.data.models import Unit
from app.modules.product.data.models import Product

@pytest.fixture(name="db_session")
def db_session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Prepopulate tables
    comp_id = uuid.UUID("dc555b36-ede8-432c-a8b9-a31294c8308a")
    cat_id = uuid.UUID("c1000000-0000-0000-0000-000000000001")
    br_id = uuid.UUID("b1000000-0000-0000-0000-000000000001")
    u_id = uuid.UUID("a1000000-0000-0000-0000-000000000001")

    session.add(Company(
        id=comp_id,
        business_name="Pulpería El Centro",
        trade_name="El Centro",
        tax_id="08011997123456",
        email="elcentro@cajafacil.com",
        currency="HNL",
        timezone="UTC",
        status="ACTIVE"
    ))
    
    session.add(Category(
        id=cat_id,
        company_id=comp_id,
        name="General",
        status="ACTIVE"
    ))
    
    session.add(Brand(
        id=br_id,
        company_id=comp_id,
        name="General",
        status="ACTIVE"
    ))

    session.add(Unit(
        id=u_id,
        company_id=comp_id,
        code="UND",
        name="Unidad",
        abbreviation="und",
        allows_decimal=False,
        status="ACTIVE"
    ))

    # Add 2 products
    session.add(Product(
        id=uuid.UUID("e1000000-0000-0000-0000-000000000001"),
        company_id=comp_id,
        internal_code="001",
        barcode="001",
        name="Coca Cola 355ml",
        cost=Decimal("15.00"),
        price=Decimal("25.00"),
        tax_rate=Decimal("15.00"),
        controls_stock=True,
        allows_decimal=False,
        is_perishable=False,
        minimum_stock=Decimal("0.00"),
        status="ACTIVE",
        category_id=cat_id,
        brand_id=br_id,
        unit_id=u_id
    ))

    session.add(Product(
        id=uuid.UUID("e1000000-0000-0000-0000-000000000002"),
        company_id=comp_id,
        internal_code="002",
        barcode="002",
        name="Pan Blanco",
        cost=Decimal("10.00"),
        price=Decimal("18.00"),
        tax_rate=Decimal("15.00"),
        controls_stock=True,
        allows_decimal=False,
        is_perishable=False,
        minimum_stock=Decimal("0.00"),
        status="ACTIVE",
        category_id=cat_id,
        brand_id=br_id,
        unit_id=u_id
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

def test_pos_search_products_success(client):
    headers = {"X-Company-ID": "dc555b36-ede8-432c-a8b9-a31294c8308a"}
    
    # 1. Search with matching criteria
    response = client.get("/api/v1/pos/search-products?search=Coca", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert len(json_data["data"]) == 1
    assert json_data["data"][0]["name"] == "Coca Cola 355ml"
    assert json_data["data"][0]["code"] == "001"
    assert json_data["data"][0]["price"] == 25.0

    # 2. Search without query term (returns all active products)
    response = client.get("/api/v1/pos/search-products", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data["data"]) == 2

    # 3. Search with limit clamping
    response = client.get("/api/v1/pos/search-products?limit=1000", headers=headers)
    assert response.status_code == 200
    
    # 4. Search with non-matching term
    response = client.get("/api/v1/pos/search-products?search=NotExist", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data["data"]) == 0
