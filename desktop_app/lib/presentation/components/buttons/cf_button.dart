import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_text_styles.dart';

/// Variantes oficiales para el botón según CF-DOC-056
enum ButtonVariant {
  primary,
  secondary,
  outline,
  destructive,
}

/// CFButton: Botón reutilizable oficial de CajaFácil (CF-ARCH-001).
///
/// Propósitos:
/// - Representar acciones de usuario consistentes en todo el POS.
/// - Cumplir con los estados Normal, Hover, Focus, Disabled y Loading de forma nativa.
///
/// Ejemplo de uso:
/// ```dart
/// CFButton(
///   label: 'Cobrar (F12)',
///   variant: ButtonVariant.primary,
///   onPressed: () => print('Cobrando...'),
/// )
/// ```
class CFButton extends StatelessWidget {
  const CFButton({
    super.key,
    required this.label,
    this.onPressed,
    this.variant = ButtonVariant.primary,
    this.icon,
    this.loading = false,
    this.enabled = true,
    this.autofocus = false,
    this.tooltip,
  });

  final String label;
  final VoidCallback? onPressed;
  final ButtonVariant variant;
  final IconData? icon;
  final bool loading;
  final bool enabled;
  final bool autofocus;
  final String? tooltip;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    // Resolver colores según la variante
    Color getBackgroundColor(Set<WidgetState> states) {
      if (states.contains(WidgetState.disabled) || !enabled || loading) {
        return theme.disabledColor.withOpacity(0.12);
      }
      switch (variant) {
        case ButtonVariant.primary:
          return colorScheme.primary;
        case ButtonVariant.secondary:
          return colorScheme.secondary.withOpacity(0.1);
        case ButtonVariant.outline:
          return Colors.transparent;
        case ButtonVariant.destructive:
          return colorScheme.error;
      }
    }

    Color getForegroundColor(Set<WidgetState> states) {
      if (states.contains(WidgetState.disabled) || !enabled || loading) {
        return theme.disabledColor;
      }
      switch (variant) {
        case ButtonVariant.primary:
          return Colors.white;
        case ButtonVariant.secondary:
          return colorScheme.secondary;
        case ButtonVariant.outline:
          return colorScheme.primary;
        case ButtonVariant.destructive:
          return Colors.white;
      }
    }

    BorderSide? getBorderSide(Set<WidgetState> states) {
      if (variant == ButtonVariant.outline) {
        final color = (states.contains(WidgetState.disabled) || !enabled || loading)
            ? theme.disabledColor
            : colorScheme.primary;
        return BorderSide(color: color, width: 1.5);
      }
      return BorderSide.none;
    }

    final buttonStyle = ButtonStyle(
      backgroundColor: WidgetStateProperty.resolveWith(getBackgroundColor),
      foregroundColor: WidgetStateProperty.resolveWith(getForegroundColor),
      side: WidgetStateProperty.resolveWith(getBorderSide),
      padding: WidgetStateProperty.all(
        const EdgeInsets.symmetric(
          horizontal: AppSpacing.m,
          vertical: AppSpacing.s,
        ),
      ),
      shape: WidgetStateProperty.all(
        const RoundedRectangleBorder(
          borderRadius: AppRadius.borderS,
        ),
      ),
      elevation: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.pressed) ||
            states.contains(WidgetState.disabled) ||
            !enabled ||
            loading) {
          return 0.0;
        }
        return 1.0;
      }),
      overlayColor: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.hovered)) {
          return Colors.black.withOpacity(0.04);
        }
        if (states.contains(WidgetState.focused) || states.contains(WidgetState.pressed)) {
          return colorScheme.primary.withOpacity(0.12);
        }
        return null;
      }),
    );

    Widget buttonContent = loading
        ? SizedBox(
            width: 20,
            height: 20,
            child: CircularProgressIndicator(
              strokeWidth: 2.0,
              valueColor: AlwaysStoppedAnimation<Color>(
                variant == ButtonVariant.primary || variant == ButtonVariant.destructive
                    ? Colors.white
                    : colorScheme.primary,
              ),
            ),
          )
        : Row(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (icon != null) ...[
                Icon(icon, size: 18),
                const SizedBox(width: AppSpacing.xs),
              ],
              Text(
                label,
                style: AppTextStyles.etiquetaBoton.copyWith(
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          );

    // Si tiene atajo visual o foco de accesibilidad
    Widget finalButton = Focus(
      autofocus: autofocus,
      child: Semantics(
        button: true,
        enabled: enabled && !loading,
        label: tooltip ?? label,
        child: OutlinedButton(
          style: buttonStyle,
          onPressed: (enabled && !loading) ? onPressed : null,
          child: buttonContent,
        ),
      ),
    );

    if (tooltip != null) {
      return Tooltip(
        message: tooltip!,
        child: finalButton,
      );
    }

    return finalButton;
  }
}
