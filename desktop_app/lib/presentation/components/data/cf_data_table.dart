import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';
import '../../theme/app_text_styles.dart';

/// CFDataColumn: Estructura de columna para la tabla
class CFDataColumn {
  const CFDataColumn({
    required this.label,
    this.numeric = false,
    this.width,
  });

  final String label;
  final bool numeric;
  final double? width;
}

/// CFDataTable: Tabla de datos optimizada para el punto de venta de CajaFácil.
///
/// Propósitos:
/// - Desplegar las líneas del carrito u otros catálogos rápidamente.
/// - Resaltar la fila activa de venta seleccionada.
/// - Forzar cifras numéricas monoespaciadas alineadas a la derecha.
class CFDataTable extends StatelessWidget {
  const CFDataTable({
    super.key,
    required this.columns,
    required this.rows,
    this.selectedIndex,
    this.onRowSelected,
    this.onRowDoubleTap,
  });

  final List<CFDataColumn> columns;
  final List<List<Widget>> rows;
  final int? selectedIndex;
  final ValueChanged<int>? onRowSelected;
  final ValueChanged<int>? onRowDoubleTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Semantics(
      label: 'Tabla de datos',
      child: Table(
        columnWidths: {
          for (int i = 0; i < columns.length; i++)
            i: columns[i].width != null
                ? FixedColumnWidth(columns[i].width!)
                : const FlexColumnWidth(),
        },
        border: TableBorder(
          horizontalInside: BorderSide(
            color: colorScheme.secondary.withOpacity(0.12),
            width: 1.0,
          ),
          bottom: BorderSide(
            color: colorScheme.secondary.withOpacity(0.12),
            width: 1.0,
          ),
        ),
        children: [
          // Fila de Cabecera
          TableRow(
            decoration: BoxDecoration(
              color: colorScheme.secondary.withOpacity(0.04),
            ),
            children: columns.map((col) {
              return TableCell(
                verticalAlignment: TableCellVerticalAlignment.middle,
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.s,
                    vertical: AppSpacing.s,
                  ),
                  child: Container(
                    alignment: col.numeric ? Alignment.centerRight : Alignment.centerLeft,
                    child: Text(
                      col.label,
                      style: AppTextStyles.cabeceraTabla.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ),
              );
            }).toList(),
          ),
          // Filas de Datos
          ...rows.asMap().entries.map((entry) {
            final rowIndex = entry.key;
            final cells = entry.value;
            final isSelected = rowIndex == selectedIndex;

            final decoration = BoxDecoration(
              color: isSelected
                  ? colorScheme.primary.withOpacity(0.06) // Fila activa seleccionada (azul soft)
                  : Colors.transparent,
            );

            return TableRow(
              decoration: decoration,
              children: cells.asMap().entries.map((cellEntry) {
                final cellIndex = cellEntry.key;
                final cellWidget = cellEntry.value;
                final col = columns[cellIndex];

                return TableCell(
                  verticalAlignment: TableCellVerticalAlignment.middle,
                  child: InkWell(
                    onTap: onRowSelected != null ? () => onRowSelected!(rowIndex) : null,
                    onDoubleTap: onRowDoubleTap != null ? () => onRowDoubleTap!(rowIndex) : null,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(
                        horizontal: AppSpacing.s,
                        vertical: AppSpacing.s,
                      ),
                      child: Container(
                        alignment: col.numeric ? Alignment.centerRight : Alignment.centerLeft,
                        child: cellWidget,
                      ),
                    ),
                  ),
                );
              }).toList(),
            );
          }),
        ],
      ),
    );
  }
}
