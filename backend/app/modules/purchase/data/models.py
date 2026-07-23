from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, UniqueConstraint, UUID as SqlUUID, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base

class Purchase(Base):
    __tablename__ = "purchase"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    supplier_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("supplier.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    
    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_condition: Mapped[str] = mapped_column(String(20), nullable=False)
    issue_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="BORRADOR")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # Relationships
    details: Mapped[list["PurchaseDetail"]] = relationship(
        "PurchaseDetail", 
        back_populates="purchase", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint("company_id", "supplier_id", "invoice_number", name="uq_purchase_company_supplier_invoice"),
    )


class PurchaseDetail(Base):
    __tablename__ = "purchase_detail"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    purchase_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("purchase.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    product_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("product.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    
    quantity: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    unit_cost: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)

    # Relationships
    purchase: Mapped["Purchase"] = relationship("Purchase", back_populates="details")
