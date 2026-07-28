from app.modules.cliente.presentation.api.dependencies.cliente_dependencies import (
    get_cliente_repository,
    get_unit_of_work,
    get_registrar_cliente_use_case,
    get_actualizar_cliente_use_case,
    get_inactivar_cliente_use_case,
    get_obtener_cliente_use_case,
    get_listar_clientes_use_case,
)

__all__ = [
    "get_cliente_repository",
    "get_unit_of_work",
    "get_registrar_cliente_use_case",
    "get_actualizar_cliente_use_case",
    "get_inactivar_cliente_use_case",
    "get_obtener_cliente_use_case",
    "get_listar_clientes_use_case",
]
