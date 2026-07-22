import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.repositories.product_repository import ProductRepository
from app.modules.product.domain.exceptions.product_already_exists_exception import ProductAlreadyExistsException

@dataclass
class CreateProductCommand:
    """
    Command carrying parameters needed to create a new Product.
    Decouples the presentation schema from the domain model instantiation.
    """
    company_id: UUID
    internal_code: str
    barcode: str | None
    name: str
    description: str | None
    category_id: UUID
    brand_id: UUID
    unit_id: UUID
    cost: Decimal
    price: Decimal
    tax_rate: Decimal
    controls_stock: bool
    allows_decimal: bool
    is_perishable: bool
    minimum_stock: Decimal
    status: str

class CreateProductUseCase:
    """
    Application use case responsible for creating a new Product.
    Applies business rules and instantiates the domain entity.
    """
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, command: CreateProductCommand) -> Product:
        product_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        # Domain entity is now constructed strictly inside the use case
        product = Product(
            id=product_id,
            company_id=command.company_id,
            internal_code=command.internal_code,
            barcode=command.barcode,
            name=command.name,
            description=command.description,
            category_id=command.category_id,
            brand_id=command.brand_id,
            unit_id=command.unit_id,
            cost=command.cost,
            price=command.price,
            tax_rate=command.tax_rate,
            controls_stock=command.controls_stock,
            allows_decimal=command.allows_decimal,
            is_perishable=command.is_perishable,
            minimum_stock=command.minimum_stock,
            status=command.status,
            created_at=now,
            updated_at=now,
        )

        self._validate_internal_code(product)
        self._validate_barcode(product)

        # Persist and return product
        return self.repository.create(product)

    def _validate_internal_code(self, product: Product) -> None:
        existing_by_code = self.repository.get_by_internal_code(product.company_id, product.internal_code)
        if existing_by_code is not None:
            raise ProductAlreadyExistsException("internal_code", product.internal_code, product.company_id)

    def _validate_barcode(self, product: Product) -> None:
        if product.barcode:
            existing_by_barcode = self.repository.get_by_barcode(product.company_id, product.barcode)
            if existing_by_barcode is not None:
                raise ProductAlreadyExistsException("barcode", product.barcode, product.company_id)
