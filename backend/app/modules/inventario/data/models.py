from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from sqlalchemy import String, DateTime, UUID as SqlUUID, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base

class MovimientoInventario(Base):
    __tablename__ = "movimiento_inventario"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    product_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("product.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # ENTRADA, SALIDA
    concept: Mapped[str] = mapped_column(String(50), nullable=False)  # COMPRA, VENTA, MERMA, etc.
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    origin_document_id: Mapped[UUID | None] = mapped_column(SqlUUID, nullable=True, index=True)
    
    notes: Mapped[str | None] = mapped_column(String(300), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    created_by: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)

    # Relationships
    merma: Mapped["Merma | None"] = relationship(
        "Merma",
        back_populates="movimiento",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False
    )
    ajuste: Mapped["AjusteInventario | None"] = relationship(
        "AjusteInventario",
        back_populates="movimiento",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False
    )


class Merma(Base):
    __tablename__ = "merma"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    movimiento_id: Mapped[UUID] = mapped_column(
        SqlUUID,
        ForeignKey("movimiento_inventario.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    reason: Mapped[str] = mapped_column(String(30), nullable=False)  # ROTURA, VENCIMIENTO, ROBO, OTRO
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Relationships
    movimiento: Mapped["MovimientoInventario"] = relationship("MovimientoInventario", back_populates="merma")


class AjusteInventario(Base):
    __tablename__ = "ajuste_inventario"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    movimiento_id: Mapped[UUID] = mapped_column(
        SqlUUID,
        ForeignKey("movimiento_inventario.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    physical_quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    system_quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    difference: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    # Relationships
    movimiento: Mapped["MovimientoInventario"] = relationship("MovimientoInventario", back_populates="ajuste")
