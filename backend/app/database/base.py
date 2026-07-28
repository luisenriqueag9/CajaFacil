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
from app.modules.compra.data.models import Compra, DetalleCompra  # noqa: F401
from app.modules.venta.data.models import Venta, VentaDetail, VentaPayment  # noqa: F401
from app.modules.inventario.data.models import MovimientoInventario as RealMovimiento, Merma as RealMerma, AjusteInventario as RealAjuste, ExistenciaProducto as RealExistenciaProducto  # noqa: F401
from app.modules.caja.infrastructure.persistence.models.caja_model import Caja as RealCaja, SesionCaja as RealSesionCaja, MovimientoCaja as RealMovimientoCaja, ArqueoCaja as RealArqueoCaja  # noqa: F401
from app.modules.tributacion.data.models import ConfiguracionTributaria as RealConfigTributaria, TasaImpuesto as RealTasaImpuesto  # noqa: F401
from app.modules.cliente.infrastructure.persistence.models.cliente_model import Cliente as RealCliente  # noqa: F401
from app.modules.credito.infrastructure.persistence.models.credito_model import Credito as RealCredito  # noqa: F401



