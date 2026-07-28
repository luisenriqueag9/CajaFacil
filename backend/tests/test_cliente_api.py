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

    # Prepopulate company
    comp_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    session.add(Company(
        id=comp_id,
        business_name="Empresa Test Clientes",
        trade_name="Empresa Test Clientes",
        tax_id="12345678-0",
        email="test@clientes.com",
        currency="USD",
        timezone="UTC",
        status="ACTIVE"
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

def test_client_api_lifecycle(client):
    company_id = "11111111-1111-1111-1111-11111111111a"

    # 1. Creacion exitosa (POST /api/v1/clientes)
    payload = {
        "company_id": company_id,
        "name": "Cliente API Test",
        "tax_id": "TAX-API-99",
        "phone": "555-9000",
        "email": "api@cliente.com"
    }

    response = client.post("/api/v1/clientes", json=payload)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["message"] == "Cliente registrado correctamente."
    
    cliente = json_data["data"]
    client_id = cliente["id"]
    assert cliente["status"] == "ACTIVO"
    assert cliente["name"] == "Cliente API Test"

    # 2. Conflicto por duplicidad (409 Conflict)
    response_dup = client.post("/api/v1/clientes", json=payload)
    assert response_dup.status_code == 409
    assert response_dup.json()["success"] is False
    assert response_dup.json()["error_code"] == "CLIENTE_YA_EXISTE"

    # 3. Error de validacion (422 Unprocessable Entity)
    invalid_payload = payload.copy()
    invalid_payload["name"] = "A" # Name too short (<2 chars)
    response_val = client.post("/api/v1/clientes", json=invalid_payload)
    assert response_val.status_code == 422

    # 4. Consulta (GET /api/v1/clientes/{id})
    response_get = client.get(f"/api/v1/clientes/{client_id}")
    assert response_get.status_code == 200
    assert response_get.json()["success"] is True
    assert response_get.json()["data"]["id"] == client_id

    # Recurso inexistente (404 Not Found)
    non_existent_uuid = str(uuid.uuid4())
    response_404 = client.get(f"/api/v1/clientes/{non_existent_uuid}")
    assert response_404.status_code == 404
    assert response_404.json()["success"] is False
    assert response_404.json()["error_code"] == "CLIENTE_NO_ENCONTRADO"

    # 5. Listado (GET /api/v1/clientes)
    response_list = client.get(f"/api/v1/clientes?company_id={company_id}")
    assert response_list.status_code == 200
    assert response_list.json()["success"] is True
    assert len(response_list.json()["data"]) == 1

    # 6. Actualizacion (PUT /api/v1/clientes/{id})
    update_payload = {
        "name": "Cliente API Modificado",
        "tax_id": "TAX-API-99",
        "phone": "555-9001",
        "email": "modified@cliente.com"
    }
    response_put = client.put(f"/api/v1/clientes/{client_id}", json=update_payload)
    assert response_put.status_code == 200
    assert response_put.json()["success"] is True
    assert response_put.json()["data"]["name"] == "Cliente API Modificado"
    assert response_put.json()["data"]["phone"] == "555-9001"

    # 7. Inactivacion (POST /api/v1/clientes/{id}/inactivar)
    response_deac = client.post(f"/api/v1/clientes/{client_id}/inactivar")
    assert response_deac.status_code == 200
    assert response_deac.json()["success"] is True
    assert response_deac.json()["data"]["status"] == "INACTIVO"
