from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.modules.product.domain.exceptions.invalid_product_exception import InvalidProductException

@dataclass
class Product:
    id: UUID
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
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        self.validate()

    def update_profile(
        self,
        *,
        internal_code: str,
        barcode: str | None,
        name: str,
        description: str | None,
        category_id: UUID,
        brand_id: UUID,
        unit_id: UUID,
        cost: Decimal,
        price: Decimal,
        tax_rate: Decimal,
        controls_stock: bool,
        allows_decimal: bool,
        is_perishable: bool,
        minimum_stock: Decimal,
        status: str,
    ) -> None:
        """
        Updates the product's details with explicit and typed parameters,
        and re-runs validations.
        """
        self.internal_code = internal_code
        self.barcode = barcode
        self.name = name
        self.description = description
        self.category_id = category_id
        self.brand_id = brand_id
        self.unit_id = unit_id
        self.cost = cost
        self.price = price
        self.tax_rate = tax_rate
        self.controls_stock = controls_stock
        self.allows_decimal = allows_decimal
        self.is_perishable = is_perishable
        self.minimum_stock = minimum_stock
        self.status = status
        self.validate()

    def deactivate(self) -> None:
        """
        Deactivates the product by setting its status to INACTIVO.
        """
        self.status = "INACTIVO"
        self.validate()

    def validate(self) -> None:
        """
        Validates the product domain invariants.
        Raises InvalidProductException if any rule is violated.
        """
        self._validate_required_fields()
        self._validate_numeric_values()
        self._validate_status()

    def _validate_required_fields(self) -> None:
        if not self.company_id:
            raise InvalidProductException("El producto debe pertenecer a una empresa (company_id es requerido).")
        if not self.internal_code or not self.internal_code.strip():
            raise InvalidProductException("El código interno del producto no puede estar vacío.")
        if not self.name or not self.name.strip():
            raise InvalidProductException("El nombre del producto no puede estar vacío.")

    def _validate_numeric_values(self) -> None:
        if self.cost < Decimal("0.00"):
            raise InvalidProductException("El costo del producto no puede ser negativo.")
        if self.price < Decimal("0.00"):
            raise InvalidProductException("El precio del producto no puede ser negativo.")
        if self.tax_rate < Decimal("0.00"):
            raise InvalidProductException("La tasa de impuesto del producto no puede ser negativa.")
        if self.minimum_stock < Decimal("0.00"):
            raise InvalidProductException("El stock mínimo del producto no puede ser negativo.")

    def _validate_status(self) -> None:
        valid_statuses = {"ACTIVO", "INACTIVO"}
        if self.status not in valid_statuses:
            raise InvalidProductException(
                f"Estado '{self.status}' no permitido. Estados válidos: ACTIVO, INACTIVO"
            )
