import 'package:flutter/material.dart';
import '../../../theme/app_spacing.dart';
import '../../../components/layout/cf_panel.dart';
import '../../../components/buttons/cf_button.dart';

/// FavoritesPanelPlaceholder: Botonera lateral del POS para inserción rápida.
class FavoritesPanelPlaceholder extends StatelessWidget {
  const FavoritesPanelPlaceholder({
    super.key,
    required this.onAddProduct,
  });

  final ValueChanged<String> onAddProduct;

  @override
  Widget build(BuildContext context) {
    // Mapeo oficial de favoritos rápidos a sus códigos mock
    final List<Map<String, String>> simulatedFavorites = [
      {'name': 'Coca Cola', 'code': '001'},
      {'name': 'Pan Blanco', 'code': '002'},
      {'name': 'Hielo Bolsa', 'code': '003'},
      {'name': 'Agua 600ml', 'code': '004'},
      {'name': 'Leche Entera', 'code': '005'},
    ];

    return CFPanel(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text(
            'FAVORITOS / RÁPIDO',
            style: TextStyle(
              fontSize: 12.0,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.0,
            ),
          ),
          const SizedBox(height: AppSpacing.s),
          Expanded(
            child: GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: AppSpacing.s,
                mainAxisSpacing: AppSpacing.s,
                childAspectRatio: 1.4,
              ),
              itemCount: simulatedFavorites.length,
              itemBuilder: (context, index) {
                final favorite = simulatedFavorites[index];
                return CFButton(
                  label: favorite['name']!,
                  variant: ButtonVariant.secondary,
                  onPressed: () => onAddProduct(favorite['code']!),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
