from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, UniqueConstraint, UUID as SqlUUID, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.base import Base

class Credito(Base):
    __tablename__ = "credito"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    client_id: Mapped[UUID] = mapped_column(
        SqlUUID,
        ForeignKey("cliente.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    credit_limit: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False, default=0)
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
        UniqueConstraint("company_id", "client_id", name="uq_credito_company_client_id"),
    )
