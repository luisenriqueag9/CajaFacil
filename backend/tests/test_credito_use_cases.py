import pytest
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from app.modules.credito.domain.aggregates.credito import Credito
from app.modules.credito.domain.repositories.credito_repository import CreditoRepository
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.domain.aggregates.cliente import Cliente
from app.modules.credito.domain.exceptions import CreditoNoEncontradoException, CreditoYaExisteException, CreditoInvalidoException, LimiteExcedidoException
from app.modules.cliente.domain.exceptions import ClienteNoEncontradoException
from app.modules.credito.application.ports.unit_of_work import UnitOfWork
from app.modules.credito.application.use_cases import (
    AbrirCuentaCreditoUseCase,
    AbrirCuentaCreditoCommand,
    ActualizarLimiteCreditoUseCase,
    ActualizarLimiteCreditoCommand,
    InactivarCuentaCreditoUseCase,
    InactivarCuentaCreditoCommand,
    ObtenerCreditoUseCase,
    ObtenerCreditoQuery,
    ListarCreditosUseCase,
    ListarCreditosQuery,
    RegistrarCargoCreditoUseCase,
    RegistrarCargoCreditoCommand,
    ReversarCargoCreditoUseCase,
    ReversarCargoCreditoCommand,
)
from app.common.event_dispatcher import EventDispatcher

class InMemoryClienteRepository(ClienteRepository):
    def __init__(self):
        self.clients = {}
    def create(self, cliente: Cliente) -> Cliente:
        self.clients[cliente.id] = cliente
        return cliente
    def get_by_id(self, client_id: uuid.UUID) -> Cliente | None:
        return self.clients.get(client_id)
    def get_by_tax_id(self, company_id: uuid.UUID, tax_id: str) -> Cliente | None:
        return None
    def get_all(self, company_id: uuid.UUID, status: str | None = None) -> list[Cliente]:
        return list(self.clients.values())
    def update(self, cliente: Cliente) -> Cliente:
        self.clients[cliente.id] = cliente
        return cliente

class InMemoryCreditoRepository(CreditoRepository):
    def __init__(self):
        self.credits = {}

    def create(self, credito: Credito) -> Credito:
        self.credits[credito.id] = credito
        return credito

    def get_by_id(self, credit_id: uuid.UUID) -> Credito | None:
        return self.credits.get(credit_id)

    def get_by_client_id(self, company_id: uuid.UUID, client_id: uuid.UUID) -> Credito | None:
        for c in self.credits.values():
            if c.company_id == company_id and c.client_id == client_id:
                return c
        return None

    def get_all(self, company_id: uuid.UUID, status: str | None = None) -> list[Credito]:
        res = []
        for c in self.credits.values():
            if c.company_id == company_id:
                if status is None or c.status.valor == status:
                    res.append(c)
        return res

    def update(self, credito: Credito) -> Credito:
        self.credits[credito.id] = credito
        return credito

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
        self.dispatched_events = []
    def dispatch(self, event) -> None:
        self.dispatched_events.append(event)

def test_open_credit_account_success():
    repo = InMemoryCreditoRepository()
    client_repo = InMemoryClienteRepository()
    uow = DummyUnitOfWork()
    dispatcher = SpyEventDispatcher()

    # Pre-register client
    company_id = uuid.uuid4()
    client_id = uuid.uuid4()
    client_repo.create(
        Cliente.register(client_id, company_id, "Cliente Test", "123", None, None, datetime.now(), datetime.now())
    )

    use_case = AbrirCuentaCreditoUseCase(repo, client_repo, uow, dispatcher)

    command = AbrirCuentaCreditoCommand(
        company_id=company_id,
        client_id=client_id,
        credit_limit=Decimal("5000.00")
    )

    dto = use_case.execute(command)
    assert dto.credit_limit == Decimal("5000.00")
    assert dto.balance == Decimal("0.00")
    assert dto.status == "ACTIVO"

    assert len(dispatcher.dispatched_events) == 1

def test_open_credit_account_client_not_found():
    repo = InMemoryCreditoRepository()
    client_repo = InMemoryClienteRepository()
    uow = DummyUnitOfWork()
    use_case = AbrirCuentaCreditoUseCase(repo, client_repo, uow)

    command = AbrirCuentaCreditoCommand(
        company_id=uuid.uuid4(),
        client_id=uuid.uuid4(),
        credit_limit=Decimal("5000.00")
    )

    with pytest.raises(ClienteNoEncontradoException):
        use_case.execute(command)

def test_add_debt_and_release_debt():
    repo = InMemoryCreditoRepository()
    client_repo = InMemoryClienteRepository()
    uow = DummyUnitOfWork()
    dispatcher = SpyEventDispatcher()

    company_id = uuid.uuid4()
    client_id = uuid.uuid4()
    client_repo.create(
        Cliente.register(client_id, company_id, "Cliente Test", "123", None, None, datetime.now(), datetime.now())
    )

    open_case = AbrirCuentaCreditoUseCase(repo, client_repo, uow, dispatcher)
    cargo_case = RegistrarCargoCreditoUseCase(repo, uow, dispatcher)
    reversar_case = ReversarCargoCreditoUseCase(repo, uow, dispatcher)

    acc = open_case.execute(AbrirCuentaCreditoCommand(company_id, client_id, Decimal("1000.00")))

    # 1. Cargo exitoso
    ref_id = uuid.uuid4()
    updated = cargo_case.execute(RegistrarCargoCreditoCommand(company_id, client_id, Decimal("400.00"), ref_id))
    assert updated.balance == Decimal("400.00")

    # 2. Cargo excediendo limite
    with pytest.raises(LimiteExcedidoException):
        cargo_case.execute(RegistrarCargoCreditoCommand(company_id, client_id, Decimal("700.00"), uuid.uuid4()))

    # 3. Reversar cargo exitoso
    updated_rev = reversar_case.execute(ReversarCargoCreditoCommand(company_id, client_id, Decimal("150.00"), ref_id))
    assert updated_rev.balance == Decimal("250.00")
