# DEPRECATED: Esta ruta temporal de compatibilidad sera eliminada
# tan pronto como finalice la migracion del modulo Compra.
# Por favor, importar desde 'app.modules.compra.presentation.api.dependencies.compra_dependencies' en su lugar.

from app.modules.compra.presentation.api.dependencies.compra_dependencies import (
    get_compra_repository,
    get_unit_of_work,
    get_supplier_lookup,
    get_product_lookup,
    get_event_dispatcher,
    get_registrar_compra_use_case,
    get_anular_compra_use_case,
    get_obtener_compra_use_case as get_obtener_compra_por_id_use_case,
    get_listar_compras_use_case,
)

__all__ = [
    "get_compra_repository",
    "get_unit_of_work",
    "get_supplier_lookup",
    "get_product_lookup",
    "get_event_dispatcher",
    "get_registrar_compra_use_case",
    "get_anular_compra_use_case",
    "get_obtener_compra_por_id_use_case",
    "get_listar_compras_use_case",
]
