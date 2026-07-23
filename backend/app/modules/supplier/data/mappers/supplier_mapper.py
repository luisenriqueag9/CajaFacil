from app.modules.supplier.data.models import Supplier as DBSupplier
from app.modules.supplier.domain.entities.supplier import Supplier as DomainSupplier

def to_db(domain_supplier: DomainSupplier) -> DBSupplier:
    """
    Convert a Domain Supplier entity into a SQLAlchemy database model.
    """
    return DBSupplier(
        id=domain_supplier.id,
        company_id=domain_supplier.company_id,
        name=domain_supplier.name,
        tax_id=domain_supplier.tax_id,
        contact_name=domain_supplier.contact_name,
        phone=domain_supplier.phone,
        email=domain_supplier.email,
        status=domain_supplier.status,
        created_at=domain_supplier.created_at,
        updated_at=domain_supplier.updated_at,
    )

def to_domain(db_supplier: DBSupplier) -> DomainSupplier:
    """
    Convert a SQLAlchemy database model into a Domain Supplier entity.
    """
    return DomainSupplier(
        id=db_supplier.id,
        company_id=db_supplier.company_id,
        name=db_supplier.name,
        tax_id=db_supplier.tax_id,
        contact_name=db_supplier.contact_name,
        phone=db_supplier.phone,
        email=db_supplier.email,
        status=db_supplier.status,
        created_at=db_supplier.created_at,
        updated_at=db_supplier.updated_at,
    )

def update_db_model(db_supplier: DBSupplier, domain_supplier: DomainSupplier) -> None:
    """
    Copy editable fields from the Domain Supplier entity to the SQLAlchemy database model.
    """
    db_supplier.name = domain_supplier.name
    db_supplier.tax_id = domain_supplier.tax_id
    db_supplier.contact_name = domain_supplier.contact_name
    db_supplier.phone = domain_supplier.phone
    db_supplier.email = domain_supplier.email
    db_supplier.status = domain_supplier.status
    db_supplier.updated_at = domain_supplier.updated_at
