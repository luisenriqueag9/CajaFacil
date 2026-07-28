import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';

/// CFProgressIndicator: Barra de progreso lineal oficial de CajaFácil.
///
/// Propósito:
/// - Visualizar el progreso de sincronización o descargas de catálogos.
class CFProgressIndicator extends StatelessWidget {
  const CFProgressIndicator({
    super.key,
    required this.value,
    this.label,
  });

  /// Valor de progreso entre 0.0 y 1.0 (o null para indeterminado)
  final double? value;
  final String? label;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Semantics(
      label: label ?? 'Indicador de progreso',
      value: value != null ? '${(value! * 100).toInt()}%' : 'Indeterminado',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        mainAxisSize: MainAxisSize.min,
        children: [
          if (label != null) ...[
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  label!,
                  style: theme.textTheme.bodySmall?.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                if (value != null)
                  Text(
                    '${(value! * 100).toInt()}%',
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: colorScheme.primary,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
              ],
            ),
            const SizedBox(height: AppSpacing.xs),
          ],
          ClipRRect(
            borderRadius: AppRadius.borderS,
            child: LinearProgressIndicator(
              value: value,
              backgroundColor: colorScheme.secondary.withOpacity(0.12),
              valueColor: AlwaysStoppedAnimation<Color>(colorScheme.primary),
              minHeight: 6.0,
            ),
          ),
        ],
      ),
    );
  }
}
