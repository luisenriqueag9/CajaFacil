import pytest
import uuid
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.modules.company.data.models import Company
from app.modules.cliente.infrastructure.persistence.models.cliente_model import Cliente

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

    # Prepopulate company and client
    comp_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    session.add(Company(
        id=comp_id,
        business_name="Empresa Test Credito",
        trade_name="Empresa Test Credito",
        tax_id="12345678-0",
        email="test@creditos.com",
        currency="USD",
        timezone="UTC",
        status="ACTIVE"
    ))
    session.flush()

    client_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    session.add(Cliente(
        id=client_id,
        company_id=comp_id,
        name="Cliente Con Credito",
        tax_id="TAX-CRED-99",
        phone="555-5000",
        email="credito@client.com",
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

def test_credit_api_lifecycle(client):
    company_id = "11111111-1111-1111-1111-11111111111a"
    client_id = "22222222-2222-2222-2222-22222222222b"

    # 1. Apertura de cuenta exitosa (POST /api/v1/creditos)
    payload = {
        "company_id": company_id,
        "client_id": client_id,
        "credit_limit": 3500.00
    }

    response = client.post("/api/v1/creditos", json=payload)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["message"] == "Cuenta de credito abierta correctamente."
    
    credit = json_data["data"]
    credit_id = credit["id"]
    assert credit["status"] == "ACTIVO"
    assert float(credit["credit_limit"]) == 3500.00
    assert float(credit["balance"]) == 0.00

    # 2. Conflicto por duplicidad (409 Conflict)
    response_dup = client.post("/api/v1/creditos", json=payload)
    assert response_dup.status_code == 409
    assert response_dup.json()["success"] is False
    assert response_dup.json()["error_code"] == "CREDITO_YA_EXISTE"

    # 3. Consulta (GET /api/v1/creditos/{id})
    response_get = client.get(f"/api/v1/creditos/{credit_id}")
    assert response_get.status_code == 200
    assert response_get.json()["success"] is True
    assert response_get.json()["data"]["id"] == credit_id

    # Recurso inexistente (404 Not Found)
    non_existent_uuid = str(uuid.uuid4())
    response_404 = client.get(f"/api/v1/creditos/{non_existent_uuid}")
    assert response_404.status_code == 404
    assert response_404.json()["success"] is False
    assert response_404.json()["error_code"] == "CREDITO_NO_ENCONTRADO"

    # 4. Listado (GET /api/v1/creditos)
    response_list = client.get(f"/api/v1/creditos?company_id={company_id}")
    assert response_list.status_code == 200
    assert response_list.json()["success"] is True
    assert len(response_list.json()["data"]) == 1

    # 5. Actualizacion de limite (PUT /api/v1/creditos/{id}/limite)
    update_payload = {
        "new_limit": 4500.00
    }
    response_put = client.put(f"/api/v1/creditos/{credit_id}/limite", json=update_payload)
    assert response_put.status_code == 200
    assert response_put.json()["success"] is True
    assert float(response_put.json()["data"]["credit_limit"]) == 4500.00

    # 6. Inactivacion (POST /api/v1/creditos/{id}/inactivar)
    response_deac = client.post(f"/api/v1/creditos/{credit_id}/inactivar")
    assert response_deac.status_code == 200
    assert response_deac.json()["success"] is True
    assert response_deac.json()["data"]["status"] == "SUSPENDIDO"
