import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_icons.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_text_styles.dart';

/// CFSearchField: Campo de búsqueda oficial con soporte de foco persistente.
///
/// Propósitos:
/// - Capturar lecturas de códigos de barra (escáner) y búsquedas incrementales.
/// - Retornar el foco e identificar visualmente los atajos de teclado.
class CFSearchField extends StatefulWidget {
  const CFSearchField({
    super.key,
    this.controller,
    this.placeholder = 'Buscar o escanear producto... (F8 para catálogo)',
    this.focusNode,
    this.autofocus = true,
    this.onChanged,
    this.onSubmitted,
    this.onClear,
    this.enabled = true,
  });

  final TextEditingController? controller;
  final String placeholder;
  final FocusNode? focusNode;
  final bool autofocus;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final VoidCallback? onClear;
  final bool enabled;

  @override
  State<CFSearchField> createState() => _CFSearchFieldState();
}

class _CFSearchFieldState extends State<CFSearchField> {
  late final TextEditingController _controller;
  bool _showClear = false;

  @override
  void initState() {
    super.initState();
    _controller = widget.controller ?? TextEditingController();
    _controller.addListener(_handleTextChanged);
    _showClear = _controller.text.isNotEmpty;
  }

  @override
  void dispose() {
    if (widget.controller == null) {
      _controller.dispose();
    } else {
      _controller.removeListener(_handleTextChanged);
    }
    super.dispose();
  }

  void _handleTextChanged() {
    final hasText = _controller.text.isNotEmpty;
    if (_showClear != hasText) {
      setState(() {
        _showClear = hasText;
      });
    }
  }

  void _clear() {
    _controller.clear();
    widget.onClear?.call();
    widget.onChanged?.call('');
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Semantics(
      textField: true,
      enabled: widget.enabled,
      label: widget.placeholder,
      child: Container(
        height: 50.0,
        decoration: BoxDecoration(
          borderRadius: AppRadius.borderS,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.02),
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: TextField(
          controller: _controller,
          focusNode: widget.focusNode,
          autofocus: widget.autofocus,
          enabled: widget.enabled,
          onChanged: widget.onChanged,
          onSubmitted: widget.onSubmitted,
          style: AppTextStyles.contenidoTablaTexto.copyWith(
            fontWeight: FontWeight.w500,
          ),
          decoration: InputDecoration(
            hintText: widget.placeholder,
            hintStyle: AppTextStyles.contenidoTablaTexto.copyWith(
              color: theme.hintColor.withOpacity(0.5),
            ),
            prefixIcon: Icon(
              AppIcons.search,
              color: widget.enabled ? colorScheme.primary : theme.disabledColor,
              size: 20.0,
            ),
            suffixIcon: _showClear && widget.enabled
                ? IconButton(
                    icon: const Icon(AppIcons.clear, size: 18.0),
                    onPressed: _clear,
                    splashRadius: 20.0,
                  )
                : Container(
                    margin: const EdgeInsets.only(right: AppSpacing.s),
                    alignment: Alignment.centerRight,
                    width: 36,
                    child: CFKeyboardShortcutBadge(
                      label: 'Enter',
                      color: theme.disabledColor.withOpacity(0.12),
                    ),
                  ),
            filled: true,
            fillColor: widget.enabled ? Colors.white : theme.disabledColor.withOpacity(0.04),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.m,
              vertical: AppSpacing.s,
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: AppRadius.borderS,
              borderSide: BorderSide(
                color: colorScheme.secondary.withOpacity(0.2),
                width: 1.0,
              ),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: AppRadius.borderS,
              borderSide: BorderSide(
                color: colorScheme.primary,
                width: 2.0,
              ),
            ),
            disabledBorder: OutlineInputBorder(
              borderRadius: AppRadius.borderS,
              borderSide: BorderSide(
                color: theme.disabledColor.withOpacity(0.1),
                width: 1.0,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

/// CFKeyboardShortcutBadge: Badge pequeño de atajo de teclado inline.
class CFKeyboardShortcutBadge extends StatelessWidget {
  const CFKeyboardShortcutBadge({
    super.key,
    required this.label,
    required this.color,
  });

  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.xxs,
        vertical: 2.0,
      ),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(4.0),
      ),
      child: Text(
        label,
        style: AppTextStyles.badge.copyWith(
          fontSize: 8.0,
          color: AppColors.textSecondary,
        ),
      ),
    );
  }
}
