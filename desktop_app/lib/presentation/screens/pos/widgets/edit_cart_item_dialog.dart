import 'package:flutter/material.dart';
import '../../../theme/app_spacing.dart';
import '../../../components/dialogs/cf_dialog.dart';
import '../../../components/inputs/cf_text_field.dart';
import '../../../components/buttons/cf_button.dart';
import 'cart_item.dart';

/// EditCartItemDialog: Diálogo reutilizable para la edición de líneas en el POS.
class EditCartItemDialog extends StatefulWidget {
  const EditCartItemDialog({
    super.key,
    required this.item,
  });

  final CartItem item;

  @override
  State<EditCartItemDialog> createState() => _EditCartItemDialogState();
}

class _EditCartItemDialogState extends State<EditCartItemDialog> {
  late final TextEditingController _quantityController;
  late final TextEditingController _discountController;
  late final TextEditingController _observationController;

  final FocusNode _quantityFocusNode = FocusNode();
  final FocusNode _discountFocusNode = FocusNode();
  final FocusNode _observationFocusNode = FocusNode();

  String? _quantityError;
  String? _discountError;

  @override
  void initState() {
    super.initState();
    _quantityController = TextEditingController(text: widget.item.quantity.toString());
    _discountController = TextEditingController(text: widget.item.discount.toString());
    _observationController = TextEditingController(text: widget.item.observation);

    // Forzar el autofocus en el campo de cantidad
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _quantityFocusNode.requestFocus();
    });
  }

  @override
  void dispose() {
    _quantityController.dispose();
    _discountController.dispose();
    _observationController.dispose();

    _quantityFocusNode.dispose();
    _discountFocusNode.dispose();
    _observationFocusNode.dispose();
    super.dispose();
  }

  void _save() {
    setState(() {
      _quantityError = null;
      _discountError = null;
    });

    final qStr = _quantityController.text.trim();
    final dStr = _discountController.text.trim();

    // Validar cantidad
    final double? qty = double.tryParse(qStr);
    if (qty == null || qty <= 0.0) {
      setState(() {
        _quantityError = 'Ingrese una cantidad válida mayor a 0';
      });
      _quantityFocusNode.requestFocus();
      return;
    }

    // Validar descuento
    final double? discount = double.tryParse(dStr);
    if (discount == null || discount < 0.0) {
      setState(() {
        _discountError = 'Ingrese un descuento válido';
      });
      _discountFocusNode.requestFocus();
      return;
    }

    // Crear un nuevo CartItem actualizado
    final updatedItem = CartItem(
      product: widget.item.product,
      quantity: qty,
      discount: discount,
      observation: _observationController.text.trim(),
    );

    Navigator.of(context).pop(updatedItem);
  }

  @override
  Widget build(BuildContext context) {
    return CFDialog(
      title: 'Editar Línea de Venta',
      actions: [
        CFButton(
          label: 'Cancelar',
          variant: ButtonVariant.outline,
          onPressed: () => Navigator.of(context).pop(null),
        ),
        const SizedBox(width: AppSpacing.s),
        CFButton(
          label: 'Guardar',
          variant: ButtonVariant.primary,
          onPressed: _save,
        ),
      ],
      child: FocusScope(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          mainAxisSize: MainAxisSize.min,
          children: [
            // Fila 1: Producto y Código (Lectura)
            Row(
              children: [
                Expanded(
                  child: CFTextField(
                    label: 'Código',
                    controller: TextEditingController(text: widget.item.product.code),
                    readOnly: true,
                    enabled: false,
                  ),
                ),
                const SizedBox(width: AppSpacing.m),
                Expanded(
                  flex: 2,
                  child: CFTextField(
                    label: 'Producto / Descripción',
                    controller: TextEditingController(text: widget.item.product.name),
                    readOnly: true,
                    enabled: false,
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.m),

            // Fila 2: Precio (Lectura) y Cantidad (Autofocus)
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: CFTextField(
                    label: 'Precio Unitario',
                    controller: TextEditingController(
                      text: 'L ${widget.item.product.price.toStringAsFixed(2)}',
                    ),
                    readOnly: true,
                    enabled: false,
                  ),
                ),
                const SizedBox(width: AppSpacing.m),
                Expanded(
                  child: CFTextField(
                    label: 'Cantidad',
                    controller: _quantityController,
                    focusNode: _quantityFocusNode,
                    autofocus: true,
                    keyboardType: const TextInputType.numberWithOptions(decimal: true),
                    errorText: _quantityError,
                    onSubmitted: (_) => _discountFocusNode.requestFocus(),
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.m),

            // Fila 3: Descuento y Observación
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: CFTextField(
                    label: 'Descuento (L)',
                    controller: _discountController,
                    focusNode: _discountFocusNode,
                    keyboardType: const TextInputType.numberWithOptions(decimal: true),
                    errorText: _discountError,
                    onSubmitted: (_) => _observationFocusNode.requestFocus(),
                  ),
                ),
                const SizedBox(width: AppSpacing.m),
                Expanded(
                  child: CFTextField(
                    label: 'Observación (Opcional)',
                    controller: _observationController,
                    focusNode: _observationFocusNode,
                    onSubmitted: (_) => _save(),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
