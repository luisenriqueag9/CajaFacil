from app.modules.product.data.models import Product as DBProduct
from app.modules.product.domain.entities.product import Product as DomainProduct

# Status translation maps
DOMAIN_TO_DB_STATUS = {
    "ACTIVO": "ACTIVE",
    "INACTIVO": "INACTIVE"
}

DB_TO_DOMAIN_STATUS = {
    "ACTIVE": "ACTIVO",
    "INACTIVE": "INACTIVO"
}

def to_db_status(domain_status: str) -> str:
    """
    Translate status from domain language to database value.
    Raises KeyError if status is invalid (no silent fallback).
    """
    return DOMAIN_TO_DB_STATUS[domain_status]

def to_domain_status(db_status: str) -> str:
    """
    Translate status from database value to domain language.
    Raises KeyError if status is invalid (no silent fallback).
    """
    return DB_TO_DOMAIN_STATUS[db_status]

def to_db(domain_product: DomainProduct) -> DBProduct:
    """
    Convert a Domain Product entity into a SQLAlchemy database model.
    """
    return DBProduct(
        id=domain_product.id,
        company_id=domain_product.company_id,
        internal_code=domain_product.internal_code,
        barcode=domain_product.barcode,
        name=domain_product.name,
        description=domain_product.description,
        category_id=domain_product.category_id,
        brand_id=domain_product.brand_id,
        unit_id=domain_product.unit_id,
        cost=domain_product.cost,
        price=domain_product.price,
        tax_rate=domain_product.tax_rate,
        controls_stock=domain_product.controls_stock,
        allows_decimal=domain_product.allows_decimal,
        is_perishable=domain_product.is_perishable,
        minimum_stock=domain_product.minimum_stock,
        status=to_db_status(domain_product.status),
        created_at=domain_product.created_at,
        updated_at=domain_product.updated_at,
    )

def to_domain(db_product: DBProduct) -> DomainProduct:
    """
    Convert a SQLAlchemy database model into a Domain Product entity.
    """
    return DomainProduct(
        id=db_product.id,
        company_id=db_product.company_id,
        internal_code=db_product.internal_code,
        barcode=db_product.barcode,
        name=db_product.name,
        description=db_product.description,
        category_id=db_product.category_id,
        brand_id=db_product.brand_id,
        unit_id=db_product.unit_id,
        cost=db_product.cost,
        price=db_product.price,
        tax_rate=db_product.tax_rate,
        controls_stock=db_product.controls_stock,
        allows_decimal=db_product.allows_decimal,
        is_perishable=db_product.is_perishable,
        minimum_stock=db_product.minimum_stock,
        status=to_domain_status(db_product.status),
        created_at=db_product.created_at,
        updated_at=db_product.updated_at,
    )

def update_db_model(db_product: DBProduct, domain_product: DomainProduct) -> None:
    """
    Copy editable fields from the Domain Product entity to the SQLAlchemy model.
    """
    # Core details
    db_product.internal_code = domain_product.internal_code
    db_product.barcode = domain_product.barcode
    db_product.name = domain_product.name
    db_product.description = domain_product.description
    
    # Categorization and links
    db_product.category_id = domain_product.category_id
    db_product.brand_id = domain_product.brand_id
    db_product.unit_id = domain_product.unit_id
    
    # Numerical and flags
    db_product.cost = domain_product.cost
    db_product.price = domain_product.price
    db_product.tax_rate = domain_product.tax_rate
    db_product.controls_stock = domain_product.controls_stock
    db_product.allows_decimal = domain_product.allows_decimal
    db_product.is_perishable = domain_product.is_perishable
    db_product.minimum_stock = domain_product.minimum_stock
    
    # Status
    db_product.status = to_db_status(domain_product.status)
    
    # Audit updated_at
    db_product.updated_at = domain_product.updated_at
