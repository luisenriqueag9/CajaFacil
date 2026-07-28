import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../buttons/cf_button.dart';
import '../inputs/cf_text_field.dart';
import 'cf_dialog.dart';

/// CFConfirmDialog: Diálogo de confirmación destructiva o validación de supervisor.
///
/// Propósitos:
/// - Confirmar la limpieza de ventas, cierres o retiros de caja.
/// - Opcionalmente solicitar un código PIN para autorización del supervisor.
class CFConfirmDialog extends StatefulWidget {
  const CFConfirmDialog({
    super.key,
    required this.message,
    this.confirmLabel = 'Confirmar',
    this.cancelLabel = 'Cancelar',
    this.requiresSupervisorPin = false,
    this.onConfirm,
    this.onCancel,
  });

  final String message;
  final String confirmLabel;
  final String cancelLabel;
  final bool requiresSupervisorPin;
  final ValueChanged<String?>? onConfirm; // Retorna el PIN si aplica
  final VoidCallback? onCancel;

  static Future<T?> show<T>({
    required BuildContext context,
    required String title,
    required String message,
    String confirmLabel = 'Confirmar',
    String cancelLabel = 'Cancelar',
    bool requiresSupervisorPin = false,
    required ValueChanged<String?>? onConfirm,
    VoidCallback? onCancel,
  }) {
    return CFDialog.show<T>(
      context: context,
      title: title,
      onClose: () {
        onCancel?.call();
        Navigator.of(context).pop();
      },
      child: CFConfirmDialog(
        message: message,
        confirmLabel: confirmLabel,
        cancelLabel: cancelLabel,
        requiresSupervisorPin: requiresSupervisorPin,
        onConfirm: (pin) {
          onConfirm?.call(pin);
          Navigator.of(context).pop(pin);
        },
        onCancel: () {
          onCancel?.call();
          Navigator.of(context).pop();
        },
      ),
    );
  }

  @override
  State<CFConfirmDialog> createState() => _CFConfirmDialogState();
}

class _CFConfirmDialogState extends State<CFConfirmDialog> {
  final TextEditingController _pinController = TextEditingController();
  String? _errorText;

  @override
  void dispose() {
    _pinController.dispose();
    super.dispose();
  }

  void _submit() {
    if (widget.requiresSupervisorPin) {
      final pin = _pinController.text.trim();
      if (pin.length < 4) {
        setState(() {
          _errorText = 'El PIN de supervisor debe tener al menos 4 dígitos';
        });
        return;
      }
      widget.onConfirm?.call(pin);
    } else {
      widget.onConfirm?.call(null);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Mensaje descriptivo
        Text(
          widget.message,
          style: const TextStyle(fontSize: 14.0, height: 1.4),
        ),
        if (widget.requiresSupervisorPin) ...[
          const SizedBox(height: AppSpacing.m),
          CFTextField(
            controller: _pinController,
            label: 'PIN de Supervisor requerido',
            placeholder: 'Ingrese el PIN de 4 dígitos',
            obscureText: true,
            keyboardType: TextInputType.number,
            autofocus: true,
            errorText: _errorText,
            onSubmitted: (val) => _submit(),
          ),
        ],
        const SizedBox(height: AppSpacing.l),
        // Acciones
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            CFButton(
              label: widget.cancelLabel,
              variant: ButtonVariant.secondary,
              onPressed: widget.onCancel,
            ),
            const SizedBox(width: AppSpacing.xs),
            CFButton(
              label: widget.confirmLabel,
              variant: widget.requiresSupervisorPin || widget.confirmLabel == 'Anular' || widget.confirmLabel == 'Borrar'
                  ? ButtonVariant.destructive
                  : ButtonVariant.primary,
              onPressed: _submit,
            ),
          ],
        ),
      ],
    );
  }
}
