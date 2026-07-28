from app.modules.credito.presentation.api.dependencies.credito_dependencies import (
    get_credito_repository,
    get_cliente_repository,
    get_unit_of_work,
    get_abrir_cuenta_use_case,
    get_actualizar_limite_use_case,
    get_inactivar_cuenta_use_case,
    get_obtener_credito_use_case,
    get_listar_creditos_use_case,
    get_registrar_cargo_use_case,
    get_reversar_cargo_use_case,
)

__all__ = [
    "get_credito_repository",
    "get_cliente_repository",
    "get_unit_of_work",
    "get_abrir_cuenta_use_case",
    "get_actualizar_limite_use_case",
    "get_inactivar_cuenta_use_case",
    "get_obtener_credito_use_case",
    "get_listar_creditos_use_case",
    "get_registrar_cargo_use_case",
    "get_reversar_cargo_use_case",
]
