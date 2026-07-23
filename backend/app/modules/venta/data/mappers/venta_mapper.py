from app.modules.venta.data.models import Venta as DBVenta, VentaDetail as DBVentaDetail, VentaPayment as DBVentaPayment
from app.modules.venta.domain.entities.venta import Venta as DomainVenta, DetalleVenta as DomainDetalleVenta, FormaPagoAceptada as DomainFormaPagoAceptada

# Translation maps for status (Spanish business terms to English DB values)
STATUS_TO_DB = {
    "CONFIRMADA": "CONFIRMED",
    "ANULADA": "VOIDED"
}

STATUS_TO_DOMAIN = {
    "CONFIRMED": "CONFIRMADA",
    "VOIDED": "ANULADA"
}

def to_db(domain_venta: DomainVenta) -> DBVenta:
    """
    Translates a Domain Venta aggregate into a SQLAlchemy model.
    """
    db_status = STATUS_TO_DB.get(domain_venta.status)
    if not db_status:
        raise KeyError(f"Estado de negocio '{domain_venta.status}' inválido en traducción.")

    db_details = [
        DBVentaDetail(
            id=d.id,
            product_id=d.product_id,
            quantity=d.quantity,
            unit_price=d.unit_price,
            discount=d.discount,
            tax_rate=d.tax_rate,
            tax_amount=d.tax_amount,
            subtotal=d.subtotal,
            total=d.total
        ) for d in domain_venta.details
    ]

    db_payments = [
        DBVentaPayment(
            payment_method=p.payment_method,
            amount=p.amount,
            transaction_reference=p.transaction_reference
        ) for p in domain_venta.payments
    ]

    return DBVenta(
        id=domain_venta.id,
        company_id=domain_venta.company_id,
        box_id=domain_venta.box_id,
        user_id=domain_venta.user_id,
        client_id=domain_venta.client_id,
        invoice_number=domain_venta.invoice_number,
        subtotal=domain_venta.subtotal,
        discount=domain_venta.discount,
        tax=domain_venta.tax,
        total=domain_venta.total,
        status=db_status,
        created_at=domain_venta.created_at,
        updated_at=domain_venta.updated_at,
        details=db_details,
        payments=db_payments,
        voided_by=domain_venta.voided_by,
        voided_at=domain_venta.voided_at,
        void_reason=domain_venta.void_reason
    )

def to_domain(db_venta: DBVenta) -> DomainVenta:
    """
    Translates a SQLAlchemy DB Venta model back into a Domain Venta aggregate.
    """
    domain_status = STATUS_TO_DOMAIN.get(db_venta.status)
    if not domain_status:
        raise KeyError(f"Estado técnico de base de datos '{db_venta.status}' inválido en traducción.")

    domain_details = [
        DomainDetalleVenta(
            id=d.id,
            product_id=d.product_id,
            quantity=d.quantity,
            unit_price=d.unit_price,
            discount=d.discount,
            tax_rate=d.tax_rate,
            tax_amount=d.tax_amount,
            subtotal=d.subtotal,
            total=d.total
        ) for d in db_venta.details
    ]

    domain_payments = [
        DomainFormaPagoAceptada(
            payment_method=p.payment_method,
            amount=p.amount,
            transaction_reference=p.transaction_reference
        ) for p in db_venta.payments
    ]

    # Return constructed aggregate root. Disables post-init validation by passing pre-validated fields.
    # Dataclass post-init is called automatically, which is fine since the persisted model is already mathematically correct.
    return DomainVenta(
        id=db_venta.id,
        company_id=db_venta.company_id,
        box_id=db_venta.box_id,
        user_id=db_venta.user_id,
        client_id=db_venta.client_id,
        invoice_number=db_venta.invoice_number,
        subtotal=db_venta.subtotal,
        discount=db_venta.discount,
        tax=db_venta.tax,
        total=db_venta.total,
        status=domain_status,
        created_at=db_venta.created_at,
        updated_at=db_venta.updated_at,
        details=domain_details,
        payments=domain_payments,
        voided_by=db_venta.voided_by,
        voided_at=db_venta.voided_at,
        void_reason=db_venta.void_reason
    )

def update_db_model(db_venta: DBVenta, domain_venta: DomainVenta) -> None:
    """
    Updates the database model with modified fields from the domain aggregate root (status, void details).
    """
    db_status = STATUS_TO_DB.get(domain_venta.status)
    if not db_status:
        raise KeyError(f"Estado de negocio '{domain_venta.status}' inválido en traducción.")

    db_venta.status = db_status
    db_venta.voided_by = domain_venta.voided_by
    db_venta.voided_at = domain_venta.voided_at
    db_venta.void_reason = domain_venta.void_reason
    db_venta.updated_at = domain_venta.updated_at
