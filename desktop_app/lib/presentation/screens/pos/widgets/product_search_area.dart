import 'package:flutter/material.dart';
import '../../../theme/app_spacing.dart';
import '../../../theme/app_text_styles.dart';
import '../../../components/inputs/cf_search_field.dart';

/// ProductSearchArea: Panel superior de la pantalla de venta que gestiona el foco y el cliente.
class ProductSearchArea extends StatelessWidget {
  const ProductSearchArea({
    super.key,
    required this.focusNode,
  });

  final FocusNode focusNode;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.min,
      children: [
        // Fila de Info del Cliente
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Text(
                  'CLIENTE: ',
                  style: AppTextStyles.cabeceraTabla.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                Text(
                  'Consumidor Final (F2)',
                  style: AppTextStyles.contenidoTablaTexto.copyWith(
                    color: colorScheme.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            Text(
              'Búsqueda Directa / Escáner Activo',
              style: AppTextStyles.badge.copyWith(
                color: colorScheme.secondary,
              ),
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.xs),
        // Buscador de foco persistente
        CFSearchField(
          focusNode: focusNode,
          placeholder: 'Escanee código de barra o busque producto aquí... (F8 para catálogo)',
        ),
      ],
    );
  }
}
