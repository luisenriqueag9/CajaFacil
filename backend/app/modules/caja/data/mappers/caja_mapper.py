from app.modules.caja.data.models import (
    Caja as DBCaja,
    MovimientoCaja as DBMovimiento,
    ArqueoCaja as DBArqueo
)
from app.modules.caja.domain.entities.caja import (
    Caja as DomainCaja,
    MovimientoCaja as DomainMovimiento,
    ArqueoCaja as DomainArqueo
)

STATUS_TO_DB = {
    "ABIERTA": "OPEN",
    "CERRADA": "CLOSED"
}

STATUS_TO_DOMAIN = {
    "OPEN": "ABIERTA",
    "CLOSED": "CERRADA"
}

def to_db(domain_caja: DomainCaja) -> DBCaja:
    """
    Translates a Domain Caja aggregate into a SQLAlchemy model.
    """
    db_status = STATUS_TO_DB.get(domain_caja.status)
    if not db_status:
        raise KeyError(f"Estado de negocio '{domain_caja.status}' inválido en traducción de caja.")

    db_movements = [
        DBMovimiento(
            id=m.id,
            caja_id=m.caja_id,
            type=m.type,
            amount=m.amount,
            payment_method=m.payment_method,
            concept=m.concept,
            origin_document_id=m.origin_document_id,
            created_at=m.created_at
        ) for m in domain_caja.movements
    ]

    db_audits = [
        DBArqueo(
            id=a.id,
            caja_id=a.caja_id,
            physical_amount=a.physical_amount,
            system_amount=a.system_amount,
            difference=a.difference,
            created_at=a.created_at,
            supervisor_id=a.supervisor_id
        ) for a in domain_caja.audits
    ]

    return DBCaja(
        id=domain_caja.id,
        company_id=domain_caja.company_id,
        user_id=domain_caja.user_id,
        status=db_status,
        opening_balance=domain_caja.opening_balance,
        opened_at=domain_caja.opened_at,
        closed_at=domain_caja.closed_at,
        movements=db_movements,
        audits=db_audits
    )

def to_domain(db_caja: DBCaja) -> DomainCaja:
    """
    Translates a SQLAlchemy DBCaja model back into a Domain Caja aggregate.
    """
    domain_status = STATUS_TO_DOMAIN.get(db_caja.status)
    if not domain_status:
        raise KeyError(f"Estado técnico de base de datos '{db_caja.status}' inválido en traducción de caja.")

    domain_movements = [
        DomainMovimiento(
            id=m.id,
            caja_id=m.caja_id,
            type=m.type,
            amount=m.amount,
            payment_method=m.payment_method,
            concept=m.concept,
            origin_document_id=m.origin_document_id,
            created_at=m.created_at
        ) for m in db_caja.movements
    ]

    domain_audits = [
        DomainArqueo(
            id=a.id,
            caja_id=a.caja_id,
            physical_amount=a.physical_amount,
            system_amount=a.system_amount,
            difference=a.difference,
            created_at=a.created_at,
            supervisor_id=a.supervisor_id
        ) for a in db_caja.audits
    ]

    return DomainCaja(
        id=db_caja.id,
        company_id=db_caja.company_id,
        user_id=db_caja.user_id,
        status=domain_status,
        opening_balance=db_caja.opening_balance,
        opened_at=db_caja.opened_at,
        closed_at=db_caja.closed_at,
        movements=domain_movements,
        audits=domain_audits
    )

def update_db_model(db_caja: DBCaja, domain_caja: DomainCaja) -> None:
    """
    Updates the database model with modified fields from the domain aggregate root (status, closed_at).
    """
    db_status = STATUS_TO_DB.get(domain_caja.status)
    if not db_status:
        raise KeyError(f"Estado de negocio '{domain_caja.status}' inválido en traducción de caja.")

    db_caja.status = db_status
    db_caja.closed_at = domain_caja.closed_at

    # Map new movements that are not in DB yet
    existing_movement_ids = {m.id for m in db_caja.movements}
    for m in domain_caja.movements:
        if m.id not in existing_movement_ids:
            db_caja.movements.append(
                DBMovimiento(
                    id=m.id,
                    caja_id=m.caja_id,
                    type=m.type,
                    amount=m.amount,
                    payment_method=m.payment_method,
                    concept=m.concept,
                    origin_document_id=m.origin_document_id,
                    created_at=m.created_at
                )
            )

    # Map new audits that are not in DB yet
    existing_audit_ids = {a.id for a in db_caja.audits}
    for a in domain_caja.audits:
        if a.id not in existing_audit_ids:
            db_caja.audits.append(
                DBArqueo(
                    id=a.id,
                    caja_id=a.caja_id,
                    physical_amount=a.physical_amount,
                    system_amount=a.system_amount,
                    difference=a.difference,
                    created_at=a.created_at,
                    supervisor_id=a.supervisor_id
                )
            )
