import 'package:flutter/material.dart';
import '../../../theme/app_icons.dart';
import '../../../theme/app_spacing.dart';
import '../../../components/layout/cf_panel.dart';
import '../../../components/data/cf_data_table.dart';
import '../../../components/data/cf_empty_state.dart';

/// SaleGridPlaceholder: Representación visual simulada del carrito de compras.
///
/// Propósito:
/// - Dibujar las columnas oficiales de la grilla de ventas.
/// - Mostrar el estado vacío inicial (`CFEmptyState`) cuando no hay productos.
class SaleGridPlaceholder extends StatelessWidget {
  const SaleGridPlaceholder({super.key});

  @override
  Widget build(BuildContext context) {
    return CFPanel(
      padding: EdgeInsets.zero, // Padding administrado por celdas
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Grilla de Datos (Header)
          const CFDataTable(
            columns: [
              CFDataColumn(label: '#', width: 40.0),
              CFDataColumn(label: 'Código', width: 120.0),
              CFDataColumn(label: 'Producto / Descripción'),
              CFDataColumn(label: 'Cant.', numeric: true, width: 80.0),
              CFDataColumn(label: 'Precio U.', numeric: true, width: 100.0),
              CFDataColumn(label: 'Desc.', numeric: true, width: 80.0),
              CFDataColumn(label: 'Total', numeric: true, width: 120.0),
            ],
            rows: [], // Inicialmente vacío
          ),
          // Estado Vacío Integrado en el Cuerpo de la Grilla
          const Expanded(
            child: Center(
              child: CFEmptyState(
                icon: AppIcons.search,
                title: 'Carrito de Ventas Vacío',
                description: 'Escanee un código de barra o use la búsqueda superior para ingresar productos.',
              ),
            ),
          ),
          // Footer de Resumen Rápido de Ítems
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
            child: const Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Líneas: 0',
                  style: TextStyle(fontWeight: FontWeight.w600),
                ),
                Text(
                  'Unidades: 0.00',
                  style: TextStyle(fontWeight: FontWeight.w600),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
