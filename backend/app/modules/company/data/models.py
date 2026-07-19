from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, UniqueConstraint, UUID as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database.base import Base

class Company(Base):
    __tablename__ = "company"

    # Primary Key
    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    
    # Basic corporate details
    business_name: Mapped[str] = mapped_column(String(100), nullable=False)
    trade_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Financial and identifier fields (Must be globally unique)
    tax_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # Optional contact fields
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    country: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    # Localizations
    currency: Mapped[str] = mapped_column(String(10), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)
    
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
