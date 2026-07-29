import 'package:flutter/material.dart';
import '../../../theme/app_colors.dart';
import '../../../theme/app_spacing.dart';
import '../../../theme/app_text_styles.dart';

/// QuickActionsBar: Barra inferior de atajos de teclado del POS.
///
/// Propósito:
/// - Mostrar visualmente al cajero cuáles son las teclas rápidas de mostrador activas.
class QuickActionsBar extends StatelessWidget {
  const QuickActionsBar({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    final List<Map<String, String>> shortcuts = [
      {'key': 'ENTER', 'desc': 'Agregar producto'},
      {'key': 'DEL', 'desc': 'Eliminar'},
      {'key': 'ESC', 'desc': 'Cancelar selección'},
      {'key': 'F2', 'desc': 'Cliente'},
      {'key': 'F3', 'desc': 'Consulta'},
      {'key': 'F6', 'desc': 'Suspender'},
      {'key': 'F7', 'desc': 'Recuperar'},
      {'key': 'F12', 'desc': 'Cobrar'},
    ];

    return Container(
      height: 40.0,
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.m),
      decoration: BoxDecoration(
        color: colorScheme.primary.withOpacity(0.04),
        border: Border(
          top: BorderSide(
            color: colorScheme.secondary.withOpacity(0.12),
            width: 1.0,
          ),
        ),
      ),
      child: Center(
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: shortcuts.map((shortcut) {
              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xs),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Tecla física (Badge oscuro)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: AppSpacing.xs,
                        vertical: 2.0,
                      ),
                      decoration: BoxDecoration(
                        color: AppColors.primary,
                        borderRadius: BorderRadius.circular(4.0),
                      ),
                      child: Text(
                        shortcut['key']!,
                        style: AppTextStyles.badge.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const SizedBox(width: 4.0),
                    // Descripción
                    Text(
                      shortcut['desc']!,
                      style: AppTextStyles.cabeceraTabla.copyWith(
                        fontSize: 11.0,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    // Divisor entre atajos
                    const SizedBox(width: AppSpacing.s),
                    Container(
                      width: 1.0,
                      height: 12.0,
                      color: colorScheme.secondary.withOpacity(0.2),
                    ),
                  ],
                ),
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}
