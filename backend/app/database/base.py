from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 Unified Declarative Base.
    All database models across modules must inherit from this class to participate
    in migrations and session query capabilities.
    """
    # Force default __tablename__ if desired, or let concrete classes specify
    pass

# Note: For Alembic migrations autogenerate to work, all domain models
# from modules should be imported here so Alembic gathers their metadata.
from app.modules.product.data.models import Product  # noqa: F401
from app.modules.unit.data.models import Unit  # noqa: F401
from app.modules.category.data.models import Category  # noqa: F401
from app.modules.company.data.models import Company  # noqa: F401
from app.modules.brand.data.models import Brand  # noqa: F401
from app.modules.supplier.data.models import Supplier  # noqa: F401
from app.modules.purchase.data.models import Purchase, PurchaseDetail  # noqa: F401
from app.modules.venta.data.models import Venta, VentaDetail, VentaPayment, DBMovimientoInventario, DBMovimientoCaja, DBCredito  # noqa: F401
from app.modules.inventario.data.models import MovimientoInventario as RealMovimiento, Merma as RealMerma, AjusteInventario as RealAjuste  # noqa: F401
from app.modules.caja.data.models import Caja as RealCaja, MovimientoCaja as RealMovimientoCaja, ArqueoCaja as RealArqueoCaja  # noqa: F401

