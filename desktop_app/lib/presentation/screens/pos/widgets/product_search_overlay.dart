import 'package:flutter/material.dart';
import '../../../theme/app_radius.dart';
import '../../../mock/mock_products.dart';
import 'search_result_tile.dart';

/// ProductSearchOverlay: Panel flotante de autocompletado del POS.
///
/// Propósito:
/// - Mostrar la lista de sugerencias filtradas sin bloquear la grilla de ventas.
class ProductSearchOverlay extends StatelessWidget {
  const ProductSearchOverlay({
    super.key,
    required this.suggestions,
    required this.highlightedIndex,
    required this.onSuggestionSelected,
  });

  final List<MockProduct> suggestions;
  final int? highlightedIndex;
  final ValueChanged<MockProduct> onSuggestionSelected;

  @override
  Widget build(BuildContext context) {
    if (suggestions.isEmpty) return const SizedBox.shrink();

    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      constraints: const BoxConstraints(maxHeight: 250.0),
      decoration: BoxDecoration(
        color: colorScheme.surface,
        borderRadius: AppRadius.borderM,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.12),
            blurRadius: 8.0,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(
          color: colorScheme.secondary.withOpacity(0.15),
          width: 1.0,
        ),
      ),
      child: ClipRRect(
        borderRadius: AppRadius.borderM,
        child: ListView.builder(
          shrinkWrap: true,
          padding: EdgeInsets.zero,
          itemCount: suggestions.length,
          itemBuilder: (context, index) {
            final product = suggestions[index];
            return SearchResultTile(
              product: product,
              isHighlighted: index == highlightedIndex,
              onTap: () => onSuggestionSelected(product),
            );
          },
        ),
      ),
    );
  }
}
