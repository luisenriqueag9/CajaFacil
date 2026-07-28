import pytest
import uuid
from datetime import datetime, timezone
from app.modules.cliente.domain.aggregates.cliente import Cliente
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.domain.exceptions import ClienteNoEncontradoException, ClienteYaExisteException, ClienteInvalidoException
from app.modules.cliente.application.ports.unit_of_work import UnitOfWork
from app.modules.cliente.application.use_cases import (
    RegistrarClienteUseCase,
    RegistrarClienteCommand,
    ActualizarClienteUseCase,
    ActualizarClienteCommand,
    InactivarClienteUseCase,
    InactivarClienteCommand,
    ObtenerClienteUseCase,
    ObtenerClienteQuery,
    ListarClientesUseCase,
    ListarClientesQuery,
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
        for c in self.clients.values():
            if c.company_id == company_id and c.tax_id == tax_id:
                return c
        return None

    def get_all(self, company_id: uuid.UUID, status: str | None = None) -> list[Cliente]:
        res = []
        for c in self.clients.values():
            if c.company_id == company_id:
                if status is None or c.status.valor == status:
                    res.append(c)
        return res

    def update(self, cliente: Cliente) -> Cliente:
        self.clients[cliente.id] = cliente
        return cliente

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

def test_register_client_success():
    repo = InMemoryClienteRepository()
    uow = DummyUnitOfWork()
    dispatcher = SpyEventDispatcher()
    use_case = RegistrarClienteUseCase(repo, uow, dispatcher)

    company_id = uuid.uuid4()
    command = RegistrarClienteCommand(
        company_id=company_id,
        name="Cliente Nuevo",
        tax_id="RUC-123456",
        phone="555-0199",
        email="cliente@correo.com"
    )

    dto = use_case.execute(command)
    assert dto.name == "Cliente Nuevo"
    assert dto.status == "ACTIVO"
    assert dto.tax_id == "RUC-123456"
    assert dto.email == "cliente@correo.com"

    # Verify event dispatched
    assert len(dispatcher.dispatched_events) == 1
    event = dispatcher.dispatched_events[0]
    assert event.name == "Cliente Nuevo"
    assert event.tax_id == "RUC-123456"

def test_register_client_duplicate_rejection():
    repo = InMemoryClienteRepository()
    uow = DummyUnitOfWork()
    use_case = RegistrarClienteUseCase(repo, uow)

    company_id = uuid.uuid4()
    command = RegistrarClienteCommand(
        company_id=company_id,
        name="Cliente A",
        tax_id="RUC-123",
        phone=None,
        email=None
    )
    use_case.execute(command)

    # Secondary register with duplicate tax_id must raise ClienteYaExisteException
    with pytest.raises(ClienteYaExisteException):
        use_case.execute(command)

def test_register_client_validation_error():
    repo = InMemoryClienteRepository()
    uow = DummyUnitOfWork()
    use_case = RegistrarClienteUseCase(repo, uow)

    company_id = uuid.uuid4()
    command_empty_name = RegistrarClienteCommand(
        company_id=company_id,
        name=" ",  # invalid name
        tax_id=None,
        phone=None,
        email=None
    )

    with pytest.raises(ClienteInvalidoException):
        use_case.execute(command_empty_name)

def test_update_client_profile_and_deactivate():
    repo = InMemoryClienteRepository()
    uow = DummyUnitOfWork()
    dispatcher = SpyEventDispatcher()
    reg_use_case = RegistrarClienteUseCase(repo, uow, dispatcher)
    upd_use_case = ActualizarClienteUseCase(repo, uow, dispatcher)
    deac_use_case = InactivarClienteUseCase(repo, uow, dispatcher)

    company_id = uuid.uuid4()
    created = reg_use_case.execute(
        RegistrarClienteCommand(company_id, "Nombre Inicial", "TAX-99", None, "test@test.com")
    )
    
    # Update profile
    updated = upd_use_case.execute(
        ActualizarClienteCommand(created.id, "Nombre Modificado", "TAX-99", "1234", "new@test.com")
    )
    assert updated.name == "Nombre Modificado"
    assert updated.email == "new@test.com"
    assert updated.phone == "1234"

    # Deactivate client
    deactivated = deac_use_case.execute(InactivarClienteCommand(created.id))
    assert deactivated.status == "INACTIVO"
