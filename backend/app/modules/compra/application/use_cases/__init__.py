from app.modules.compra.application.use_cases.registrar_compra_use_case import RegistrarCompraUseCase
from app.modules.compra.application.use_cases.anular_compra_use_case import AnularCompraUseCase
from app.modules.compra.application.use_cases.obtener_compra_use_case import ObtenerCompraUseCase
from app.modules.compra.application.use_cases.listar_compras_use_case import ListarComprasUseCase
from app.modules.compra.application.use_cases.registrar_devolucion_use_case import RegistrarDevolucionProveedorUseCase

# Forwarding imports for backward compatibility with tests
from app.modules.compra.application.commands.registrar_compra_command import RegistrarCompraCommand, DetalleCompraCommand
from app.modules.compra.application.commands.anular_compra_command import AnularCompraCommand
from app.modules.compra.application.use_cases.obtener_compra_use_case import ObtenerCompraUseCase as ObtenerCompraPorIdUseCase

__all__ = [
    "RegistrarCompraUseCase",
    "AnularCompraUseCase",
    "ObtenerCompraUseCase",
    "ListarComprasUseCase",
    "RegistrarDevolucionProveedorUseCase",
    "RegistrarCompraCommand",
    "DetalleCompraCommand",
    "AnularCompraCommand",
    "ObtenerCompraPorIdUseCase",
]
