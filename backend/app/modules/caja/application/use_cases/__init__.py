from app.modules.caja.application.use_cases.abrir_caja_use_case import AbrirSesionUseCase
from app.modules.caja.application.use_cases.cerrar_caja_use_case import CerrarSesionUseCase
from app.modules.caja.application.use_cases.registrar_movimiento_caja_use_case import RegistrarMovimientoUseCase
from app.modules.caja.application.use_cases.registrar_arqueo_caja_use_case import RegistrarArqueoUseCase
from app.modules.caja.application.use_cases.anular_movimiento_use_case import AnularMovimientoUseCase
from app.modules.caja.application.use_cases.obtener_caja_activa_use_case import ObtenerSesionUseCase
from app.modules.caja.application.use_cases.obtener_saldo_caja_use_case import ListarSesionesUseCase

# Forwarding imports for compatibility with tests
from app.modules.caja.application.commands.abrir_sesion_command import AbrirSesionCommand
from app.modules.caja.application.commands.cerrar_sesion_command import CerrarSesionCommand
from app.modules.caja.application.commands.registrar_movimiento_command import RegistrarMovimientoCommand
from app.modules.caja.application.commands.registrar_arqueo_command import RegistrarArqueoCommand
from app.modules.caja.application.commands.anular_movimiento_command import AnularMovimientoCommand
from app.modules.caja.application.queries.obtener_sesion_query import ObtenerSesionQuery
from app.modules.caja.application.queries.listar_sesiones_query import ListarSesionesQuery

# Backward compatibility stubs for existing tests
AbrirCajaUseCase = AbrirSesionUseCase
AbrirCajaCommand = AbrirSesionCommand
RegistrarMovimientoCajaUseCase = RegistrarMovimientoUseCase
RegistrarMovimientoCajaCommand = RegistrarMovimientoCommand
RegistrarArqueoCajaUseCase = RegistrarArqueoUseCase
RegistrarArqueoCajaCommand = RegistrarArqueoCommand
CerrarCajaUseCase = CerrarSesionUseCase
CerrarCajaCommand = CerrarSesionCommand
ObtenerCajaActivaUseCase = ObtenerSesionUseCase

__all__ = [
    "AbrirSesionUseCase",
    "CerrarSesionUseCase",
    "RegistrarMovimientoUseCase",
    "RegistrarArqueoUseCase",
    "AnularMovimientoUseCase",
    "ObtenerSesionUseCase",
    "ListarSesionesUseCase",
    "AbrirSesionCommand",
    "CerrarSesionCommand",
    "RegistrarMovimientoCommand",
    "RegistrarArqueoCommand",
    "AnularMovimientoCommand",
    "ObtenerSesionQuery",
    "ListarSesionesQuery",
    # Legacy stubs
    "AbrirCajaUseCase",
    "AbrirCajaCommand",
    "RegistrarMovimientoCajaUseCase",
    "RegistrarMovimientoCajaCommand",
    "RegistrarArqueoCajaUseCase",
    "RegistrarArqueoCajaCommand",
    "CerrarCajaUseCase",
    "CerrarCajaCommand",
    "ObtenerCajaActivaUseCase",
]
