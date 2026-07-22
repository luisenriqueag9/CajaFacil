import pytest
import uuid
from datetime import datetime, timezone
from app.modules.brand.domain.entities.brand import Brand
from app.modules.brand.domain.exceptions import BrandAlreadyExistsException, InvalidBrandException, BrandNotFoundException
from app.modules.brand.application.use_cases import (
    CreateBrandUseCase,
    UpdateBrandUseCase,
    GetBrandByIdUseCase,
    ListBrandsUseCase,
    DeactivateBrandUseCase,
    ActivateBrandUseCase,
    DeleteBrandUseCase
)

class InMemoryBrandRepository:
    def __init__(self):
        self.brands = {}

    def create(self, brand: Brand) -> Brand:
        self.brands[brand.id] = brand
        return brand

    def get_by_id(self, brand_id) -> Brand | None:
        return self.brands.get(brand_id)

    def get_by_name(self, company_id, name) -> Brand | None:
        for b in self.brands.values():
            if b.company_id == company_id and b.name.lower() == name.lower():
                return b
        return None

    def get_all(self, company_id, status=None) -> list[Brand]:
        result = []
        for b in self.brands.values():
            if b.company_id == company_id:
                if status is None or b.status == status:
                    result.append(b)
        return sorted(result, key=lambda x: x.name)

    def update(self, brand: Brand) -> Brand:
        self.brands[brand.id] = brand
        return brand

    def delete(self, brand_id) -> bool:
        if brand_id in self.brands:
            del self.brands[brand_id]
            return True
        return False

def test_brand_creation_and_normalization():
    repo = InMemoryBrandRepository()
    use_case = CreateBrandUseCase(repo)

    company_id = uuid.uuid4()
    brand = Brand(
        id=uuid.uuid4(),
        company_id=company_id,
        name="  cOca   coLa  ",
        status="ACTIVO",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    created = use_case.execute(brand)
    assert created.name == "cOca coLa"  # Normalized but preserves casing
    assert repo.get_by_id(brand.id) is not None

    # Try duplicate (case-insensitive)
    duplicate = Brand(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Coca Cola",
        status="ACTIVO",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    with pytest.raises(BrandAlreadyExistsException):
        use_case.execute(duplicate)

def test_brand_update_and_normalization():
    repo = InMemoryBrandRepository()
    create_uc = CreateBrandUseCase(repo)
    update_uc = UpdateBrandUseCase(repo)

    company_id = uuid.uuid4()
    brand1 = Brand(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Sabritas",
        status="ACTIVO",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    create_uc.execute(brand1)

    brand2 = Brand(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Bimbo",
        status="ACTIVO",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    create_uc.execute(brand2)

    # Update to valid normalized name
    updated = update_uc.execute(brand2.id, {"name": "  biMbo   nUevo  "})
    assert updated.name == "biMbo nUevo"

    # Try duplicate rename
    with pytest.raises(BrandAlreadyExistsException):
        update_uc.execute(brand2.id, {"name": "Sabritas"})

def test_deactivate_and_activate():
    repo = InMemoryBrandRepository()
    create_uc = CreateBrandUseCase(repo)
    deactivate_uc = DeactivateBrandUseCase(repo)
    activate_uc = ActivateBrandUseCase(repo)

    company_id = uuid.uuid4()
    brand = Brand(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Sula",
        status="ACTIVO",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    create_uc.execute(brand)

    deactivate_uc.execute(brand.id)
    assert repo.get_by_id(brand.id).status == "INACTIVO"

    activate_uc.execute(brand.id)
    assert repo.get_by_id(brand.id).status == "ACTIVO"
