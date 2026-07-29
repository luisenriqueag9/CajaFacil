import 'package:flutter/material.dart';
import '../../../theme/app_spacing.dart';
import '../../../components/layout/cf_panel.dart';
import '../../../components/buttons/cf_button.dart';

/// FavoritesPanelPlaceholder: Botonera lateral derecha del POS (30% de ancho).
///
/// Propósito:
/// - Mostrar los botones rápidos de acceso a productos de alta rotación.
class FavoritesPanelPlaceholder extends StatelessWidget {
  const FavoritesPanelPlaceholder({super.key});

  @override
  Widget build(BuildContext context) {
    // Lista de botones rápidos simulados para mostrador
    final List<String> simulatedFavorites = [
      'Hielo Bolsa',
      'Pan Blanco',
      'Recarga L 50',
      'Bolsa Kraft',
      'Leche Deslact.',
      'Refresco 3L',
      'Servilletas',
      'Agua Purificada',
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
                return CFButton(
                  label: simulatedFavorites[index],
                  variant: ButtonVariant.secondary,
                  onPressed: () {
                    // Simular inserción inactiva en este sprint
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
