from uuid import UUID
from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.repositories.product_repository import ProductRepository
from app.modules.product.domain.exceptions.product_not_found_exception import ProductNotFoundException
from app.modules.product.domain.exceptions.product_already_exists_exception import ProductAlreadyExistsException
from app.modules.product.domain.exceptions.invalid_product_exception import InvalidProductException
from app.common.exceptions import ValidationException

class UpdateProductUseCase:
    """
    Application use case responsible for updating an existing Product.
    Ensures secure property mutations and domain-driven encapsulation design.
    """
    
    # White-list of fields allowed to be updated. Attributes like id, company_id and created_at are excluded.
    ALLOWED_UPDATE_FIELDS = {
        "internal_code",
        "barcode",
        "name",
        "description",
        "category_id",
        "brand_id",
        "unit_id",
        "cost",
        "price",
        "tax_rate",
        "controls_stock",
        "allows_decimal",
        "is_perishable",
        "minimum_stock",
        "status"
    }

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: UUID, updates: dict[str, object]) -> Product:
        if not updates:
            raise ValidationException("No se enviaron campos para actualizar.")

        # Fetch product, verifying existence
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundException(product_id)

        # Validate that only allowed fields are requested for update
        for field in updates.keys():
            if field not in self.ALLOWED_UPDATE_FIELDS:
                raise InvalidProductException(
                    f"El campo '{field}' no está permitido para actualización o no existe."
                )

        # Perform uniqueness checks for code/barcode if modified
        self._validate_uniqueness_for_update(product, updates)

        # Mutate the entity (structured assignment using update_profile)
        product.update_profile(
            internal_code=updates.get("internal_code", product.internal_code),
            barcode=updates.get("barcode", product.barcode),
            name=updates.get("name", product.name),
            description=updates.get("description", product.description),
            category_id=updates.get("category_id", product.category_id),
            brand_id=updates.get("brand_id", product.brand_id),
            unit_id=updates.get("unit_id", product.unit_id),
            cost=updates.get("cost", product.cost),
            price=updates.get("price", product.price),
            tax_rate=updates.get("tax_rate", product.tax_rate),
            controls_stock=updates.get("controls_stock", product.controls_stock),
            allows_decimal=updates.get("allows_decimal", product.allows_decimal),
            is_perishable=updates.get("is_perishable", product.is_perishable),
            minimum_stock=updates.get("minimum_stock", product.minimum_stock),
            status=updates.get("status", product.status),
        )

        # Persist changes
        return self.repository.update(product)

    def _validate_uniqueness_for_update(self, product: Product, updates: dict[str, object]) -> None:
        if "internal_code" in updates:
            new_code = str(updates["internal_code"])
            if new_code != product.internal_code:
                existing = self.repository.get_by_internal_code(product.company_id, new_code)
                if existing is not None and existing.id != product.id:
                    raise ProductAlreadyExistsException("internal_code", new_code, product.company_id)

        if "barcode" in updates:
            new_barcode = updates["barcode"]
            if new_barcode and new_barcode != product.barcode:
                existing = self.repository.get_by_barcode(product.company_id, str(new_barcode))
                if existing is not None and existing.id != product.id:
                    raise ProductAlreadyExistsException("barcode", str(new_barcode), product.company_id)
