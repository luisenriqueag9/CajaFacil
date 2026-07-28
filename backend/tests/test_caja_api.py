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
from app.modules.caja.infrastructure.persistence.models.caja_model import Caja

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

    # Prepopulate company and physical caja register
    comp_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    session.add(Company(
        id=comp_id,
        business_name="Empresa Test Caja",
        trade_name="Empresa Test Caja",
        tax_id="12345678-0",
        email="test@cajas.com",
        currency="NIO",
        timezone="UTC",
        status="ACTIVE"
    ))
    session.flush()

    caja_id = uuid.UUID("33333333-3333-3333-3333-33333333333c")
    session.add(Caja(
        id=caja_id,
        company_id=comp_id,
        name="Caja Registradora 01",
        status="ACTIVA",
        created_at=datetime.now(timezone.utc)
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

def test_caja_api_lifecycle(client):
    company_id = "11111111-1111-1111-1111-11111111111a"
    caja_id = "33333333-3333-3333-3333-33333333333c"
    user_id = str(uuid.uuid4())

    # 1. Abrir sesion (POST /api/v1/cajas/sesiones)
    payload_abrir = {
        "caja_id": caja_id,
        "company_id": company_id,
        "user_id": user_id,
        "opening_balance": 1000.00
    }
    response = client.post("/api/v1/cajas/sesiones", json=payload_abrir)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["success"] is True
    
    sesion = json_data["data"]
    sesion_id = sesion["id"]
    assert sesion["status"] == "ABIERTA"
    assert float(sesion["opening_balance"]) == 1000.00

    # 2. Registrar movimiento (POST /api/v1/cajas/sesiones/{sesion_id}/movimientos)
    payload_mov = {
        "type": "INGRESO",
        "amount": 250.00,
        "payment_method": "EFECTIVO",
        "concept": "VENTA DIRECTA",
        "origin_context": "Ventas",
        "origin_document_id": str(uuid.uuid4())
    }
    response_mov = client.post(f"/api/v1/cajas/sesiones/{sesion_id}/movimientos", json=payload_mov)
    assert response_mov.status_code == 201
    assert response_mov.json()["success"] is True
    assert len(response_mov.json()["data"]["movements"]) == 1
    movimiento_id = response_mov.json()["data"]["movements"][0]["id"]

    # 3. Registrar arqueo (POST /api/v1/cajas/sesiones/{sesion_id}/arqueos)
    payload_arq = {
        "physical_amount": 1250.00,
        "supervisor_id": str(uuid.uuid4())
    }
    response_arq = client.post(f"/api/v1/cajas/sesiones/{sesion_id}/arqueos", json=payload_arq)
    assert response_arq.status_code == 201
    assert response_arq.json()["success"] is True
    assert len(response_arq.json()["data"]["audits"]) == 1
    assert float(response_arq.json()["data"]["audits"][0]["difference"]) == 0.00

    # 4. Anular movimiento (POST /api/v1/cajas/sesiones/{sesion_id}/movimientos/{movimiento_id}/anular)
    response_anul = client.post(f"/api/v1/cajas/sesiones/{sesion_id}/movimientos/{movimiento_id}/anular")
    assert response_anul.status_code == 200
    assert response_anul.json()["success"] is True
    # Deberian haber 2 movimientos ahora: el original (anulado) y la anulacion contramovimiento
    assert len(response_anul.json()["data"]["movements"]) == 2
    assert response_anul.json()["data"]["movements"][0]["voided"] is True

    # 5. Obtener sesion por ID (GET /api/v1/cajas/sesiones/{sesion_id})
    response_get = client.get(f"/api/v1/cajas/sesiones/{sesion_id}")
    assert response_get.status_code == 200
    assert response_get.json()["success"] is True
    assert response_get.json()["data"]["id"] == sesion_id

    # 6. Listar sesiones (GET /api/v1/cajas/sesiones)
    response_list = client.get(f"/api/v1/cajas/sesiones?company_id={company_id}")
    assert response_list.status_code == 200
    assert response_list.json()["success"] is True
    assert len(response_list.json()["data"]) == 1

    # 7. Cerrar sesion (POST /api/v1/cajas/sesiones/{sesion_id}/cerrar)
    response_close = client.post(f"/api/v1/cajas/sesiones/{sesion_id}/cerrar")
    assert response_close.status_code == 200
    assert response_close.json()["success"] is True
    assert response_close.json()["data"]["status"] == "CERRADA"
