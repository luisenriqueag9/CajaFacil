import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria, TasaImpuesto, DesgloseImpuesto
from app.modules.tributacion.domain.services.motor_tributario import MotorTributario
from app.modules.tributacion.domain.exceptions import (
    ConfiguracionInvalidaException,
    ConfiguracionExpiradaException,
    SolapamientoConfiguracionException
)
from app.modules.tributacion.application.use_cases import (
    CrearConfiguracionTributariaUseCase,
    CrearConfiguracionTributariaCommand,
    TasaInput,
    ActivarConfiguracionTributariaUseCase,
    CalcularImpuestoTransaccionUseCase
)
from app.modules.tributacion.domain.repositories.configuracion_repository import ConfiguracionTributariaRepository
from app.modules.tributacion.application.event_dispatcher import EventDispatcher
from app.modules.tributacion.domain.events.tributacion_events import (
    ConfiguracionTributariaCreada,
    ConfiguracionTributariaActivada,
    ConfiguracionTributariaDesactivada
)

# ==========================================
# FAST IN-MEMORY REPOSITORY DOUBLE
# ==========================================

class InMemoryConfiguracionRepository(ConfiguracionTributariaRepository):
    def __init__(self):
        self.configs = {}

    def save(self, config: ConfiguracionTributaria) -> ConfiguracionTributaria:
        self.configs[config.id] = config
        return config

    def get_by_id(self, config_id: uuid.UUID) -> ConfiguracionTributaria | None:
        return self.configs.get(config_id)

    def get_active_by_company(self, company_id: uuid.UUID) -> ConfiguracionTributaria | None:
        for c in self.configs.values():
            if c.company_id == company_id and c.is_active:
                return c
        return None

    def search(self, company_id: uuid.UUID, filters: dict) -> list[ConfiguracionTributaria]:
        result = []
        for c in self.configs.values():
            if c.company_id == company_id:
                if "is_active" in filters and filters["is_active"] is not None and c.is_active != filters["is_active"]:
                    continue
                result.append(c)
        return sorted(result, key=lambda x: x.valid_from, reverse=True)


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

def test_tributacion_domain_invariants():
    config_id = uuid.uuid4()
    company_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # 1. Invariant: invalid calculation type
    with pytest.raises(ConfiguracionInvalidaException, match="Tipo de cálculo impositivo"):
        ConfiguracionTributaria(
            id=config_id,
            company_id=company_id,
            name="Régimen Invalido",
            is_active=False,
            valid_from=now,
            calculation_type="IMPUESTO_SUMADO"
        )

    # 2. Invariant: negative tax rate percentage
    with pytest.raises(ConfiguracionInvalidaException, match="no puede ser negativo"):
        TasaImpuesto(
            id=uuid.uuid4(),
            configuracion_id=config_id,
            name="General",
            code="IVA_GENERAL",
            rate_percentage=Decimal("-1.50")
        )

    # 3. Invariant: unique code check
    config = ConfiguracionTributaria(
        id=config_id,
        company_id=company_id,
        name="Regimen General",
        is_active=False,
        valid_from=now,
        calculation_type="ADICIONADO"
    )

    tasa1 = TasaImpuesto(id=uuid.uuid4(), configuracion_id=config_id, name="IVA A", code="IVA_G", rate_percentage=Decimal("15.00"))
    tasa2 = TasaImpuesto(id=uuid.uuid4(), configuracion_id=config_id, name="IVA B", code="IVA_G", rate_percentage=Decimal("18.00"))

    config.agregar_tasa(tasa1)
    with pytest.raises(ConfiguracionInvalidaException, match="ya existe en esta configuración"):
        config.agregar_tasa(tasa2)


# ==========================================
# MOTOR TRIBUTARIO SERVICE TESTS
# ==========================================

def test_motor_tributario_adicionado():
    motor = MotorTributario()
    config_id = uuid.uuid4()
    company_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    config = ConfiguracionTributaria(
        id=config_id,
        company_id=company_id,
        name="Régimen General",
        is_active=True,
        valid_from=now,
        calculation_type="ADICIONADO"
    )
    config.agregar_tasa(TasaImpuesto(uuid.uuid4(), config_id, "IVA", "IVA_GENERAL", Decimal("15.00")))

    # Item: Price 100, Qty 2, Category General
    items = [
        {"price": Decimal("100.00"), "quantity": Decimal("2.00"), "tax_category": "TASA_GENERAL"}
    ]

    desgloses = motor.calcular(items, config)
    assert len(desgloses) == 1
    assert desgloses[0].rate_code == "IVA_GENERAL"
    assert desgloses[0].net_amount == Decimal("200.00")
    assert desgloses[0].tax_amount == Decimal("30.00")


def test_motor_tributario_incluido():
    motor = MotorTributario()
    config_id = uuid.uuid4()
    company_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    config = ConfiguracionTributaria(
        id=config_id,
        company_id=company_id,
        name="Régimen Especial",
        is_active=True,
        valid_from=now,
        calculation_type="INCLUIDO"
    )
    config.agregar_tasa(TasaImpuesto(uuid.uuid4(), config_id, "IVA", "IVA_GENERAL", Decimal("15.00")))

    # Item: Price 115 (tax included), Qty 2, Category General. Total 230. Net should be 200, tax 30.
    items = [
        {"price": Decimal("115.00"), "quantity": Decimal("2.00"), "tax_category": "TASA_GENERAL"}
    ]

    desgloses = motor.calcular(items, config)
    assert len(desgloses) == 1
    assert desgloses[0].net_amount == Decimal("200.00")
    assert desgloses[0].tax_amount == Decimal("30.00")


def test_motor_tributario_fallback_no_config():
    motor = MotorTributario()
    items = [
        {"price": Decimal("50.00"), "quantity": Decimal("3.00"), "tax_category": "TASA_GENERAL"}
    ]

    # No configuration provided (Monotributo/simplificado)
    desgloses = motor.calcular(items, None)
    assert len(desgloses) == 1
    assert desgloses[0].net_amount == Decimal("150.00")
    assert desgloses[0].tax_amount == Decimal("0.00")


# ==========================================
# USE CASE UNIT TESTS
# ==========================================

def test_crear_y_activar_configuracion():
    repo = InMemoryConfiguracionRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()

    published_events = []
    dispatcher.subscribe(ConfiguracionTributariaCreada, lambda ev: published_events.append(ev))
    dispatcher.subscribe(ConfiguracionTributariaActivada, lambda ev: published_events.append(ev))

    # 1. Create config
    crear_use_case = CrearConfiguracionTributariaUseCase(repo, db, dispatcher)
    command = CrearConfiguracionTributariaCommand(
        company_id=company_id,
        name="Regimen General 2026",
        calculation_type="ADICIONADO",
        rates=[
            TasaInput(name="IVA General", code="IVA_GENERAL", rate_percentage=Decimal("15.00"))
        ]
    )

    config = crear_use_case.execute(command)
    assert config.is_active is False
    assert len(config.rates) == 1
    assert len(published_events) == 1

    # 2. Activate config
    activar_use_case = ActivarConfiguracionTributariaUseCase(repo, db, dispatcher)
    config_act = activar_use_case.execute(company_id, config.id)
    assert config_act.is_active is True
    assert len(published_events) == 2


# ==========================================
# SQLALCHEMY INTEGRATION & ROLLBACK TESTS
# ==========================================

def test_tributacion_transactional_rollback():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db_session = TestingSessionLocal()

    try:
        from app.modules.tributacion.data.repositories.configuracion_repository_impl import ConfiguracionTributariaRepositoryImpl
        from app.modules.tributacion.data.models import ConfiguracionTributaria as DBConfig

        repo = ConfiguracionTributariaRepositoryImpl(db_session)
        dispatcher = EventDispatcher()

        # Force failure in event listener to trigger rollback
        def failing_subscriber(ev):
            raise RuntimeError("Forced failure to trigger database rollback!")

        dispatcher.subscribe(ConfiguracionTributariaCreada, failing_subscriber)

        use_case = CrearConfiguracionTributariaUseCase(repo, db_session, dispatcher)

        company_id = uuid.uuid4()
        command = CrearConfiguracionTributariaCommand(
            company_id=company_id,
            name="Regimen Rollback",
            calculation_type="ADICIONADO",
            rates=[]
        )

        with pytest.raises(RuntimeError, match="Forced failure to trigger database rollback"):
            use_case.execute(command)

        # Check DB: should show NO configs registered
        db_session.close()
        db_session = TestingSessionLocal()

        configs_in_db = db_session.query(DBConfig).all()
        assert len(configs_in_db) == 0, "Database should have rolled back completely!"

    finally:
        db_session.close()
