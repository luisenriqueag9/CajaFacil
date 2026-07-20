from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import String, Text, Numeric, Boolean, DateTime, UniqueConstraint, CheckConstraint, UUID as SqlUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base

class Product(Base):
    __tablename__ = "product"

    # Primary Key
    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    
    # Context field (linked via physical Foreign Key)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    
    # Identifiers
    internal_code: Mapped[str] = mapped_column(String(50), nullable=False)
    barcode: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    
    # Basic Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Domain categorization references (linked via physical Foreign Keys)
    category_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("category.id", ondelete="RESTRICT"), 
        nullable=False
    )
    brand_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("brand.id", ondelete="RESTRICT"), 
        nullable=False
    )
    unit_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("unit.id", ondelete="RESTRICT"), 
        nullable=False
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    category: Mapped["Category"] = relationship()
    brand: Mapped["Brand"] = relationship()
    unit: Mapped["Unit"] = relationship()
    
    # Financial metrics
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    
    # Inventory control flags
    controls_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    allows_decimal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_perishable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    minimum_stock: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    
    # Lifespan and administrative status
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    
    # Audit timestamps
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

    # Multi-field uniqueness constraint and field value non-negativity checks
    __table_args__ = (
        UniqueConstraint("company_id", "internal_code", name="uq_product_company_internal_code"),
        CheckConstraint("cost >= 0", name="chk_product_cost_non_negative"),
        CheckConstraint("price >= 0", name="chk_product_price_non_negative"),
        CheckConstraint("minimum_stock >= 0", name="chk_product_minimum_stock_non_negative"),
        CheckConstraint("tax_rate >= 0", name="chk_product_tax_rate_non_negative"),
    )
