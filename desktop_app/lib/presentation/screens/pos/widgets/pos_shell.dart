import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../theme/app_spacing.dart';
import '../../../mock/mock_products.dart';
import '../../../components/navigation/cf_top_bar.dart';
import '../../../components/feedback/cf_toast.dart';
import 'cart_item.dart';
import 'product_search_area.dart';
import 'sale_grid_placeholder.dart';
import 'favorites_panel_placeholder.dart';
import 'totals_panel_placeholder.dart';
import 'quick_actions_bar.dart';

/// PosShell: Componente estructural interactivo de la terminal del POS.
///
/// Propósitos:
/// - Organizar el espacio del cajero y gestionar el estado local del carrito.
/// - Implementar atajos de teclado globales (Arrow Up/Down, DEL, ESC) y autofocus.
class PosShell extends StatefulWidget {
  const PosShell({super.key});

  @override
  State<PosShell> createState() => _PosShellState();
}

class _PosShellState extends State<PosShell> {
  final FocusNode _searchFocusNode = FocusNode();
  final TextEditingController _searchController = TextEditingController();

  // Estado del Carrito Local (Prototipo Frontend)
  final List<CartItem> _cartItems = [];
  int? _selectedIndex;

  @override
  void initState() {
    super.initState();
    // Solicitar foco inicial tras el renderizado
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _requestFocus();
    });
  }

  @override
  void dispose() {
    _searchFocusNode.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _requestFocus() {
    _searchFocusNode.requestFocus();
  }

  // Agrega un producto por su código
  void _addProduct(String code) {
    final String cleanCode = code.trim();
    if (cleanCode.isEmpty) return;

    final product = MockProductsCatalog.findByCode(cleanCode);
    if (product == null) {
      // Toast de error de producto no encontrado
      CFToast.show(
        context,
        message: 'No se encontró el producto.',
        type: ToastType.error,
      );
    } else {
      setState(() {
        // Verificar si el producto ya está en el carrito
        final existingIndex = _cartItems.indexWhere((item) => item.product.code == product.code);
        if (existingIndex != -1) {
          _cartItems[existingIndex].quantity += 1.0;
        } else {
          _cartItems.add(CartItem(product: product));
        }
        // Deseleccionar cualquier fila activa al agregar un nuevo item
        _selectedIndex = null;
      });
    }

    // Limpiar input y recuperar foco al final del frame para prevalecer sobre cierres
    _searchController.clear();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _requestFocus();
    });
  }

  // Navegación mediante teclas de flecha
  void _navigateSelection(int direction) {
    if (_cartItems.isEmpty) return;

    setState(() {
      if (_selectedIndex == null) {
        _selectedIndex = direction > 0 ? 0 : _cartItems.length - 1;
      } else {
        final newIndex = _selectedIndex! + direction;
        if (newIndex >= 0 && newIndex < _cartItems.length) {
          _selectedIndex = newIndex;
        }
      }
    });
  }

  // Elimina la fila seleccionada
  void _deleteSelectedRow() {
    if (_selectedIndex != null && _selectedIndex! >= 0 && _selectedIndex! < _cartItems.length) {
      setState(() {
        _cartItems.removeAt(_selectedIndex!);
        _selectedIndex = null;
      });
      _requestFocus();
    }
  }

  // Cancela la selección actual y devuelve el foco
  void _cancelSelection() {
    setState(() {
      _selectedIndex = null;
    });
    _requestFocus();
  }

  @override
  Widget build(BuildContext context) {
    // Cálculos acumulativos del mostrador
    final subtotal = _cartItems.fold<double>(0.0, (sum, item) => sum + item.subtotal);
    final discount = _cartItems.fold<double>(0.0, (sum, item) => sum + item.discount);
    final tax = subtotal * 0.15; // 15% ISV simulado
    final total = subtotal + tax - discount;

    return Focus(
      autofocus: true,
      onKeyEvent: (node, event) {
        if (event is KeyDownEvent) {
          final key = event.logicalKey;
          if (key == LogicalKeyboardKey.arrowDown) {
            _navigateSelection(1);
            return KeyEventResult.handled;
          } else if (key == LogicalKeyboardKey.arrowUp) {
            _navigateSelection(-1);
            return KeyEventResult.handled;
          } else if (key == LogicalKeyboardKey.delete) {
            _deleteSelectedRow();
            return KeyEventResult.handled;
          } else if (key == LogicalKeyboardKey.escape) {
            _cancelSelection();
            return KeyEventResult.handled;
          }
        }
        return KeyEventResult.ignored;
      },
      child: Column(
        children: [
          // 1. Cabecera Contextual Fija
          CFTopBar(
            userName: 'Cajero Demo',
            branchName: 'Sucursal Centro',
            posTerminalName: 'Caja 01',
            currentTime: '10:35',
            isOnline: true,
            isPrinterConnected: true,
            hasPendingSync: false,
          ),

          // 2. Campo Central de Trabajo
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.m),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // A) Entrada y Foco
                  ProductSearchArea(
                    focusNode: _searchFocusNode,
                    controller: _searchController,
                    onSubmitted: _addProduct,
                    onClear: () {
                      _searchController.clear();
                      _requestFocus();
                    },
                  ),
                  const SizedBox(height: AppSpacing.m),

                  // B) Grilla de Venta y Botonera
                  Expanded(
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // SaleGrid - 70% Ancho
                        Expanded(
                          flex: 7,
                          child: SaleGridPlaceholder(
                            cartItems: _cartItems,
                            selectedIndex: _selectedIndex,
                            onRowSelected: (index) {
                              setState(() {
                                _selectedIndex = index;
                              });
                            },
                          ),
                        ),
                        const SizedBox(width: AppSpacing.m),
                        // FavoritesPanel - 30% Ancho
                        Expanded(
                          flex: 3,
                          child: FavoritesPanelPlaceholder(
                            onAddProduct: _addProduct,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.m),

                  // C) Desglose de Importes y Checkout
                  TotalsPanelPlaceholder(
                    subtotal: subtotal,
                    tax: tax,
                    discount: discount,
                    total: total,
                    onCheckout: () {
                      if (_cartItems.isEmpty) {
                        CFToast.show(
                          context,
                          message: 'El carrito está vacío.',
                          type: ToastType.warning,
                        );
                        return;
                      }
                      CFToast.show(
                        context,
                        message: 'Checkout simulado: L ${total.toStringAsFixed(2)}',
                        type: ToastType.success,
                      );
                    },
                  ),
                ],
              ),
            ),
          ),

          // 3. Barra de Atajos de Teclado
          const QuickActionsBar(),
        ],
      ),
    );
  }
}
