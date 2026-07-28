import 'package:flutter/material.dart';
import '../../theme/app_icons.dart';
import '../../theme/app_spacing.dart';
import '../badges/cf_badge.dart';

/// CFStatusBar: Colección oficial de indicadores de estado técnico de CajaFácil.
///
/// Propósito:
/// - Visualizar de forma no intrusiva el estado de la sincronización de red y de periféricos.
class CFStatusBar extends StatelessWidget {
  const CFStatusBar({
    super.key,
    this.isOnline = true,
    this.isPrinterConnected = true,
    this.hasPendingSync = false,
  });

  final bool isOnline;
  final bool isPrinterConnected;
  final bool hasPendingSync;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Indicador de Conexión de Red
        CFBadge(
          label: isOnline ? 'ONLINE' : 'OFFLINE',
          icon: isOnline ? AppIcons.cloud : AppIcons.warning,
          color: isOnline ? Colors.green : Colors.red,
        ),
        const SizedBox(width: AppSpacing.xs),
        // Indicador de Impresora
        CFBadge(
          label: isPrinterConnected ? 'IMPRESORA' : 'IMP. ERROR',
          icon: AppIcons.print,
          color: isPrinterConnected ? Colors.green : Colors.amber.shade700,
        ),
        if (hasPendingSync) ...[
          const SizedBox(width: AppSpacing.xs),
          // Indicador de Sincronización Pendiente
          const CFBadge(
            label: 'PENDIENTE',
            icon: AppIcons.sync,
            color: Colors.blue,
          ),
        ],
      ],
    );
  }
}
