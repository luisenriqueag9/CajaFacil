from app.modules.company.data.models import Company as DBCompany
from app.modules.company.domain.entities.company import Company as DomainCompany


def to_db(domain_company: DomainCompany) -> DBCompany:
    """
    Convert a Domain Company entity into a SQLAlchemy model.
    """
    return DBCompany(
        id=domain_company.id,
        business_name=domain_company.business_name,
        trade_name=domain_company.trade_name,
        tax_id=domain_company.tax_id,
        email=domain_company.email,
        phone=domain_company.phone,
        country=domain_company.country,
        currency=domain_company.currency,
        timezone=domain_company.timezone,
        status=domain_company.status,
        created_at=domain_company.created_at,
        updated_at=domain_company.updated_at,
    )


def to_domain(db_company: DBCompany) -> DomainCompany:
    """
    Convert a SQLAlchemy model into a Domain Company entity.
    """
    return DomainCompany(
        id=db_company.id,
        business_name=db_company.business_name,
        trade_name=db_company.trade_name,
        tax_id=db_company.tax_id,
        email=db_company.email,
        phone=db_company.phone,
        country=db_company.country,
        currency=db_company.currency,
        timezone=db_company.timezone,
        status=db_company.status,
        created_at=db_company.created_at,
        updated_at=db_company.updated_at,
    )


def update_db_model(
    db_company: DBCompany,
    domain_company: DomainCompany,
) -> None:
    """
    Copy editable fields from the Domain Company entity to the SQLAlchemy model.
    """

    db_company.business_name = domain_company.business_name
    db_company.trade_name = domain_company.trade_name
    db_company.email = domain_company.email
    db_company.phone = domain_company.phone
    db_company.currency = domain_company.currency
    db_company.timezone = domain_company.timezone
    db_company.status = domain_company.status