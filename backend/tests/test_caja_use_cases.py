import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone

from app.modules.caja.domain.aggregates.sesion_caja import SesionCaja
from app.modules.caja.domain.entities.caja import Caja
from app.modules.caja.domain.entities.movimiento_caja import MovimientoCaja
from app.modules.caja.domain.entities.arqueo_caja import ArqueoCaja
from app.modules.caja.domain.value_objects.estado_sesion import EstadoSesion
from app.modules.caja.domain.value_objects.tipo_movimiento import TipoMovimiento
from app.modules.caja.domain.value_objects.metodo_pago import MetodoPago
from app.modules.caja.domain.value_objects.dinero import Dinero
from app.modules.caja.domain.exceptions import (
    CajaCerradaException,
    CajaYaAbiertaException,
    CajaNoAbiertaException,
    MontoInvalidoException,
    CajaNotFoundException,
    SesionCajaNotFoundException
)
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.domain.repositories.sesion_caja_repository import SesionCajaRepository
from app.modules.caja.application.ports.unit_of_work import UnitOfWork
from app.modules.caja.application.use_cases import (
    AbrirSesionUseCase,
    AbrirSesionCommand,
    RegistrarMovimientoUseCase,
    RegistrarMovimientoCommand,
    RegistrarArqueoUseCase,
    RegistrarArqueoCommand,
    CerrarSesionUseCase,
    CerrarSesionCommand,
    AnularMovimientoUseCase,
    AnularMovimientoCommand,
    ObtenerSesionUseCase,
    ObtenerSesionQuery,
    ListarSesionesUseCase,
    ListarSesionesQuery
)
from app.common.event_dispatcher import EventDispatcher

# ==========================================
# IN-MEMORY REPOSITORIES FOR CAJA & SESION
# ==========================================

class InMemoryCajaRepository(CajaRepository):
    def __init__(self):
        self.cajas = {}
    def create(self, caja: Caja) -> Caja:
        self.cajas[caja.id] = caja
        return caja
    def get_by_id(self, caja_id: uuid.UUID) -> Caja | None:
        return self.cajas.get(caja_id)
    def get_all(self, company_id: uuid.UUID) -> list[Caja]:
        return [c for c in self.cajas.values() if c.company_id == company_id]

class InMemorySesionCajaRepository(SesionCajaRepository):
    def __init__(self):
        self.sessions = {}
    def create(self, sesion: SesionCaja) -> SesionCaja:
        self.sessions[sesion.id] = sesion
        return sesion
    def get_by_id(self, sesion_id: uuid.UUID) -> SesionCaja | None:
        return self.sessions.get(sesion_id)
    def get_active_by_user(self, company_id: uuid.UUID, user_id: uuid.UUID) -> SesionCaja | None:
        for s in self.sessions.values():
            if s.company_id == company_id and s.user_id == user_id and s.status.is_abierta:
                return s
        return None
    def get_active_by_caja(self, company_id: uuid.UUID, caja_id: uuid.UUID) -> SesionCaja | None:
        for s in self.sessions.values():
            if s.company_id == company_id and s.caja_id == caja_id and s.status.is_abierta:
                return s
        return None
    def get_all(self, company_id: uuid.UUID, status: str | None = None) -> list[SesionCaja]:
        res = []
        for s in self.sessions.values():
            if s.company_id == company_id:
                if status is None or s.status.valor == status:
                    res.append(s)
        return res
    def update(self, sesion: SesionCaja) -> SesionCaja:
        self.sessions[sesion.id] = sesion
        return sesion

class DummyUnitOfWork(UnitOfWork):
    def __enter__(self) -> "DummyUnitOfWork":
        return self
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
    def commit(self) -> None:
        pass
    def rollback(self) -> None:
        pass

class SpyEventDispatcher(EventDispatcher):
    def __init__(self):
        self.events = []
    def dispatch(self, event) -> None:
        self.events.append(event)

# ==========================================
# TEST FIXTURES
# ==========================================

@pytest.fixture
def test_setup():
    caja_repo = InMemoryCajaRepository()
    sesion_repo = InMemorySesionCajaRepository()
    uow = DummyUnitOfWork()
    dispatcher = SpyEventDispatcher()
    
    company_id = uuid.uuid4()
    caja_id = uuid.uuid4()
    caja_repo.create(Caja(caja_id, company_id, "Caja 01", "ACTIVA", datetime.now()))

    return {
        "caja_repo": caja_repo,
        "sesion_repo": sesion_repo,
        "uow": uow,
        "dispatcher": dispatcher,
        "company_id": company_id,
        "caja_id": caja_id
    }

# ==========================================
# GRANULAR TEST CASES
# ==========================================

def test_abrir_sesion_exitoso(test_setup):
    abrir_case = AbrirSesionUseCase(test_setup["sesion_repo"], test_setup["caja_repo"], test_setup["uow"], test_setup["dispatcher"])
    user_id = uuid.uuid4()

    dto = abrir_case.execute(AbrirSesionCommand(test_setup["caja_id"], test_setup["company_id"], user_id, Decimal("500.00")))
    assert dto.status == "ABIERTA"
    assert dto.opening_balance == Decimal("500.00")
    assert len(test_setup["dispatcher"].events) == 1

def test_abrir_sesion_caja_inexistente(test_setup):
    abrir_case = AbrirSesionUseCase(test_setup["sesion_repo"], test_setup["caja_repo"], test_setup["uow"], test_setup["dispatcher"])
    with pytest.raises(CajaNotFoundException):
        abrir_case.execute(AbrirSesionCommand(uuid.uuid4(), test_setup["company_id"], uuid.uuid4(), Decimal("500.00")))

def test_abrir_sesion_ya_activa_usuario(test_setup):
    abrir_case = AbrirSesionUseCase(test_setup["sesion_repo"], test_setup["caja_repo"], test_setup["uow"], test_setup["dispatcher"])
    user_id = uuid.uuid4()
    
    # First session
    abrir_case.execute(AbrirSesionCommand(test_setup["caja_id"], test_setup["company_id"], user_id, Decimal("500.00")))
    
    # Second box for same user
    another_caja_id = uuid.uuid4()
    test_setup["caja_repo"].create(Caja(another_caja_id, test_setup["company_id"], "Caja 02", "ACTIVA", datetime.now()))
    
    with pytest.raises(CajaYaAbiertaException):
        abrir_case.execute(AbrirSesionCommand(another_caja_id, test_setup["company_id"], user_id, Decimal("100.00")))

def test_abrir_sesion_caja_ya_ocupada(test_setup):
    abrir_case = AbrirSesionUseCase(test_setup["sesion_repo"], test_setup["caja_repo"], test_setup["uow"], test_setup["dispatcher"])
    user1 = uuid.uuid4()
    user2 = uuid.uuid4()
    
    abrir_case.execute(AbrirSesionCommand(test_setup["caja_id"], test_setup["company_id"], user1, Decimal("500.00")))
    
    with pytest.raises(CajaYaAbiertaException):
        abrir_case.execute(AbrirSesionCommand(test_setup["caja_id"], test_setup["company_id"], user2, Decimal("100.00")))

def test_registrar_movimientos(test_setup):
    abrir_case = AbrirSesionUseCase(test_setup["sesion_repo"], test_setup["caja_repo"], test_setup["uow"], test_setup["dispatcher"])
    mov_case = RegistrarMovimientoUseCase(test_setup["sesion_repo"], test_setup["uow"], test_setup["dispatcher"])
    
    sesion_dto = abrir_case.execute(AbrirSesionCommand(test_setup["caja_id"], test_setup["company_id"], uuid.uuid4(), Decimal("100.00")))
    
    # Registrar ingreso
    dto = mov_case.execute(RegistrarMovimientoCommand(sesion_dto.id, "INGRESO", Decimal("50.00"), "EFECTIVO", "VENTA"))
    assert len(dto.movements) == 1
    assert dto.movements[0].type == "INGRESO"
    assert dto.movements[0].amount == Decimal("50.00")
    
    # Registrar egreso
    dto = mov_case.execute(RegistrarMovimientoCommand(sesion_dto.id, "EGRESO", Decimal("30.00"), "EFECTIVO", "RETIRO"))
    assert len(dto.movements) == 2
    assert dto.movements[1].type == "EGRESO"
    assert dto.movements[1].amount == Decimal("30.00")

def test_arqueo_con_diferencias(test_setup):
    abrir_case = AbrirSesionUseCase(test_setup["sesion_repo"], test_setup["caja_repo"], test_setup["uow"], test_setup["dispatcher"])
    mov_case = RegistrarMovimientoUseCase(test_setup["sesion_repo"], test_setup["uow"], test_setup["dispatcher"])
    arq_case = RegistrarArqueoUseCase(test_setup["sesion_repo"], test_setup["uow"], test_setup["dispatcher"])
    
    sesion_dto = abrir_case.execute(AbrirSesionCommand(test_setup["caja_id"], test_setup["company_id"], uuid.uuid4(), Decimal("1000.00")))
    
    # Cash movements
    mov_case.execute(RegistrarMovimientoCommand(sesion_dto.id, "INGRESO", Decimal("300.00"), "EFECTIVO", "VENTA"))
    # Card movement (does not count towards physical cash!)
    mov_case.execute(RegistrarMovimientoCommand(sesion_dto.id, "INGRESO", Decimal("500.00"), "TARJETA", "VENTA"))
    
    # Theoretical cash = 1000 + 300 = 1300.
    # Physical audit count = 1290. Difference = -10 (faltante).
    dto = arq_case.execute(RegistrarArqueoCommand(sesion_dto.id, Decimal("1290.00"), None))
    assert len(dto.audits) == 1
    assert dto.audits[0].difference == Decimal("-10.00")
    assert dto.audits[0].system_amount == Decimal("1300.00")

def test_anular_movimiento_por_contramovimiento(test_setup):
    abrir_case = AbrirSesionUseCase(test_setup["sesion_repo"], test_setup["caja_repo"], test_setup["uow"], test_setup["dispatcher"])
    mov_case = RegistrarMovimientoUseCase(test_setup["sesion_repo"], test_setup["uow"], test_setup["dispatcher"])
    anular_case = AnularMovimientoUseCase(test_setup["sesion_repo"], test_setup["uow"], test_setup["dispatcher"])
    
    sesion_dto = abrir_case.execute(AbrirSesionCommand(test_setup["caja_id"], test_setup["company_id"], uuid.uuid4(), Decimal("100.00")))
    
    dto = mov_case.execute(RegistrarMovimientoCommand(sesion_dto.id, "INGRESO", Decimal("50.00"), "EFECTIVO", "GASTO"))
    mov_id = dto.movements[0].id
    
    dto = anular_case.execute(AnularMovimientoCommand(sesion_dto.id, mov_id))
    assert dto.movements[0].voided is True
    assert len(dto.movements) == 2
    # The contramovement
    assert dto.movements[1].type == "EGRESO"
    assert dto.movements[1].concept == "ANULACION - GASTO"
    assert dto.movements[1].amount == Decimal("50.00")

def test_cierre_sesion_inabilita_modificaciones(test_setup):
    abrir_case = AbrirSesionUseCase(test_setup["sesion_repo"], test_setup["caja_repo"], test_setup["uow"], test_setup["dispatcher"])
    cerrar_case = CerrarSesionUseCase(test_setup["sesion_repo"], test_setup["uow"], test_setup["dispatcher"])
    mov_case = RegistrarMovimientoUseCase(test_setup["sesion_repo"], test_setup["uow"], test_setup["dispatcher"])
    
    sesion_dto = abrir_case.execute(AbrirSesionCommand(test_setup["caja_id"], test_setup["company_id"], uuid.uuid4(), Decimal("100.00")))
    
    # Close session
    dto = cerrar_case.execute(CerrarSesionCommand(sesion_dto.id))
    assert dto.status == "CERRADA"
    
    # Attempting to add movement should raise exception
    with pytest.raises(CajaCerradaException):
        mov_case.execute(RegistrarMovimientoCommand(sesion_dto.id, "INGRESO", Decimal("50.00"), "EFECTIVO", "VENTA"))
