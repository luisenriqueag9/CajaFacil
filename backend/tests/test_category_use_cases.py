import pytest
import uuid
from datetime import datetime, timezone
from app.modules.category.domain.entities.category import Category
from app.modules.category.domain.exceptions import CategoryAlreadyExistsException, InvalidCategoryException, CategoryNotFoundException
from app.modules.category.application.use_cases import (
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    GetCategoryByIdUseCase,
    ListCategoriesUseCase,
    DeactivateCategoryUseCase,
    ActivateCategoryUseCase,
    InitializeDefaultCategoryUseCase,
    GetDefaultCategoryUseCase,
)

class InMemoryCategoryRepository:
    def __init__(self):
        self.categories = {}

    def create(self, category: Category) -> Category:
        self.categories[category.id] = category
        return category

    def get_by_id(self, category_id) -> Category | None:
        return self.categories.get(category_id)

    def get_by_name(self, company_id, name) -> Category | None:
        for c in self.categories.values():
            if c.company_id == company_id and c.name.lower() == name.lower():
                return c
        return None

    def get_all(self, company_id, status=None) -> list[Category]:
        result = []
        for c in self.categories.values():
            if c.company_id == company_id:
                if status is None or c.status == status:
                    result.append(c)
        return sorted(result, key=lambda x: x.name)

    def update(self, category: Category) -> Category:
        self.categories[category.id] = category
        return category

    def get_default_category(self, company_id) -> Category | None:
        for c in self.categories.values():
            if c.company_id == company_id and c.protected:
                return c
        return None


def test_category_creation_and_normalization():
    repo = InMemoryCategoryRepository()
    use_case = CreateCategoryUseCase(repo)

    company_id = uuid.uuid4()
    category = Category.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="  lAcTeOs   fReScOs  ",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    created = use_case.execute(category)
    assert created.name == "lAcTeOs fReScOs"  # Normalizado pero conserva casing
    assert repo.get_by_id(category.id) is not None

    # Intentar duplicado (insensible a mayúsculas/minúsculas)
    duplicate = Category.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Lacteos Frescos",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    with pytest.raises(CategoryAlreadyExistsException):
        use_case.execute(duplicate)


def test_category_update_and_normalization():
    repo = InMemoryCategoryRepository()
    create_uc = CreateCategoryUseCase(repo)
    update_uc = UpdateCategoryUseCase(repo)

    company_id = uuid.uuid4()
    cat1 = Category.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Bebidas",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    create_uc.execute(cat1)

    cat2 = Category.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Abarrotes",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    create_uc.execute(cat2)

    # Actualizar a nombre válido normalizado
    updated = update_uc.execute(cat2.id, {"name": "  aBarrotes   nUevos  "})
    assert updated.name == "aBarrotes nUevos"

    # Intentar renombrar a categoría que ya existe
    with pytest.raises(CategoryAlreadyExistsException):
        update_uc.execute(cat2.id, {"name": "Bebidas"})


def test_deactivate_and_activate():
    repo = InMemoryCategoryRepository()
    create_uc = CreateCategoryUseCase(repo)
    deactivate_uc = DeactivateCategoryUseCase(repo)
    activate_uc = ActivateCategoryUseCase(repo)

    company_id = uuid.uuid4()
    category = Category.register(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Ferreteria",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    create_uc.execute(category)

    deactivate_uc.execute(category.id)
    assert repo.get_by_id(category.id).status == "INACTIVO"

    activate_uc.execute(category.id)
    assert repo.get_by_id(category.id).status == "ACTIVO"


def test_protected_category_constraints():
    repo = InMemoryCategoryRepository()
    company_id = uuid.uuid4()
    
    # Crear categoría protegida
    protected_cat = Category.initialize_default(
        id=uuid.uuid4(),
        company_id=company_id,
        name="Sin Clasificar",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    repo.create(protected_cat)

    update_uc = UpdateCategoryUseCase(repo)
    deactivate_uc = DeactivateCategoryUseCase(repo)

    # Intentar renombrar la categoría protegida debe fallar
    with pytest.raises(InvalidCategoryException):
        update_uc.execute(protected_cat.id, {"name": "Otro Nombre"})

    # Intentar desactivar la categoría protegida debe fallar
    with pytest.raises(InvalidCategoryException):
        deactivate_uc.execute(protected_cat.id)


def test_initialize_and_get_default_category():
    repo = InMemoryCategoryRepository()
    init_uc = InitializeDefaultCategoryUseCase(repo)
    get_uc = GetDefaultCategoryUseCase(repo)

    company_id = uuid.uuid4()
    
    # Inicializar la categoría por defecto
    default_cat = init_uc.execute(company_id)
    assert default_cat.name == "Sin Clasificar"
    assert default_cat.protected is True

    # Recuperar la categoría por defecto
    retrieved = get_uc.execute(company_id)
    assert retrieved.id == default_cat.id
    assert retrieved.name == "Sin Clasificar"
    assert retrieved.protected is True
