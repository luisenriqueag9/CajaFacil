from app.modules.tributacion.data.models import (
    ConfiguracionTributaria as DBConfig,
    TasaImpuesto as DBTasa
)
from app.modules.tributacion.domain.entities.configuracion import (
    ConfiguracionTributaria as DomainConfig,
    TasaImpuesto as DomainTasa
)

def to_db(domain_config: DomainConfig) -> DBConfig:
    """
    Converts Domain ConfiguracionTributaria to database model.
    """
    db_rates = [
        DBTasa(
            id=t.id,
            configuracion_id=t.configuracion_id,
            name=t.name,
            code=t.code,
            rate_percentage=t.rate_percentage
        ) for t in domain_config.rates
    ]

    return DBConfig(
        id=domain_config.id,
        company_id=domain_config.company_id,
        name=domain_config.name,
        is_active=domain_config.is_active,
        valid_from=domain_config.valid_from,
        valid_to=domain_config.valid_to,
        calculation_type=domain_config.calculation_type,
        rates=db_rates
    )

def to_domain(db_config: DBConfig) -> DomainConfig:
    """
    Converts database model back into Domain ConfiguracionTributaria.
    """
    domain_rates = [
        DomainTasa(
            id=t.id,
            configuracion_id=t.configuracion_id,
            name=t.name,
            code=t.code,
            rate_percentage=t.rate_percentage
        ) for t in db_config.rates
    ]

    return DomainConfig(
        id=db_config.id,
        company_id=db_config.company_id,
        name=db_config.name,
        is_active=db_config.is_active,
        valid_from=db_config.valid_from,
        valid_to=db_config.valid_to,
        calculation_type=db_config.calculation_type,
        rates=domain_rates
    )

def update_db_model(db_config: DBConfig, domain_config: DomainConfig) -> None:
    """
    Copies modifications (is_active, valid_to) from domain configuration back into the database model.
    """
    db_config.is_active = domain_config.is_active
    db_config.valid_to = domain_config.valid_to

    # Sincronize rates
    existing_rates_ids = {r.id for r in db_config.rates}
    for r in domain_config.rates:
        if r.id not in existing_rates_ids:
            db_config.rates.append(
                DBTasa(
                    id=r.id,
                    configuracion_id=r.configuracion_id,
                    name=r.name,
                    code=r.code,
                    rate_percentage=r.rate_percentage
                )
            )
