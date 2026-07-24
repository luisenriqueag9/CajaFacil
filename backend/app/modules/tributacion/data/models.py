from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from sqlalchemy import String, DateTime, UUID as SqlUUID, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base

class ConfiguracionTributaria(Base):
    __tablename__ = "configuracion_tributaria"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    valid_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    valid_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    calculation_type: Mapped[str] = mapped_column(String(20), nullable=False, default="ADICIONADO")

    # Relationships
    rates: Mapped[list["TasaImpuesto"]] = relationship(
        "TasaImpuesto",
        back_populates="configuracion",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class TasaImpuesto(Base):
    __tablename__ = "tasa_impuesto"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    configuracion_id: Mapped[UUID] = mapped_column(
        SqlUUID,
        ForeignKey("configuracion_tributaria.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    rate_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)

    # Relationships
    configuracion: Mapped["ConfiguracionTributaria"] = relationship("ConfiguracionTributaria", back_populates="rates")
