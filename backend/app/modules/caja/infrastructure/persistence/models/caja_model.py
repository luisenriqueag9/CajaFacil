from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, UUID as SqlUUID, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base

class Caja(Base):
    __tablename__ = "caja"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID, 
        ForeignKey("company.id", ondelete="RESTRICT"), 
        nullable=False, 
        index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVA")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )

    # Relationship to sessions
    sessions: Mapped[list["SesionCaja"]] = relationship(
        "SesionCaja",
        back_populates="caja",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class SesionCaja(Base):
    __tablename__ = "sesion_caja"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    caja_id: Mapped[UUID] = mapped_column(
        SqlUUID,
        ForeignKey("caja.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    company_id: Mapped[UUID] = mapped_column(
        SqlUUID,
        ForeignKey("company.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    user_id: Mapped[UUID] = mapped_column(SqlUUID, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ABIERTA")
    opening_balance: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    
    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    caja: Mapped["Caja"] = relationship("Caja", back_populates="sessions")
    movements: Mapped[list["MovimientoCaja"]] = relationship(
        "MovimientoCaja",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    audits: Mapped[list["ArqueoCaja"]] = relationship(
        "ArqueoCaja",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class MovimientoCaja(Base):
    __tablename__ = "movimiento_caja"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    sesion_id: Mapped[UUID] = mapped_column(
        SqlUUID,
        ForeignKey("sesion_caja.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # INGRESO, EGRESO
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False)  # EFECTIVO, TARJETA, TRANSFERENCIA, CREDITO
    concept: Mapped[str] = mapped_column(String(100), nullable=False)
    origin_context: Mapped[str | None] = mapped_column(String(50), nullable=True)
    origin_document_id: Mapped[UUID | None] = mapped_column(SqlUUID, nullable=True, index=True)
    voided: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )

    # Relationship
    session: Mapped["SesionCaja"] = relationship("SesionCaja", back_populates="movements")


class ArqueoCaja(Base):
    __tablename__ = "arqueo_caja"

    id: Mapped[UUID] = mapped_column(SqlUUID, primary_key=True, default=uuid4)
    sesion_id: Mapped[UUID] = mapped_column(
        SqlUUID,
        ForeignKey("sesion_caja.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    physical_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    system_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    difference: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    supervisor_id: Mapped[UUID | None] = mapped_column(SqlUUID, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )

    # Relationship
    session: Mapped["SesionCaja"] = relationship("SesionCaja", back_populates="audits")
