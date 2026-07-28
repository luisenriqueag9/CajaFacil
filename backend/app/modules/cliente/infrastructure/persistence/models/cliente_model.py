from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, UniqueConstraint, UUID as SqlUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.base import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    tax_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVO")
    
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

    __table_args__ = (
        UniqueConstraint("company_id", "tax_id", name="uq_cliente_company_tax_id"),
    )
