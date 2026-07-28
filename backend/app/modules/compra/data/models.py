# DEPRECATED: Esta carpeta temporal de compatibilidad sera eliminada
# tan pronto como finalice la migracion del modulo Compra.
# Por favor, importar desde 'app.modules.compra.infrastructure.persistence.models' en su lugar.

from app.modules.compra.infrastructure.persistence.models.compra_model import Compra, DetalleCompra

__all__ = ["Compra", "DetalleCompra"]
