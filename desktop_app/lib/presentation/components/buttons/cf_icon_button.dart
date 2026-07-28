import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';

/// CFIconButton: Botón de icono oficial reutilizable de CajaFácil.
///
/// Soporta estados Normal, Hover, Focus, Disabled y accesibilidad integrada.
class CFIconButton extends StatelessWidget {
  const CFIconButton({
    super.key,
    required this.icon,
    this.onPressed,
    this.enabled = true,
    this.autofocus = false,
    this.tooltip,
    this.color,
  });

  final IconData icon;
  final VoidCallback? onPressed;
  final bool enabled;
  final bool autofocus;
  final String? tooltip;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    final Color effectiveColor = color ?? colorScheme.primary;

    Widget button = Focus(
      autofocus: autofocus,
      child: Semantics(
        button: true,
        enabled: enabled,
        label: tooltip ?? 'Botón de icono',
        child: InkWell(
          borderRadius: AppRadius.borderS,
          onTap: enabled ? onPressed : null,
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.xs),
            child: Icon(
              icon,
              color: enabled ? effectiveColor : theme.disabledColor,
              size: 20.0,
            ),
          ),
        ),
      ),
    );

    if (tooltip != null) {
      return Tooltip(
        message: tooltip!,
        child: button,
      );
    }

    return button;
  }
}
