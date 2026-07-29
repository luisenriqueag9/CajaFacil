import 'package:flutter/material.dart';
import '../../../theme/app_colors.dart';
import '../../../theme/app_spacing.dart';
import '../../../theme/app_text_styles.dart';
import '../../../components/layout/cf_panel.dart';
import '../../../components/buttons/cf_button.dart';

/// TotalsPanelPlaceholder: Cuadro inferior de desglose e importe total del POS.
///
/// Propósito:
/// - Presentar de forma clara los totales calculados acumulativos.
/// - Ofrecer botones para suspender/recuperar/consultar y cobrar.
class TotalsPanelPlaceholder extends StatelessWidget {
  const TotalsPanelPlaceholder({
    super.key,
    required this.subtotal,
    required this.tax,
    required this.discount,
    required this.total,
    this.onCheckout,
    this.onSuspend,
    this.onResume,
    this.onQuery,
  });

  final double subtotal;
  final double tax;
  final double discount;
  final double total;
  final VoidCallback? onCheckout;
  final VoidCallback? onSuspend;
  final VoidCallback? onResume;
  final VoidCallback? onQuery;

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        // Acciones auxiliares a la izquierda
        Expanded(
          flex: 4,
          child: Row(
            children: [
              CFButton(
                label: 'Suspender (F6)',
                variant: ButtonVariant.outline,
                onPressed: onSuspend,
              ),
              const SizedBox(width: AppSpacing.xs),
              CFButton(
                label: 'Recuperar (F7)',
                variant: ButtonVariant.outline,
                onPressed: onResume,
              ),
              const SizedBox(width: AppSpacing.xs),
              CFButton(
                label: 'Consultar (F3)',
                variant: ButtonVariant.outline,
                onPressed: onQuery,
              ),
            ],
          ),
        ),
        const SizedBox(width: AppSpacing.m),
        // Desglose de importes y botón cobrar a la derecha
        Expanded(
          flex: 6,
          child: CFPanel(
            color: AppColors.primary,
            border: Border.all(color: Colors.transparent),
            padding: const EdgeInsets.all(AppSpacing.s),
            child: Row(
              children: [
                // Impuestos y Descuentos
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      _buildRowDetail('SUBTOTAL:', 'L ${subtotal.toStringAsFixed(2)}'),
                      const SizedBox(height: 4.0),
                      _buildRowDetail('ISV (15%):', 'L ${tax.toStringAsFixed(2)}'),
                      const SizedBox(height: 4.0),
                      _buildRowDetail('DESCUENTOS:', 'L ${discount.toStringAsFixed(2)}'),
                    ],
                  ),
                ),
                const SizedBox(width: AppSpacing.m),
                // Separador
                Container(
                  width: 1.5,
                  height: 60.0,
                  color: Colors.white24,
                ),
                const SizedBox(width: AppSpacing.m),
                // Total
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      'TOTAL A PAGAR:',
                      style: AppTextStyles.badge.copyWith(
                        color: Colors.white70,
                      ),
                    ),
                    Text(
                      'L ${total.toStringAsFixed(2)}',
                      style: const TextStyle(
                        fontFamily: AppTextStyles.fontFamilyNumeric,
                        fontSize: 32.0,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
                const SizedBox(width: AppSpacing.m),
                // Botón Cobrar
                CFButton(
                  label: 'COBRAR (F12)',
                  variant: ButtonVariant.secondary,
                  onPressed: onCheckout,
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildRowDetail(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: AppTextStyles.badge.copyWith(
            color: Colors.white70,
          ),
        ),
        Text(
          value,
          style: AppTextStyles.contenidoTablaNumero.copyWith(
            color: Colors.white,
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
    );
  }
}
