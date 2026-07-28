import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_text_styles.dart';

/// CFTextField: Campo de texto estándar de CajaFácil.
///
/// Propósitos:
/// - Capturar entradas alfabéticas o generales de forma consistente.
/// - Cumplir con los estados de validación, hover, focus y disabled del Design System.
class CFTextField extends StatelessWidget {
  const CFTextField({
    super.key,
    this.controller,
    this.label,
    this.placeholder,
    this.errorText,
    this.enabled = true,
    this.autofocus = false,
    this.focusNode,
    this.onChanged,
    this.onSubmitted,
    this.keyboardType = TextInputType.text,
    this.obscureText = false,
    this.prefixIcon,
    this.suffixIcon,
    this.readOnly = false,
  });

  final TextEditingController? controller;
  final String? label;
  final String? placeholder;
  final String? errorText;
  final bool enabled;
  final bool autofocus;
  final FocusNode? focusNode;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final TextInputType keyboardType;
  final bool obscureText;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final bool readOnly;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Semantics(
      textField: true,
      enabled: enabled,
      label: label ?? placeholder ?? 'Campo de texto',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          if (label != null) ...[
            Text(
              label!,
              style: AppTextStyles.cabeceraTabla.copyWith(
                fontWeight: FontWeight.w600,
                color: enabled ? colorScheme.primary : theme.disabledColor,
              ),
            ),
            const SizedBox(height: AppSpacing.xxs),
          ],
          TextField(
            controller: controller,
            focusNode: focusNode,
            enabled: enabled,
            autofocus: autofocus,
            obscureText: obscureText,
            keyboardType: keyboardType,
            onChanged: onChanged,
            onSubmitted: onSubmitted,
            readOnly: readOnly,
            style: AppTextStyles.contenidoTablaTexto.copyWith(
              color: enabled ? colorScheme.onSurface : theme.disabledColor,
            ),
            decoration: InputDecoration(
              hintText: placeholder,
              hintStyle: AppTextStyles.contenidoTablaTexto.copyWith(
                color: theme.hintColor,
              ),
              prefixIcon: prefixIcon,
              suffixIcon: suffixIcon,
              filled: !enabled,
              fillColor: theme.disabledColor.withOpacity(0.04),
              contentPadding: const EdgeInsets.symmetric(
                horizontal: AppSpacing.m,
                vertical: AppSpacing.s,
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: AppRadius.borderS,
                borderSide: BorderSide(
                  color: errorText != null
                      ? colorScheme.error
                      : colorScheme.secondary.withOpacity(0.3),
                  width: 1.0,
                ),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: AppRadius.borderS,
                borderSide: BorderSide(
                  color: errorText != null ? colorScheme.error : colorScheme.primary,
                  width: 2.0,
                ),
              ),
              disabledBorder: OutlineInputBorder(
                borderRadius: AppRadius.borderS,
                borderSide: BorderSide(
                  color: theme.disabledColor.withOpacity(0.2),
                  width: 1.0,
                ),
              ),
              errorText: errorText,
              errorStyle: AppTextStyles.badge.copyWith(
                color: colorScheme.error,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
