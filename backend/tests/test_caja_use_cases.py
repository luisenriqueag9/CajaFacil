import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.modules.caja.domain.entities.caja import Caja, MovimientoCaja, ArqueoCaja
from app.modules.caja.domain.exceptions import (
    CajaCerradaException,
    CajaYaAbiertaException,
    CajaNoAbiertaException,
    MontoInvalidoException
)
from app.modules.caja.application.use_cases import (
    AbrirCajaUseCase,
    AbrirCajaCommand,
    RegistrarMovimientoCajaUseCase,
    RegistrarMovimientoCajaCommand,
    RegistrarArqueoCajaUseCase,
    RegistrarArqueoCajaCommand,
    CerrarCajaUseCase,
    CerrarCajaCommand,
    ObtenerSaldoCajaUseCase,
    ObtenerCajaActivaUseCase
)
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.application.event_dispatcher import EventDispatcher
from app.modules.caja.domain.events.caja_events import (
    CajaAbierta,
    MovimientoCajaRegistrado,
    ArqueoRealizado,
    CajaCerrada
)

# ==========================================
# FAST IN-MEMORY REPOSITORY DOUBLE
# ==========================================

class InMemoryCajaRepository(CajaRepository):
    def __init__(self):
        self.sessions = {}

    def save(self, caja: Caja) -> Caja:
        self.sessions[caja.id] = caja
        return caja

    def get_by_id(self, caja_id: uuid.UUID) -> Caja | None:
        return self.sessions.get(caja_id)

    def get_active_by_user(self, company_id: uuid.UUID, user_id: uuid.UUID) -> Caja | None:
        for c in self.sessions.values():
            if c.company_id == company_id and c.user_id == user_id and c.status == "ABIERTA":
                return c
        return None

    def search(self, company_id: uuid.UUID, filters: dict) -> list[Caja]:
        result = []
        for c in self.sessions.values():
            if c.company_id == company_id:
                if "user_id" in filters and filters["user_id"] and c.user_id != filters["user_id"]:
                    continue
                if "status" in filters and filters["status"] and c.status != filters["status"]:
                    continue
                result.append(c)
        return sorted(result, key=lambda x: x.opened_at, reverse=True)


class DummySession:
    def begin_nested(self):
        class DummyNestedTrans:
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
        return DummyNestedTrans()
    def commit(self): pass
    def rollback(self): pass


# ==========================================
# DOMAIN INVARIANT TESTS
# ==========================================

def test_caja_domain_invariants():
    caja_id = uuid.uuid4()
    company_id = uuid.uuid4()
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # 1. Invariant: amount must be > 0
    with pytest.raises(MontoInvalidoException):
        MovimientoCaja(
            id=uuid.uuid4(),
            caja_id=caja_id,
            type="INGRESO",
            amount=Decimal("0.00"),
            payment_method="EFECTIVO",
            concept="VENTA",
            origin_document_id=None,
            created_at=now
        )

    # 2. Invariant: Invalid Enum type
    with pytest.raises(ValueError, match="Tipo de movimiento de caja inválido"):
        MovimientoCaja(
            id=uuid.uuid4(),
            caja_id=caja_id,
            type="TRANSFERENCIA_EGRESO",
            amount=Decimal("100.00"),
            payment_method="EFECTIVO",
            concept="VENTA",
            origin_document_id=None,
            created_at=now
        )


# ==========================================
# USE CASE UNIT TESTS
# ==========================================

def test_abrir_caja_happy_path():
    repo = InMemoryCajaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    user_id = uuid.uuid4()

    published_events = []
    dispatcher.subscribe(CajaAbierta, lambda ev: published_events.append(ev))

    use_case = AbrirCajaUseCase(repo, db, dispatcher)

    command = AbrirCajaCommand(
        company_id=company_id,
        user_id=user_id,
        opening_balance=Decimal("150.00")
    )

    caja = use_case.execute(command)
    assert caja.status == "ABIERTA"
    assert caja.opening_balance == Decimal("150.00")
    assert len(caja.movements) == 1
    assert caja.movements[0].concept == "FONDO_APERTURA"
    assert len(published_events) == 1
    assert published_events[0].opening_balance == Decimal("150.00")


def test_abrir_caja_already_open():
    repo = InMemoryCajaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    user_id = uuid.uuid4()

    use_case = AbrirCajaUseCase(repo, db, dispatcher)

    # First opening
    use_case.execute(AbrirCajaCommand(company_id, user_id, Decimal("50.00")))

    # Second opening (should raise since first is still active)
    with pytest.raises(CajaYaAbiertaException):
        use_case.execute(AbrirCajaCommand(company_id, user_id, Decimal("100.00")))


def test_registrar_movimiento_happy_path():
    repo = InMemoryCajaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # Open box
    caja = AbrirCajaUseCase(repo, db, dispatcher).execute(
        AbrirCajaCommand(company_id, user_id, Decimal("100.00"))
    )

    published_events = []
    dispatcher.subscribe(MovimientoCajaRegistrado, lambda ev: published_events.append(ev))

    use_case = RegistrarMovimientoCajaUseCase(repo, db, dispatcher)

    command = RegistrarMovimientoCajaCommand(
        company_id=company_id,
        caja_id=caja.id,
        type="INGRESO",
        amount=Decimal("450.00"),
        payment_method="TARJETA",
        concept="VENTA"
    )

    mov = use_case.execute(command)
    assert mov.amount == Decimal("450.00")
    assert mov.payment_method == "TARJETA"
    assert len(caja.movements) == 2  # Opening movement + new movement
    assert len(published_events) == 1


def test_registrar_arqueo_with_difference():
    repo = InMemoryCajaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # Open box (base 100 in cash)
    caja = AbrirCajaUseCase(repo, db, dispatcher).execute(
        AbrirCajaCommand(company_id, user_id, Decimal("100.00"))
    )

    # System expected is 100 in cash. Let's declare physical counted is 105 (excess of 5)
    published_events = []
    dispatcher.subscribe(ArqueoRealizado, lambda ev: published_events.append(ev))

    use_case = RegistrarArqueoCajaUseCase(repo, db, dispatcher)

    command = RegistrarArqueoCajaCommand(
        company_id=company_id,
        caja_id=caja.id,
        physical_amount=Decimal("105.00")
    )

    arq = use_case.execute(command)
    assert arq.difference == Decimal("5.00")
    assert arq.system_amount == Decimal("100.00")
    
    # Corrective movement registered automatically (concept AJUSTE_ARQUEO)
    assert len(caja.movements) == 2  # Opening + corrective adjustment
    assert caja.movements[1].concept == "AJUSTE_ARQUEO"
    assert caja.movements[1].amount == Decimal("5.00")
    assert len(published_events) == 1


def test_cerrar_caja_and_block_mutations():
    repo = InMemoryCajaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # Open box
    caja = AbrirCajaUseCase(repo, db, dispatcher).execute(
        AbrirCajaCommand(company_id, user_id, Decimal("100.00"))
    )

    published_events = []
    dispatcher.subscribe(CajaCerrada, lambda ev: published_events.append(ev))

    close_use_case = CerrarCajaUseCase(repo, db, dispatcher)
    
    # Close box (counted physical 100, system expects 100)
    caja_cerrada = close_use_case.execute(
        CerrarCajaCommand(company_id, caja.id, Decimal("100.00"))
    )
    assert caja_cerrada.status == "CERRADA"
    assert caja_cerrada.closed_at is not None
    assert len(published_events) == 1

    # Verify mutations are blocked on closed box
    move_use_case = RegistrarMovimientoCajaUseCase(repo, db, dispatcher)
    with pytest.raises(CajaCerradaException):
        move_use_case.execute(
            RegistrarMovimientoCajaCommand(
                company_id=company_id,
                caja_id=caja.id,
                type="INGRESO",
                amount=Decimal("50.00"),
                payment_method="EFECTIVO",
                concept="VENTA"
            )
        )


# ==========================================
# SQLALCHEMY INTEGRATION & ROLLBACK TESTS
# ==========================================

def test_caja_transactional_rollback():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db_session = TestingSessionLocal()

    try:
        from app.modules.caja.data.repositories.caja_repository_impl import CajaRepositoryImpl
        from app.modules.caja.data.models import Caja as DBCaja

        repo = CajaRepositoryImpl(db_session)
        dispatcher = EventDispatcher()

        # Force failure in event listener to trigger rollback
        def failing_subscriber(ev):
            raise RuntimeError("Forced failure to trigger database rollback!")

        dispatcher.subscribe(CajaAbierta, failing_subscriber)

        use_case = AbrirCajaUseCase(repo, db_session, dispatcher)

        company_id = uuid.uuid4()
        user_id = uuid.uuid4()

        command = AbrirCajaCommand(
            company_id=company_id,
            user_id=user_id,
            opening_balance=Decimal("250.00")
        )

        with pytest.raises(RuntimeError, match="Forced failure to trigger database rollback"):
            use_case.execute(command)

        # Check DB: should show NO boxes registered
        db_session.close()
        db_session = TestingSessionLocal()

        cajas_in_db = db_session.query(DBCaja).all()
        assert len(cajas_in_db) == 0, "Database should have rolled back completely!"

    finally:
        db_session.close()
