import 'package:flutter/material.dart';
import '../../../theme/app_icons.dart';
import '../../../theme/app_spacing.dart';
import '../../../theme/app_text_styles.dart';
import '../../../components/layout/cf_panel.dart';
import '../../../components/data/cf_data_table.dart';
import '../../../components/data/cf_empty_state.dart';
import 'cart_item.dart';

/// SaleGridPlaceholder: Grilla del carrito de ventas interactiva del POS.
///
/// Propósitos:
/// - Mostrar dinámicamente las líneas agregadas al carrito.
/// - Resaltar la fila activa seleccionada.
/// - Permitir la selección con click de filas.
class SaleGridPlaceholder extends StatelessWidget {
  const SaleGridPlaceholder({
    super.key,
    required this.cartItems,
    this.selectedIndex,
    this.onRowSelected,
    this.onRowDoubleTap,
  });

  final List<CartItem> cartItems;
  final int? selectedIndex;
  final ValueChanged<int>? onRowSelected;
  final ValueChanged<int>? onRowDoubleTap;

  @override
  Widget build(BuildContext context) {
    // Calcular totales de líneas y unidades
    final totalLines = cartItems.length;
    final totalUnits = cartItems.fold<double>(0.0, (sum, item) => sum + item.quantity);

    // Preparar filas para la CFDataTable
    final List<List<Widget>> tableRows = cartItems.asMap().entries.map((entry) {
      final index = entry.key;
      final item = entry.value;

      return [
        Text('${index + 1}', style: AppTextStyles.contenidoTablaTexto),
        Text(item.product.code, style: AppTextStyles.contenidoTablaTexto),
        Text(item.product.name, style: AppTextStyles.contenidoTablaTexto),
        Text(
          item.quantity.toStringAsFixed(2),
          style: AppTextStyles.contenidoTablaNumero,
        ),
        Text(
          'L ${item.product.price.toStringAsFixed(2)}',
          style: AppTextStyles.contenidoTablaNumero,
        ),
        Text(
          'L ${item.discount.toStringAsFixed(2)}',
          style: AppTextStyles.contenidoTablaNumero,
        ),
        Text(
          'L ${item.total.toStringAsFixed(2)}',
          style: AppTextStyles.contenidoTablaNumero.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
      ];
    }).toList();

    return CFPanel(
      padding: EdgeInsets.zero,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Tabla de Datos
          CFDataTable(
            columns: const [
              CFDataColumn(label: '#', width: 40.0),
              CFDataColumn(label: 'Código', width: 100.0),
              CFDataColumn(label: 'Producto / Descripción'),
              CFDataColumn(label: 'Cant.', numeric: true, width: 80.0),
              CFDataColumn(label: 'Precio U.', numeric: true, width: 100.0),
              CFDataColumn(label: 'Desc.', numeric: true, width: 80.0),
              CFDataColumn(label: 'Total', numeric: true, width: 120.0),
            ],
            rows: tableRows,
            selectedIndex: selectedIndex,
            onRowSelected: onRowSelected,
            onRowDoubleTap: onRowDoubleTap,
          ),

          // Si el carrito está vacío, mostramos el empty state
          if (cartItems.isEmpty)
            const Expanded(
              child: Center(
                child: CFEmptyState(
                  icon: AppIcons.search,
                  title: 'Carrito de Ventas Vacío',
                  description: 'Escanee un código de barra o use la botonera para agregar productos.',
                ),
              ),
            )
          else
            const Expanded(child: SizedBox()), // Relleno de espacio vertical

          // Footer informativo de totales acumulados de la grilla
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.m,
              vertical: AppSpacing.s,
            ),
            decoration: BoxDecoration(
              border: Border(
                top: BorderSide(
                  color: Theme.of(context).colorScheme.secondary.withOpacity(0.12),
                  width: 1.0,
                ),
              ),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Líneas: $totalLines',
                  style: AppTextStyles.cabeceraTabla.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                ),
                Text(
                  'Unidades: ${totalUnits.toStringAsFixed(2)}',
                  style: AppTextStyles.cabeceraTabla.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
