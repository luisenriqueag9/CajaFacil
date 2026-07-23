from app.modules.inventario.data.models import (
    MovimientoInventario as DBMovimiento,
    Merma as DBMerma,
    AjusteInventario as DBAjuste
)
from app.modules.inventario.domain.entities.movimiento import (
    MovimientoInventario as DomainMovimiento,
    Merma as DomainMerma,
    AjusteInventario as DomainAjuste
)

def to_db(domain_mov: DomainMovimiento) -> DBMovimiento:
    """
    Translates a Domain MovimientoInventario aggregate into a SQLAlchemy model.
    """
    db_merma = None
    if domain_mov.merma is not None:
        db_merma = DBMerma(
            id=domain_mov.merma.id,
            reason=domain_mov.merma.reason,
            description=domain_mov.merma.description
        )

    db_ajuste = None
    if domain_mov.ajuste is not None:
        db_ajuste = DBAjuste(
            id=domain_mov.ajuste.id,
            physical_quantity=domain_mov.ajuste.physical_quantity,
            system_quantity=domain_mov.ajuste.system_quantity,
            difference=domain_mov.ajuste.difference
        )

    return DBMovimiento(
        id=domain_mov.id,
        company_id=domain_mov.company_id,
        product_id=domain_mov.product_id,
        type=domain_mov.type,
        concept=domain_mov.concept,
        quantity=domain_mov.quantity,
        origin_document_id=domain_mov.origin_document_id,
        notes=domain_mov.notes,
        created_at=domain_mov.created_at,
        created_by=domain_mov.created_by,
        merma=db_merma,
        ajuste=db_ajuste
    )

def to_domain(db_mov: DBMovimiento) -> DomainMovimiento:
    """
    Translates a SQLAlchemy DBMovimiento model into a Domain MovimientoInventario aggregate.
    """
    domain_merma = None
    if db_mov.merma is not None:
        domain_merma = DomainMerma(
            id=db_mov.merma.id,
            reason=db_mov.merma.reason,
            description=db_mov.merma.description
        )

    domain_ajuste = None
    if db_mov.ajuste is not None:
        domain_ajuste = DomainAjuste(
            id=db_mov.ajuste.id,
            physical_quantity=db_mov.ajuste.physical_quantity,
            system_quantity=db_mov.ajuste.system_quantity,
            difference=db_mov.ajuste.difference
        )

    # Disable post-init validation by passing pre-validated fields
    return DomainMovimiento(
        id=db_mov.id,
        company_id=db_mov.company_id,
        product_id=db_mov.product_id,
        type=db_mov.type,
        concept=db_mov.concept,
        quantity=db_mov.quantity,
        origin_document_id=db_mov.origin_document_id,
        notes=db_mov.notes,
        created_at=db_mov.created_at,
        created_by=db_mov.created_by,
        merma=domain_merma,
        ajuste=domain_ajuste
    )
