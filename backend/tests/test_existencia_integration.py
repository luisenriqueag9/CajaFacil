import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario
from app.modules.inventario.domain.exceptions import StockInsuficienteException, ProductoNoManejaInventarioException
from app.modules.inventario.domain.events.inventario_events import InventarioActualizado
from app.modules.inventario.application.event_dispatcher import EventDispatcher
from app.modules.inventario.application.ports.product_lookup import ProductLookup, ProductDetails
from app.modules.inventario.application.ports.stock_checker_impl import StockCheckerImpl
from app.modules.inventario.application.use_cases import (
    ConsultarExistenciaUseCase,
    RecalcularExistenciaDesdeKardexUseCase,
    RegistrarMovimientoUseCase,
    RegistrarMovimientoCommand,
    RegistrarMermaUseCase,
    RegistrarMermaCommand,
    RegistrarAjusteUseCase,
    RegistrarAjusteCommand
)
from app.modules.inventario.data.repositories.existencia_repository_impl import ExistenciaRepositoryImpl
from app.modules.inventario.data.repositories.movimiento_repository_impl import MovimientoInventarioRepositoryImpl

# ==========================================
# TEST DOUBLE PRODUCT LOOKUP
# ==========================================

class TestProductLookup(ProductLookup):
    def __init__(self):
        self.products = {}

    def add_product(self, product_id: uuid.UUID, active: bool = True, controls_stock: bool = True, allows_negative: bool = False):
        self.products[product_id] = ProductDetails(
            exists=True,
            active=active,
            controls_stock=controls_stock,
            allows_negative=allows_negative
        )

    def get_details(self, company_id: uuid.UUID, product_id: uuid.UUID) -> ProductDetails:
        return self.products.get(
            product_id, 
            ProductDetails(exists=False, active=False, controls_stock=False, allows_negative=False)
        )


# ==========================================
# SQLALCHEMY METADATA SETUPS
# ==========================================

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    # Import other models to ensure SQLite registers foreign keys correctly
    from app.modules.company.data.models import Company
    from app.modules.product.data.models import Product
    from app.modules.brand.data.models import Brand
    from app.modules.category.data.models import Category
    from app.modules.unit.data.models import Unit
    
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Pre-populate required company and products to satisfy FK constraints in sqlite
    # We use UUIDs containing trailing letters to avoid SQLite numeric affinity float conversion!
    comp_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    prod_id1 = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    prod_id2 = uuid.UUID("33333333-3333-3333-3333-33333333333c")

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
    
    brand = Brand(id=uuid.uuid4(), company_id=comp_id, name="Marca Test")
    cat = Category(id=uuid.uuid4(), company_id=comp_id, name="Categoria Test")
    unit = Unit(id=uuid.uuid4(), company_id=comp_id, code="UN01", name="Unidad", abbreviation="UN", allows_decimal=False, status="ACTIVE")
    session.add(brand)
    session.add(cat)
    session.add(unit)
    session.flush()

    session.add(Product(
        id=prod_id1, company_id=comp_id, name="Refresco", internal_code="REF01",
        cost=Decimal("10.00"), price=Decimal("15.00"), tax_rate=Decimal("15.00"), status="ACTIVE",
        controls_stock=True, allows_decimal=False, minimum_stock=Decimal("5.00"),
        brand_id=brand.id, category_id=cat.id, unit_id=unit.id
    ))
    session.add(Product(
        id=prod_id2, company_id=comp_id, name="Pan", internal_code="PAN01",
        cost=Decimal("1.00"), price=Decimal("2.00"), tax_rate=Decimal("0.00"), status="ACTIVE",
        controls_stock=True, allows_decimal=True, minimum_stock=Decimal("10.00"),
        brand_id=brand.id, category_id=cat.id, unit_id=unit.id
    ))
    session.commit()

    yield session
    session.close()


# ==========================================
# EXISTENCIAS INTEGRATION TESTS
# ==========================================

def test_existencias_flow_and_constraints(db_session):
    company_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    product_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    user_id = uuid.uuid4()

    # Repositories
    existencia_repo = ExistenciaRepositoryImpl(db_session)
    movimiento_repo = MovimientoInventarioRepositoryImpl(db_session)

    # Dispatcher and Lookup
    dispatcher = EventDispatcher()
    product_lookup = TestProductLookup()
    product_lookup.add_product(product_id, allows_negative=False)

    # Events capture list
    captured_events = []
    dispatcher.subscribe(InventarioActualizado, lambda ev: captured_events.append(ev))

    # Use Cases
    consultar_uc = ConsultarExistenciaUseCase(existencia_repo, product_lookup)
    registrar_uc = RegistrarMovimientoUseCase(movimiento_repo, existencia_repo, db_session, dispatcher, product_lookup)

    # 1. Consult non-existent stock: should initialize to 0
    existencia = consultar_uc.execute(company_id, product_id)
    assert existencia.stock == Decimal("0.0000")

    # 2. Register ENTRADA (Compra) of 10
    cmd_in = RegistrarMovimientoCommand(
        company_id=company_id,
        product_id=product_id,
        type="ENTRADA",
        concept="COMPRA",
        quantity=Decimal("10.0000"),
        created_by=user_id
    )
    registrar_uc.execute(cmd_in)

    # Check fast balance is now 10
    existencia = existencia_repo.get_by_product_id(company_id, product_id)
    assert existencia.stock == Decimal("10.0000")
    assert len(captured_events) == 1
    assert captured_events[-1].new_balance == Decimal("10.0000")

    # 3. Register SALIDA (Venta) of 4
    cmd_out = RegistrarMovimientoCommand(
        company_id=company_id,
        product_id=product_id,
        type="SALIDA",
        concept="VENTA",
        quantity=Decimal("4.0000"),
        created_by=user_id
    )
    registrar_uc.execute(cmd_out)

    # Check fast balance is now 6
    existencia = existencia_repo.get_by_product_id(company_id, product_id)
    assert existencia.stock == Decimal("6.0000")
    assert captured_events[-1].new_balance == Decimal("6.0000")

    # 4. Attempt SALIDA (Venta) of 8: should raise StockInsuficienteException (allows_negative = False)
    cmd_excess = RegistrarMovimientoCommand(
        company_id=company_id,
        product_id=product_id,
        type="SALIDA",
        concept="VENTA",
        quantity=Decimal("8.0000"),
        created_by=user_id
    )
    with pytest.raises(StockInsuficienteException):
        registrar_uc.execute(cmd_excess)

    # Check stock remained at 6
    existencia = existencia_repo.get_by_product_id(company_id, product_id)
    assert existencia.stock == Decimal("6.0000")


def test_allows_negative_stock(db_session):
    company_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    product_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    user_id = uuid.uuid4()

    existencia_repo = ExistenciaRepositoryImpl(db_session)
    movimiento_repo = MovimientoInventarioRepositoryImpl(db_session)
    dispatcher = EventDispatcher()
    
    # Configure lookup to allow negative stock
    product_lookup = TestProductLookup()
    product_lookup.add_product(product_id, allows_negative=True)

    registrar_uc = RegistrarMovimientoUseCase(movimiento_repo, existencia_repo, db_session, dispatcher, product_lookup)

    # 1. Register SALIDA of 5: starts at 0, should become -5
    cmd = RegistrarMovimientoCommand(
        company_id=company_id,
        product_id=product_id,
        type="SALIDA",
        concept="VENTA",
        quantity=Decimal("5.0000"),
        created_by=user_id
    )
    registrar_uc.execute(cmd)

    existencia = existencia_repo.get_by_product_id(company_id, product_id)
    assert existencia.stock == Decimal("-5.0000")


def test_registrar_merma_and_ajuste(db_session):
    company_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    product_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    user_id = uuid.uuid4()

    existencia_repo = ExistenciaRepositoryImpl(db_session)
    movimiento_repo = MovimientoInventarioRepositoryImpl(db_session)
    dispatcher = EventDispatcher()
    product_lookup = TestProductLookup()
    product_lookup.add_product(product_id, allows_negative=False)

    registrar_uc = RegistrarMovimientoUseCase(movimiento_repo, existencia_repo, db_session, dispatcher, product_lookup)
    merma_uc = RegistrarMermaUseCase(movimiento_repo, existencia_repo, db_session, dispatcher, product_lookup)
    ajuste_uc = RegistrarAjusteUseCase(movimiento_repo, existencia_repo, db_session, dispatcher, product_lookup)

    # Set initial stock to 10
    registrar_uc.execute(RegistrarMovimientoCommand(
        company_id=company_id, product_id=product_id, type="ENTRADA",
        concept="COMPRA", quantity=Decimal("10.0000"), created_by=user_id
    ))

    # 1. Merma of 2 units (Rotura)
    cmd_merma = RegistrarMermaCommand(
        company_id=company_id,
        product_id=product_id,
        quantity=Decimal("2.0000"),
        reason="ROTURA",
        created_by=user_id,
        description="Botella rota"
    )
    merma_uc.execute(cmd_merma)

    # Stock should be 8
    existencia = existencia_repo.get_by_product_id(company_id, product_id)
    assert existencia.stock == Decimal("8.0000")

    # 2. Adjust physical quantity to 15 (creates ENTRADA movement of 7)
    cmd_ajuste = RegistrarAjusteCommand(
        company_id=company_id,
        product_id=product_id,
        physical_quantity=Decimal("15.0000"),
        supervisor_id=user_id,
        notes="Conteo físico auditoría"
    )
    ajuste_uc.execute(cmd_ajuste)

    existencia = existencia_repo.get_by_product_id(company_id, product_id)
    assert existencia.stock == Decimal("15.0000")

    # Check last movement in DB is an ENTRADA of 7 units for AJUSTE
    last_mov = movimiento_repo.search(company_id, {"product_id": product_id})[0]
    assert last_mov.type == "ENTRADA"
    assert last_mov.concept == "AJUSTE"
    assert last_mov.quantity == Decimal("7.0000")


def test_recalcular_existencia_desde_kardex(db_session):
    company_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    product_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    user_id = uuid.uuid4()

    existencia_repo = ExistenciaRepositoryImpl(db_session)
    movimiento_repo = MovimientoInventarioRepositoryImpl(db_session)
    dispatcher = EventDispatcher()
    product_lookup = TestProductLookup()
    product_lookup.add_product(product_id, allows_negative=False)

    registrar_uc = RegistrarMovimientoUseCase(movimiento_repo, existencia_repo, db_session, dispatcher, product_lookup)
    recalcular_uc = RecalcularExistenciaDesdeKardexUseCase(existencia_repo, movimiento_repo, product_lookup, db_session)

    # 1. Populate Kardex with several movements
    registrar_uc.execute(RegistrarMovimientoCommand(
        company_id=company_id, product_id=product_id, type="ENTRADA",
        concept="COMPRA", quantity=Decimal("20.0000"), created_by=user_id
    ))
    registrar_uc.execute(RegistrarMovimientoCommand(
        company_id=company_id, product_id=product_id, type="SALIDA",
        concept="VENTA", quantity=Decimal("5.0000"), created_by=user_id
    ))
    registrar_uc.execute(RegistrarMovimientoCommand(
        company_id=company_id, product_id=product_id, type="SALIDA",
        concept="VENTA", quantity=Decimal("3.0000"), created_by=user_id
    ))

    # Current stock is 12
    existencia = existencia_repo.get_by_product_id(company_id, product_id)
    assert existencia.stock == Decimal("12.0000")

    # 2. Corrupt or clear the stock balance in existence table manually
    existencia.stock = Decimal("0.0000")
    existencia_repo.save(existencia)
    db_session.commit()

    # Verify cache is corrupted
    assert existencia_repo.get_by_product_id(company_id, product_id).stock == Decimal("0.0000")

    # 3. Recalculate from Kardex
    recalculated = recalcular_uc.execute(company_id, product_id)
    assert recalculated.stock == Decimal("12.0000")

    # Verify persisted cache value is restored
    assert existencia_repo.get_by_product_id(company_id, product_id).stock == Decimal("12.0000")


def test_transactional_rollback_on_existencia(db_session):
    company_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    product_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    user_id = uuid.uuid4()

    existencia_repo = ExistenciaRepositoryImpl(db_session)
    movimiento_repo = MovimientoInventarioRepositoryImpl(db_session)
    product_lookup = TestProductLookup()
    product_lookup.add_product(product_id, allows_negative=False)

    # Force failure in event listener to trigger rollback
    dispatcher = EventDispatcher()
    def failing_listener(ev):
        raise RuntimeError("Forced failure to verify rollback!")
    dispatcher.subscribe(InventarioActualizado, failing_listener)

    registrar_uc = RegistrarMovimientoUseCase(movimiento_repo, existencia_repo, db_session, dispatcher, product_lookup)

    # Execute and verify runtime error
    with pytest.raises(RuntimeError, match="Forced failure to verify rollback"):
        registrar_uc.execute(RegistrarMovimientoCommand(
            company_id=company_id, product_id=product_id, type="ENTRADA",
            concept="COMPRA", quantity=Decimal("15.0000"), created_by=user_id
        ))

    # Verify both movement is NOT recorded and stock remained at 0
    existencia = existencia_repo.get_by_product_id(company_id, product_id)
    assert existencia is None or existencia.stock == Decimal("0.0000")
    
    movements = movimiento_repo.search(company_id, {"product_id": product_id})
    assert len(movements) == 0


def test_stock_checker_port(db_session):
    company_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
    product_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")
    user_id = uuid.uuid4()

    existencia_repo = ExistenciaRepositoryImpl(db_session)
    movimiento_repo = MovimientoInventarioRepositoryImpl(db_session)
    dispatcher = EventDispatcher()
    product_lookup = TestProductLookup()
    product_lookup.add_product(product_id, allows_negative=False)

    registrar_uc = RegistrarMovimientoUseCase(movimiento_repo, existencia_repo, db_session, dispatcher, product_lookup)
    stock_checker = StockCheckerImpl(existencia_repo, product_lookup)

    # 1. Initialize stock to 5
    registrar_uc.execute(RegistrarMovimientoCommand(
        company_id=company_id, product_id=product_id, type="ENTRADA",
        concept="COMPRA", quantity=Decimal("5.0000"), created_by=user_id
    ))

    # 2. Check sufficient stock via port
    assert stock_checker.has_sufficient_stock(company_id, product_id, Decimal("3.0000")) is True
    assert stock_checker.has_sufficient_stock(company_id, product_id, Decimal("6.0000")) is False

    # 3. If allows negative is True, always has stock
    product_lookup.add_product(product_id, allows_negative=True)
    assert stock_checker.has_sufficient_stock(company_id, product_id, Decimal("100.0000")) is True
