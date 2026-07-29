import 'package:flutter/material.dart';
import '../../../theme/app_spacing.dart';
import '../../../components/navigation/cf_top_bar.dart';
import 'product_search_area.dart';
import 'sale_grid_placeholder.dart';
import 'favorites_panel_placeholder.dart';
import 'totals_panel_placeholder.dart';
import 'quick_actions_bar.dart';

/// PosShell: Componente estructural permanente de la terminal del POS.
///
/// Propósito:
/// - Organizar el espacio físico de pantalla del cajero según CF-DOC-058.
/// - Implementar la proporción 70% izquierda para ventas y 30% derecha para complementos.
/// - Mantener el foco inicial en la barra de escaneo de productos.
class PosShell extends StatefulWidget {
  const PosShell({super.key});

  @override
  State<PosShell> createState() => _PosShellState();
}

class _PosShellState extends State<PosShell> {
  final FocusNode _searchFocusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    // Solicitar foco inicial de forma asíncrona para ProductSearchField
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _searchFocusNode.requestFocus();
    });
  }

  @override
  void dispose() {
    _searchFocusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // 1. Barra Superior Fija (Branding + Auditoría + Status Bar)
        const CFTopBar(
          userName: 'Cajero Demo',
          branchName: 'Sucursal Centro',
          posTerminalName: 'Caja 01',
          currentTime: '14:13',
          isOnline: true,
          isPrinterConnected: true,
          hasPendingSync: false,
        ),

        // 2. Área Central de Trabajo
        Expanded(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.m),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // A) Área de Búsqueda y Selección de Cliente
                ProductSearchArea(
                  focusNode: _searchFocusNode,
                ),
                const SizedBox(height: AppSpacing.m),

                // B) Bloque de Carrito (70%) y Favoritos (30%)
                Expanded(
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // SaleGrid (Carrito) - 70% del Ancho Horizontal
                      const Expanded(
                        flex: 7,
                        child: SaleGridPlaceholder(),
                      ),
                      const SizedBox(width: AppSpacing.m),
                      // FavoritesPanel (Botonera) - 30% del Ancho Horizontal
                      const Expanded(
                        flex: 3,
                        child: FavoritesPanelPlaceholder(),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: AppSpacing.m),

                // C) Bloque de Totales e Importes
                const TotalsPanelPlaceholder(),
              ],
            ),
          ),
        ),

        // 3. Barra de Atajos e Instrucciones de Teclado (Fija en Base)
        const QuickActionsBar(),
      ],
    );
  }
}
