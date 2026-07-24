from app.modules.inventario.application.use_cases.registrar_movimiento_use_case import (
    RegistrarMovimientoUseCase,
    RegistrarMovimientoCommand
)
from app.modules.inventario.application.use_cases.registrar_merma_use_case import (
    RegistrarMermaUseCase,
    RegistrarMermaCommand
)
from app.modules.inventario.application.use_cases.registrar_ajuste_use_case import (
    RegistrarAjusteUseCase,
    RegistrarAjusteCommand
)
from app.modules.inventario.application.use_cases.obtener_stock_producto_use_case import ObtenerStockProductoUseCase
from app.modules.inventario.application.use_cases.listar_movimientos_use_case import ListarMovimientosUseCase
from app.modules.inventario.application.use_cases.consultar_existencia_use_case import ConsultarExistenciaUseCase
from app.modules.inventario.application.use_cases.recalcular_existencia_use_case import RecalcularExistenciaDesdeKardexUseCase
