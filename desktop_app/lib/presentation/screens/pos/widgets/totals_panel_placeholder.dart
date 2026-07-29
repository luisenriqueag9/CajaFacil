import 'package:flutter/material.dart';
import '../../../theme/app_colors.dart';
import '../../../theme/app_spacing.dart';
import '../../../theme/app_text_styles.dart';
import '../../../components/layout/cf_panel.dart';
import '../../../components/buttons/cf_button.dart';

/// TotalsPanelPlaceholder: Cuadro inferior de desglose e importe total de la venta.
///
/// Propósito:
/// - Presentar el total gigante a cobrar y desglose de impuestos/descuentos.
/// - Ofrecer el botón de llamada a cobro F12/Checkout.
class TotalsPanelPlaceholder extends StatelessWidget {
  const TotalsPanelPlaceholder({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        // Botones auxiliares de mostrador a la izquierda
        Expanded(
          flex: 4,
          child: Row(
            children: [
              CFButton(
                label: 'Suspender (F6)',
                variant: ButtonVariant.outline,
                onPressed: () {},
              ),
              const SizedBox(width: AppSpacing.xs),
              CFButton(
                label: 'Recuperar (F7)',
                variant: ButtonVariant.outline,
                onPressed: () {},
              ),
              const SizedBox(width: AppSpacing.xs),
              CFButton(
                label: 'Consultar (F3)',
                variant: ButtonVariant.outline,
                onPressed: () {},
              ),
            ],
          ),
        ),
        const SizedBox(width: AppSpacing.m),
        // Desglose de Totales y Botón Cobrar (Checkout)
        Expanded(
          flex: 6,
          child: CFPanel(
            color: AppColors.primary, // Fondo Slate Profundo
            border: Border.all(color: Colors.transparent),
            padding: const EdgeInsets.all(AppSpacing.s),
            child: Row(
              children: [
                // Impuestos y Descuentos desglosados
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      _buildRowDetail('SUBTOTAL:', 'L 0.00'),
                      const SizedBox(height: 4.0),
                      _buildRowDetail('ISV (15%):', 'L 0.00'),
                      const SizedBox(height: 4.0),
                      _buildRowDetail('DESCUENTOS:', 'L 0.00'),
                    ],
                  ),
                ),
                const SizedBox(width: AppSpacing.m),
                // Línea divisoria vertical
                Container(
                  width: 1.5,
                  height: 60.0,
                  color: Colors.white24,
                ),
                const SizedBox(width: AppSpacing.m),
                // Total Gigante y Botón F12
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
                    const Text(
                      'L 0.00',
                      style: TextStyle(
                        fontFamily: AppTextStyles.fontFamilyNumeric,
                        fontSize: 36.0,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
                const SizedBox(width: AppSpacing.m),
                // Botón Checkout F12
                CFButton(
                  label: 'COBRAR (F12)',
                  variant: ButtonVariant.secondary, // Botón llamativo
                  onPressed: () {},
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
