import 'package:flutter/material.dart';
import '../../../theme/app_spacing.dart';
import '../../../theme/app_text_styles.dart';
import '../../../../app/modules/product/presentation/models/product_search_result.dart';

/// SearchResultTile: Celda de resultado individual en el panel de autocompletado.
class SearchResultTile extends StatelessWidget {
  const SearchResultTile({
    super.key,
    required this.product,
    required this.isHighlighted,
    required this.onTap,
  });

  final ProductSearchResult product;
  final bool isHighlighted;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Semantics(
      button: true,
      selected: isHighlighted,
      label: 'Producto: ${product.name}, Código: ${product.code}, Precio: L ${product.price.toStringAsFixed(2)}',
      child: InkWell(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.m,
            vertical: AppSpacing.s,
          ),
          decoration: BoxDecoration(
            color: isHighlighted
                ? colorScheme.primary.withOpacity(0.08) // Highlight color
                : Colors.transparent,
            border: Border(
              bottom: BorderSide(
                color: colorScheme.secondary.withOpacity(0.08),
                width: 1.0,
              ),
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              // Código y Nombre
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      product.code,
                      style: AppTextStyles.badge.copyWith(
                        color: colorScheme.primary,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 2.0),
                    Text(
                      product.name,
                      style: AppTextStyles.contenidoTablaTexto.copyWith(
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),
              // Precio
              Text(
                'L ${product.price.toStringAsFixed(2)}',
                style: AppTextStyles.contenidoTablaNumero.copyWith(
                  fontWeight: FontWeight.bold,
                  color: colorScheme.primary,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
