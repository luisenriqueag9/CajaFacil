from app.modules.purchase.data.models import Purchase as DBPurchase, PurchaseDetail as DBPurchaseDetail
from app.modules.purchase.domain.entities.purchase import Purchase as DomainPurchase
from app.modules.purchase.domain.entities.purchase_detail import PurchaseDetail as DomainPurchaseDetail

def to_db(domain_purchase: DomainPurchase) -> DBPurchase:
    """
    Convert a Domain Purchase entity into a SQLAlchemy database model.
    """
    db_purchase = DBPurchase(
        id=domain_purchase.id,
        company_id=domain_purchase.company_id,
        supplier_id=domain_purchase.supplier_id,
        invoice_number=domain_purchase.invoice_number,
        payment_condition=domain_purchase.payment_condition,
        issue_date=domain_purchase.issue_date,
        status=domain_purchase.status,
        created_at=domain_purchase.created_at,
        updated_at=domain_purchase.updated_at,
    )
    
    db_purchase.details = [
        DBPurchaseDetail(
            id=item.id,
            purchase_id=item.purchase_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_cost=item.unit_cost
        )
        for item in domain_purchase.items
    ]
    return db_purchase

def to_domain(db_purchase: DBPurchase) -> DomainPurchase:
    """
    Convert a SQLAlchemy database model into a Domain Purchase entity.
    """
    items = [
        DomainPurchaseDetail(
            id=item.id,
            purchase_id=item.purchase_id,
            product_id=item.product_id,
            quantity=float(item.quantity),
            unit_cost=float(item.unit_cost)
        )
        for item in db_purchase.details
    ]
    
    return DomainPurchase(
        id=db_purchase.id,
        company_id=db_purchase.company_id,
        supplier_id=db_purchase.supplier_id,
        invoice_number=db_purchase.invoice_number,
        payment_condition=db_purchase.payment_condition,
        issue_date=db_purchase.issue_date,
        status=db_purchase.status,
        created_at=db_purchase.created_at,
        updated_at=db_purchase.updated_at,
        items=items
    )

def update_db_model(db_purchase: DBPurchase, domain_purchase: DomainPurchase) -> None:
    """
    Copy editable fields from the Domain Purchase entity to the SQLAlchemy database model.
    """
    db_purchase.status = domain_purchase.status
    db_purchase.updated_at = domain_purchase.updated_at
    
    # Details are immutable once confirmed, but during draft we might update items:
    # Remove existing and recreate
    db_purchase.details.clear()
    db_purchase.details.extend([
        DBPurchaseDetail(
            id=item.id,
            purchase_id=item.purchase_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_cost=item.unit_cost
        )
        for item in domain_purchase.items
    ])
