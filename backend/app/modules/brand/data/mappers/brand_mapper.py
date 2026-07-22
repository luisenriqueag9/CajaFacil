from app.modules.brand.data.models import Brand as DBBrand
from app.modules.brand.domain.entities.brand import Brand as DomainBrand

def to_db(domain_brand: DomainBrand) -> DBBrand:
    """
    Convert a Domain Brand entity into a SQLAlchemy database model.
    """
    return DBBrand(
        id=domain_brand.id,
        company_id=domain_brand.company_id,
        name=domain_brand.name,
        description=None,        # Domain entity has no description per approved simple design
        status=domain_brand.status,
        created_at=domain_brand.created_at,
        updated_at=domain_brand.updated_at,
    )

def to_domain(db_brand: DBBrand) -> DomainBrand:
    """
    Convert a SQLAlchemy database model into a Domain Brand entity.
    """
    return DomainBrand(
        id=db_brand.id,
        company_id=db_brand.company_id,
        name=db_brand.name,
        status=db_brand.status,
        created_at=db_brand.created_at,
        updated_at=db_brand.updated_at,
    )

def update_db_model(db_brand: DBBrand, domain_brand: DomainBrand) -> None:
    """
    Copy editable fields from the Domain Brand entity to the SQLAlchemy database model.
    """
    db_brand.name = domain_brand.name
    db_brand.status = domain_brand.status
    db_brand.updated_at = domain_brand.updated_at
