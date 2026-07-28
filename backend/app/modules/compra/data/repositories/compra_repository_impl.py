# DEPRECATED: Esta carpeta temporal de compatibilidad sera eliminada
# tan pronto como finalice la migracion del modulo Compra.
# Por favor, importar desde 'app.modules.compra.infrastructure.persistence.repositories' en su lugar.

from app.modules.compra.infrastructure.persistence.repositories.compra_repository_impl import CompraRepositoryImpl

__all__ = ["CompraRepositoryImpl"]
