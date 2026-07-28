import 'package:flutter/material.dart';
import '../../theme/app_icons.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_text_styles.dart';

/// CFNumberField: Campo numérico con incrementadores/decrementadores inline.
///
/// Propósitos:
/// - Capturar cantidades y pesos con precisión matemática.
/// - Operación ágil por teclado o click en botones.
class CFNumberField extends StatefulWidget {
  const CFNumberField({
    super.key,
    this.value = 1.0,
    this.min = 0.0,
    this.max = 999999.0,
    this.step = 1.0,
    this.decimals = 2,
    this.onChanged,
    this.focusNode,
    this.autofocus = false,
    this.enabled = true,
  });

  final double value;
  final double min;
  final double max;
  final double step;
  final int decimals;
  final ValueChanged<double>? onChanged;
  final FocusNode? focusNode;
  final bool autofocus;
  final bool enabled;

  @override
  State<CFNumberField> createState() => _CFNumberFieldState();
}

class _CFNumberFieldState extends State<CFNumberField> {
  late final TextEditingController _controller;
  late double _currentValue;

  @override
  void initState() {
    super.initState();
    _currentValue = widget.value;
    _controller = TextEditingController(text: _formatValue(_currentValue));
  }

  @override
  void didUpdateWidget(CFNumberField oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.value != widget.value) {
      _currentValue = widget.value;
      _controller.text = _formatValue(_currentValue);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  String _formatValue(double val) {
    return val.toStringAsFixed(widget.decimals);
  }

  void _updateValue(double val) {
    final clamped = val.clamp(widget.min, widget.max);
    if (clamped != _currentValue) {
      setState(() {
        _currentValue = clamped;
        _controller.text = _formatValue(_currentValue);
      });
      widget.onChanged?.call(_currentValue);
    }
  }

  void _increment() {
    _updateValue(_currentValue + widget.step);
  }

  void _decrement() {
    _updateValue(_currentValue - widget.step);
  }

  void _onFieldChanged(String text) {
    final parsed = double.tryParse(text);
    if (parsed != null) {
      _currentValue = parsed.clamp(widget.min, widget.max);
      widget.onChanged?.call(_currentValue);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Semantics(
      label: 'Campo numérico',
      value: _formatValue(_currentValue),
      child: Container(
        height: 40.0,
        decoration: BoxDecoration(
          borderRadius: AppRadius.borderS,
          border: Border.all(
            color: colorScheme.secondary.withOpacity(0.2),
            width: 1.0,
          ),
          color: widget.enabled ? Colors.white : theme.disabledColor.withOpacity(0.04),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Decrement Button
            IconButton(
              icon: const Icon(AppIcons.remove, size: 16.0),
              onPressed: widget.enabled ? _decrement : null,
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(minWidth: 36, minHeight: 36),
              splashRadius: 18.0,
            ),
            // Text Input Field
            Container(
              width: 80.0,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                border: Border.symmetric(
                  vertical: BorderSide(
                    color: colorScheme.secondary.withOpacity(0.15),
                    width: 1.0,
                  ),
                ),
              ),
              child: TextField(
                controller: _controller,
                focusNode: widget.focusNode,
                autofocus: widget.autofocus,
                enabled: widget.enabled,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                textAlign: TextAlign.center,
                onChanged: _onFieldChanged,
                onSubmitted: (val) {
                  _updateValue(_currentValue);
                },
                style: AppTextStyles.contenidoTablaNumero.copyWith(
                  fontWeight: FontWeight.w600,
                  color: widget.enabled ? colorScheme.onSurface : theme.disabledColor,
                ),
                decoration: const InputDecoration(
                  isDense: true,
                  border: InputBorder.none,
                  contentPadding: EdgeInsets.symmetric(horizontal: AppSpacing.xs),
                ),
              ),
            ),
            // Increment Button
            IconButton(
              icon: const Icon(AppIcons.add, size: 16.0),
              onPressed: widget.enabled ? _increment : null,
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(minWidth: 36, minHeight: 36),
              splashRadius: 18.0,
            ),
          ],
        ),
      ),
    );
  }
}
