from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, Text, DateTime, UniqueConstraint, UUID as SqlUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.base import Base

class Brand(Base):
    __tablename__ = "brand"

    # Primary Key
    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    
    # Context field (mandatory)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    
    # Identifiers and descriptions
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Flags and administrative configuration
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    
    # Timestamps
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

    # Unique constraints within the company context
    __table_args__ = (
        UniqueConstraint("company_id", "code", name="uq_brand_company_code"),
        UniqueConstraint("company_id", "name", name="uq_brand_company_name"),
    )
