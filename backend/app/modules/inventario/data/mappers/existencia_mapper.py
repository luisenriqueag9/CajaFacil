from app.modules.inventario.data.models import ExistenciaProducto as DBExistencia
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto as DomainExistencia

def to_db(domain_existencia: DomainExistencia) -> DBExistencia:
    """
    Maps Domain ExistenciaProducto to database model.
    """
    return DBExistencia(
        id=domain_existencia.id,
        company_id=domain_existencia.company_id,
        product_id=domain_existencia.product_id,
        stock=domain_existencia.stock
    )

def to_domain(db_existencia: DBExistencia) -> DomainExistencia:
    """
    Maps database model back into Domain ExistenciaProducto.
    """
    return DomainExistencia(
        id=db_existencia.id,
        company_id=db_existencia.company_id,
        product_id=db_existencia.product_id,
        stock=db_existencia.stock
    )

def update_db_model(db_existencia: DBExistencia, domain_existencia: DomainExistencia) -> None:
    """
    Copies current stock from domain entity back into the database model.
    """
    db_existencia.stock = domain_existencia.stock
