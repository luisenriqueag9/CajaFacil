import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';

/// CFPanel: Contenedor estructural oficial de CajaFácil.
///
/// Propósitos:
/// - Agrupar componentes con un color de fondo y bordes consistentes.
class CFPanel extends StatelessWidget {
  const CFPanel({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(AppSpacing.m),
    this.color,
    this.border,
  });

  final Widget child;
  final EdgeInsetsGeometry padding;
  final Color? color;
  final Border? border;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      padding: padding,
      decoration: BoxDecoration(
        color: color ?? colorScheme.surface,
        borderRadius: AppRadius.borderM,
        border: border ??
            Border.all(
              color: colorScheme.secondary.withOpacity(0.12),
              width: 1.0,
            ),
      ),
      child: child,
    );
  }
}
