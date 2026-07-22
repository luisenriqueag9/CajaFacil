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

        # Mutate the entity (structured assignment preparing for full DDD encapsulation)
        self._apply_updates_to_entity(product, updates)

        # Validate domain invariants after mutations
        product.validate()

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

    def _apply_updates_to_entity(self, product: Product, updates: dict[str, object]) -> None:
        """
        Structured setter mapping.
        Replaces unrestricted setattr() and provides single hook to incorporate entity methods
        (like change_price, rename, etc.) in subsequent refactors.
        """
        if "internal_code" in updates:
            product.internal_code = str(updates["internal_code"])
        if "barcode" in updates:
            product.barcode = str(updates["barcode"]) if updates["barcode"] is not None else None
        if "name" in updates:
            product.name = str(updates["name"])
        if "description" in updates:
            product.description = str(updates["description"]) if updates["description"] is not None else None
        if "category_id" in updates:
            product.category_id = updates["category_id"]
        if "brand_id" in updates:
            product.brand_id = updates["brand_id"]
        if "unit_id" in updates:
            product.unit_id = updates["unit_id"]
        if "cost" in updates:
            product.cost = updates["cost"]
        if "price" in updates:
            product.price = updates["price"]
        if "tax_rate" in updates:
            product.tax_rate = updates["tax_rate"]
        if "controls_stock" in updates:
            product.controls_stock = bool(updates["controls_stock"])
        if "allows_decimal" in updates:
            product.allows_decimal = bool(updates["allows_decimal"])
        if "is_perishable" in updates:
            product.is_perishable = bool(updates["is_perishable"])
        if "minimum_stock" in updates:
            product.minimum_stock = updates["minimum_stock"]
        if "status" in updates:
            product.status = str(updates["status"])
