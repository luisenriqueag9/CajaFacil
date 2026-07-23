import pytest
import uuid
from datetime import datetime, timezone
from app.modules.supplier.domain.entities.supplier import Supplier
from app.modules.supplier.domain.exceptions import SupplierNotFoundException, SupplierAlreadyExistsException, InvalidSupplierException
from app.modules.supplier.application.use_cases import (
    CreateSupplierUseCase,
    UpdateSupplierUseCase,
    GetSupplierByIdUseCase,
    ListSuppliersUseCase,
    DeactivateSupplierUseCase,
    ActivateSupplierUseCase,
)

class InMemorySupplierRepository:
    def __init__(self):
        self.suppliers = {}

    def create(self, supplier: Supplier) -> Supplier:
        self.suppliers[supplier.id] = supplier
        return supplier

    def get_by_id(self, supplier_id: uuid.UUID) -> Supplier | None:
        return self.suppliers.get(supplier_id)

    def get_by_tax_id(self, company_id: uuid.UUID, tax_id: str) -> Supplier | None:
        for s in self.suppliers.values():
            if s.company_id == company_id and s.tax_id and s.tax_id.lower() == tax_id.lower():
                return s
        return None

    def get_all(self, company_id: uuid.UUID, status: str | None = None) -> list[Supplier]:
        result = []
        for s in self.suppliers.values():
            if s.company_id == company_id:
                if status is None or s.status == status:
                    result.append(s)
        return sorted(result, key=lambda x: x.name)

    def update(self, supplier: Supplier) -> Supplier:
        self.suppliers[supplier.id] = supplier
        return supplier


def test_supplier_registration_and_normalization():
    repo = InMemorySupplierRepository()
    create_uc = CreateSupplierUseCase(repo)

    company_id = uuid.uuid4()
    supplier = Supplier.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="  dIstribuidora   cAstRo  ",
        tax_id="  rtn-12345-6  ",
        contact_name="Juan Castro",
        phone="555-0199",
        email="juan@castro.com",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    created = create_uc.execute(supplier)
    assert created.name == "dIstribuidora cAstRo"  # Collapsed spaces but preserves case
    assert created.tax_id == "RTN-12345-6"  # Upper-cased and spaces collapsed
    assert created.status == "ACTIVO"
    assert repo.get_by_id(supplier.id) is not None


def test_supplier_duplicate_tax_id_restriction():
    repo = InMemorySupplierRepository()
    create_uc = CreateSupplierUseCase(repo)

    company_id = uuid.uuid4()
    sup1 = Supplier.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Distribuidora A",
        tax_id="RTN-999",
        contact_name="Pedro",
        phone=None,
        email=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    create_uc.execute(sup1)

    sup2 = Supplier.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Distribuidora B",
        tax_id=" rtn-999  ",  # duplicates sup1 after normalisation
        contact_name="Maria",
        phone=None,
        email=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    with pytest.raises(SupplierAlreadyExistsException):
        create_uc.execute(sup2)


def test_supplier_name_no_uniqueness_constraint():
    repo = InMemorySupplierRepository()
    create_uc = CreateSupplierUseCase(repo)
    list_uc = ListSuppliersUseCase(repo)

    company_id = uuid.uuid4()
    
    # Register two suppliers with the exact same name (e.g. informal local suppliers named Don Jose)
    sup1 = Supplier.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Don Jose",
        tax_id=None,
        contact_name="Jose Gomez",
        phone=None,
        email=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    create_uc.execute(sup1)

    sup2 = Supplier.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="  Don   Jose  ",
        tax_id=None,
        contact_name="Jose Ramirez",
        phone=None,
        email=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    create_uc.execute(sup2)

    suppliers = list_uc.execute(company_id=company_id)
    assert len(suppliers) == 2
    assert suppliers[0].name == "Don Jose"
    assert suppliers[1].name == "Don Jose"
    assert suppliers[0].id != suppliers[1].id


def test_supplier_domain_invariants():
    # Empty name validation
    with pytest.raises(InvalidSupplierException):
        Supplier.register(
            id=uuid.uuid4(),
            company_id=uuid.uuid4(),
            name="",
            tax_id=None,
            contact_name=None,
            phone=None,
            email=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

    # Missing company_id validation
    with pytest.raises(InvalidSupplierException):
        Supplier(
            id=uuid.uuid4(),
            company_id=None,
            name="Proveedor A",
            tax_id=None,
            contact_name=None,
            phone=None,
            email=None,
            status="ACTIVO",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

    # Empty tax_id spaces validation
    with pytest.raises(InvalidSupplierException):
        Supplier.register(
            id=uuid.uuid4(),
            company_id=uuid.uuid4(),
            name="Proveedor B",
            tax_id="   ",
            contact_name=None,
            phone=None,
            email=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )


def test_supplier_update_profile_and_tax_id_uniqueness():
    repo = InMemorySupplierRepository()
    create_uc = CreateSupplierUseCase(repo)
    update_uc = UpdateSupplierUseCase(repo)

    company_id = uuid.uuid4()
    sup1 = Supplier.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Proveedor Uno",
        tax_id="TAX-111",
        contact_name=None,
        phone=None,
        email=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    create_uc.execute(sup1)

    sup2 = Supplier.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Proveedor Dos",
        tax_id=None,
        contact_name=None,
        phone=None,
        email=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    create_uc.execute(sup2)

    # Valid update
    updated = update_uc.execute(
        supplier_id=sup2.id,
        updates={"name": "Proveedor Dos Modificado", "tax_id": "TAX-222"}
    )
    assert updated.name == "Proveedor Dos Modificado"
    assert updated.tax_id == "TAX-222"

    # Attempting duplicate tax_id update
    with pytest.raises(SupplierAlreadyExistsException):
        update_uc.execute(
            supplier_id=sup2.id,
            updates={"tax_id": "TAX-111"}
        )


def test_supplier_deactivate_and_activate():
    repo = InMemorySupplierRepository()
    create_uc = CreateSupplierUseCase(repo)
    deactivate_uc = DeactivateSupplierUseCase(repo)
    activate_uc = ActivateSupplierUseCase(repo)

    company_id = uuid.uuid4()
    supplier = Supplier.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Proveedor Temporal",
        tax_id=None,
        contact_name=None,
        phone=None,
        email=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    create_uc.execute(supplier)

    deactivate_uc.execute(supplier.id)
    assert repo.get_by_id(supplier.id).status == "INACTIVO"

    activate_uc.execute(supplier.id)
    assert repo.get_by_id(supplier.id).status == "ACTIVO"
