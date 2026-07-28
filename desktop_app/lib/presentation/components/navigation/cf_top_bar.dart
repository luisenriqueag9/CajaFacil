import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_text_styles.dart';
import 'cf_status_bar.dart';

/// CFTopBar: Barra superior oficial y persistente de CajaFácil POS.
///
/// Propósito:
/// - Mostrar el contexto operativo del cajero y los metadatos de auditoría en cabecera (CF-DOC-058).
class CFTopBar extends StatelessWidget {
  const CFTopBar({
    super.key,
    required this.userName,
    required this.branchName,
    required this.posTerminalName,
    this.isOnline = true,
    this.isPrinterConnected = true,
    this.hasPendingSync = false,
    this.currentTime = '12:00',
    this.onLogout,
  });

  final String userName;
  final String branchName;
  final String posTerminalName;
  final bool isOnline;
  final bool isPrinterConnected;
  final bool hasPendingSync;
  final String currentTime;
  final VoidCallback? onLogout;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      height: 50.0,
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.m),
      decoration: BoxDecoration(
        color: colorScheme.primary, // Gris Slate Profundo
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            blurRadius: 4.0,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // Sección de Logotipo y Título de App
          Row(
            children: [
              Text(
                'CajaFácil POS',
                style: AppTextStyles.etiquetaBoton.copyWith(
                  color: Colors.white,
                  fontSize: 16.0,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(width: AppSpacing.s),
              Container(
                width: 1.5,
                height: 20.0,
                color: Colors.white24,
              ),
              const SizedBox(width: AppSpacing.s),
              // Contexto de Auditoría
              Text(
                'Sucursal: $branchName | Terminal: $posTerminalName | Cajero: $userName',
                style: AppTextStyles.cabeceraTabla.copyWith(
                  color: Colors.white.withOpacity(0.7),
                  fontSize: 12.0,
                ),
              ),
            ],
          ),
          // Sección de Estados y Reloj
          Row(
            children: [
              CFStatusBar(
                isOnline: isOnline,
                isPrinterConnected: isPrinterConnected,
                hasPendingSync: hasPendingSync,
              ),
              const SizedBox(width: AppSpacing.s),
              Text(
                currentTime,
                style: AppTextStyles.contenidoTablaNumero.copyWith(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
              if (onLogout != null) ...[
                const SizedBox(width: AppSpacing.s),
                IconButton(
                  icon: const Icon(Icons.logout_rounded, color: Colors.white70, size: 18.0),
                  onPressed: onLogout,
                  tooltip: 'Cerrar sesión',
                  splashRadius: 20.0,
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }
}
