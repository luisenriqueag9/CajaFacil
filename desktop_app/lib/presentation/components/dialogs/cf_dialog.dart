import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_icons.dart';
import '../buttons/cf_icon_button.dart';

/// CFDialog: Modal base oficial de CajaFácil.
///
/// Propósitos:
/// - Mostrar ventanas superpuestas con un fondo translúcido (overlay).
/// - Asegurar un atajo universal de cierre con ESC y foco correcto.
class CFDialog extends StatelessWidget {
  const CFDialog({
    super.key,
    required this.title,
    required this.child,
    this.actions,
    this.onClose,
  });

  final String title;
  final Widget child;
  final List<Widget>? actions;
  final VoidCallback? onClose;

  static Future<T?> show<T>({
    required BuildContext context,
    required String title,
    required Widget child,
    List<Widget>? actions,
    VoidCallback? onClose,
  }) {
    return showGeneralDialog<T>(
      context: context,
      barrierDismissible: true,
      barrierLabel: 'Cerrar diálogo',
      barrierColor: Colors.black.withOpacity(0.5), // Overlay de 50%
      transitionDuration: const Duration(milliseconds: 150), // Micro-animación 150ms
      pageBuilder: (context, anim1, anim2) => Container(),
      transitionBuilder: (context, anim1, anim2, childWidget) {
        final scale = 0.95 + (0.05 * anim1.value); // Escalado 95% a 100%
        return Transform.scale(
          scale: scale,
          child: Opacity(
            opacity: anim1.value,
            child: CFDialog(
              title: title,
              actions: actions,
              onClose: onClose ?? () => Navigator.of(context).pop(),
              child: child,
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return FocusScope(
      autofocus: true,
      child: KeyboardListener(
        focusNode: FocusNode(),
        onKeyEvent: (event) {
          // Escuchar atajo ESC
          if (event.logicalKey.keyLabel == 'Escape') {
            onClose?.call();
          }
        },
        child: Dialog(
          shape: const RoundedRectangleBorder(
            borderRadius: AppRadius.borderM,
          ),
          elevation: 4.0,
          backgroundColor: colorScheme.surface,
          child: Container(
            constraints: const BoxConstraints(maxWidth: 500.0),
            padding: const EdgeInsets.all(AppSpacing.m),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Cabecera
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      title,
                      style: AppTextStyles.titlePrincipal.copyWith(
                        color: colorScheme.primary,
                      ),
                    ),
                    CFIconButton(
                      icon: AppIcons.cancel,
                      onPressed: onClose,
                      tooltip: 'Cerrar diálogo (ESC)',
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.m),
                // Contenido
                Flexible(
                  child: SingleChildScrollView(
                    child: child,
                  ),
                ),
                // Acciones
                if (actions != null && actions!.isNotEmpty) ...[
                  const SizedBox(height: AppSpacing.m),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: actions!
                        .map((widget) => Padding(
                              padding: const EdgeInsets.only(left: AppSpacing.xs),
                              child: widget,
                            ))
                        .toList(),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
