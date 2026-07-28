import 'package:flutter/material.dart';
import '../../theme/app_icons.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_text_styles.dart';

/// Semántica de la notificación Toast según CF-DOC-056
enum ToastType {
  success,
  error,
  info,
  warning,
}

/// CFToast: Notificación emergente auto-desvanecible oficial de CajaFácil.
///
/// Propósitos:
/// - Mostrar retroalimentación rápida sin robar el foco principal.
/// - Cumplir con los contrastes y colores semánticos aprobados.
class CFToast extends StatelessWidget {
  const CFToast({
    super.key,
    required this.message,
    this.type = ToastType.info,
    this.onClose,
  });

  final String message;
  final ToastType type;
  final VoidCallback? onClose;

  static void show(
    BuildContext context, {
    required String message,
    ToastType type = ToastType.info,
    Duration duration = const Duration(seconds: 3),
  }) {
    final scaffoldMessenger = ScaffoldMessenger.of(context);
    scaffoldMessenger.showSnackBar(
      SnackBar(
        duration: duration,
        elevation: 2.0,
        backgroundColor: Colors.transparent,
        padding: EdgeInsets.zero,
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.all(AppSpacing.m),
        content: CFToast(
          message: message,
          type: type,
          onClose: () => scaffoldMessenger.hideCurrentSnackBar(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    Color getBgColor() {
      switch (type) {
        case ToastType.success:
          return colorScheme.primary; // Verde Éxito o Primario según Tema
        case ToastType.error:
          return colorScheme.error;
        case ToastType.warning:
          return Colors.amber.shade700;
        case ToastType.info:
          return colorScheme.secondary;
      }
    }

    IconData getIcon() {
      switch (type) {
        case ToastType.success:
          return AppIcons.success;
        case ToastType.error:
          return AppIcons.error;
        case ToastType.warning:
          return AppIcons.warning;
        case ToastType.info:
          return AppIcons.info;
      }
    }

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.m,
        vertical: AppSpacing.s,
      ),
      decoration: BoxDecoration(
        color: getBgColor(),
        borderRadius: AppRadius.borderM,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 6.0,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(getIcon(), color: Colors.white, size: 20.0),
          const SizedBox(width: AppSpacing.s),
          Expanded(
            child: Text(
              message,
              style: AppTextStyles.textoToast.copyWith(
                color: Colors.white,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          if (onClose != null) ...[
            const SizedBox(width: AppSpacing.xs),
            IconButton(
              icon: const Icon(AppIcons.cancel, color: Colors.white, size: 16.0),
              onPressed: onClose,
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(minWidth: 24, minHeight: 24),
              splashRadius: 16.0,
            ),
          ],
        ],
      ),
    );
  }
}
