from app.modules.category.data.models import Category as DBCategory
from app.modules.category.domain.entities.category import Category as DomainCategory

def to_db(domain_category: DomainCategory) -> DBCategory:
    """
    Convert a Domain Category entity into a SQLAlchemy database model.
    """
    return DBCategory(
        id=domain_category.id,
        company_id=domain_category.company_id,
        name=domain_category.name,
        status=domain_category.status,
        protected=domain_category.protected,
        created_at=domain_category.created_at,
        updated_at=domain_category.updated_at,
    )

def to_domain(db_category: DBCategory) -> DomainCategory:
    """
    Convert a SQLAlchemy database model into a Domain Category entity.
    """
    return DomainCategory(
        id=db_category.id,
        company_id=db_category.company_id,
        name=db_category.name,
        status=db_category.status,
        protected=db_category.protected,
        created_at=db_category.created_at,
        updated_at=db_category.updated_at,
    )

def update_db_model(db_category: DBCategory, domain_category: DomainCategory) -> None:
    """
    Copy editable fields from the Domain Category entity to the SQLAlchemy database model.
    """
    db_category.name = domain_category.name
    db_category.status = domain_category.status
    db_category.protected = domain_category.protected
    db_category.updated_at = domain_category.updated_at
