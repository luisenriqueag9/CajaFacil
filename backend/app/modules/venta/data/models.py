from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, UniqueConstraint, UUID as SqlUUID, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from decimal import Decimal

from app.database.base import Base

class Venta(Base):
    __tablename__ = "venta"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    box_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    client_id: Mapped[UUID | None] = mapped_column(SqlUUID, nullable=True, index=True)
    
    invoice_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    subtotal: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    discount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    tax: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="CONFIRMADA")
    
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

    # Auditing fields for voiding/annulment
    voided_by: Mapped[UUID | None] = mapped_column(SqlUUID, nullable=True)
    voided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    void_reason: Mapped[str | None] = mapped_column(String(300), nullable=True)

    # Relationships
    details: Mapped[list["VentaDetail"]] = relationship(
        "VentaDetail", 
        back_populates="venta", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    payments: Mapped[list["VentaPayment"]] = relationship(
        "VentaPayment",
        back_populates="venta",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class VentaDetail(Base):
    __tablename__ = "venta_detail"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    venta_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("venta.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    product_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("product.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    discount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    # Relationships
    venta: Mapped["Venta"] = relationship("Venta", back_populates="details")


class VentaPayment(Base):
    __tablename__ = "venta_payment"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    venta_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("venta.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    transaction_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    venta: Mapped["Venta"] = relationship("Venta", back_populates="payments")


# ==========================================
# MOCK DATABASE MODELS FOR OTHER DOMAINS
# (To support sychronous local transaction)
# ==========================================

class DBMovimientoInventario(Base):
    __tablename__ = "movimiento_inventario"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    product_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("product.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)  # SALIDA, ENTRADA
    concept: Mapped[str] = mapped_column(String(50), nullable=False)  # VENTA, ANULACION_VENTA
    reference_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)  # Venta ID
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )


class DBMovimientoCaja(Base):
    __tablename__ = "movimiento_caja"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    box_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)  # INGRESO, EGRESO
    concept: Mapped[str] = mapped_column(String(50), nullable=False)  # VENTA, ANULACION_VENTA
    reference_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)  # Venta ID
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )


class DBCredito(Base):
    __tablename__ = "credito"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    client_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    reference_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)  # Venta ID
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVO")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
