# DEPRECATED: Esta ruta temporal de compatibilidad sera eliminada
# tan pronto como finalice la migracion del modulo Compra.
# Por favor, importar desde 'app.modules.compra.presentation.api.routers.compra_router' en su lugar.

from app.modules.compra.presentation.api.routers.compra_router import router

__all__ = ["router"]
