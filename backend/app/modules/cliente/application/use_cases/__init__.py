from app.modules.cliente.application.use_cases.registrar_cliente_use_case import RegistrarClienteUseCase
from app.modules.cliente.application.use_cases.actualizar_cliente_use_case import ActualizarClienteUseCase
from app.modules.cliente.application.use_cases.inactivar_cliente_use_case import InactivarClienteUseCase
from app.modules.cliente.application.use_cases.obtener_cliente_use_case import ObtenerClienteUseCase
from app.modules.cliente.application.use_cases.listar_clientes_use_case import ListarClientesUseCase

# Forwarding imports to mirror the Compras architecture template matching test patterns
from app.modules.cliente.application.commands.registrar_cliente_command import RegistrarClienteCommand
from app.modules.cliente.application.commands.actualizar_cliente_command import ActualizarClienteCommand
from app.modules.cliente.application.commands.inactivar_cliente_command import InactivarClienteCommand
from app.modules.cliente.application.queries.obtener_cliente_query import ObtenerClienteQuery
from app.modules.cliente.application.queries.listar_clientes_query import ListarClientesQuery

__all__ = [
    "RegistrarClienteUseCase",
    "ActualizarClienteUseCase",
    "InactivarClienteUseCase",
    "ObtenerClienteUseCase",
    "ListarClientesUseCase",
    "RegistrarClienteCommand",
    "ActualizarClienteCommand",
    "InactivarClienteCommand",
    "ObtenerClienteQuery",
    "ListarClientesQuery",
]
