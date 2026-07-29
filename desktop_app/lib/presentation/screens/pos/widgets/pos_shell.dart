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
import 'product_search_overlay.dart';
import 'edit_cart_item_dialog.dart';

/// PosShell: Componente estructural interactivo del POS con búsqueda inteligente.
///
/// Propósitos:
/// - Controlar la grilla de ventas, totales e interacción de búsqueda en tiempo real.
/// - Implementar atajos de teclado y navegación del panel flotante de autocompletado.
class PosShell extends StatefulWidget {
  const PosShell({super.key});

  @override
  State<PosShell> createState() => _PosShellState();
}

class _PosShellState extends State<PosShell> {
  final FocusNode _searchFocusNode = FocusNode();
  final TextEditingController _searchController = TextEditingController();

  // Estado del Carrito Local
  final List<CartItem> _cartItems = [];
  int? _selectedIndex;

  // Estado de Búsqueda Inteligente
  final List<MockProduct> _suggestions = [];
  int? _highlightedSuggestionIndex;

  @override
  void initState() {
    super.initState();
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

  // Filtrado de productos en tiempo real
  void _onSearchChanged(String query) {
    setState(() {
      _suggestions.clear();
      _highlightedSuggestionIndex = null;

      final cleanQuery = query.trim();
      if (cleanQuery.isNotEmpty) {
        // Filtrar productos según coincidencias (código, código parcial, o nombre)
        final matches = MockProductsCatalog.products.where((product) {
          final codeMatch = product.code.startsWith(cleanQuery) || product.code == cleanQuery;
          final nameMatch = product.name.toLowerCase().contains(cleanQuery.toLowerCase());
          return codeMatch || nameMatch;
        }).toList();

        _suggestions.addAll(matches);
      }
    });
  }

  // Agrega un producto por su código
  void _addProduct(String code) {
    final String cleanCode = code.trim();
    if (cleanCode.isEmpty) return;

    final product = MockProductsCatalog.findByCode(cleanCode);
    if (product == null) {
      CFToast.show(
        context,
        message: 'No se encontró el producto.',
        type: ToastType.error,
      );
    } else {
      setState(() {
        final existingIndex = _cartItems.indexWhere((item) => item.product.code == product.code);
        if (existingIndex != -1) {
          _cartItems[existingIndex].quantity += 1.0;
        } else {
          _cartItems.add(CartItem(product: product));
        }
        _selectedIndex = null;
        // Cerrar panel de sugerencias
        _suggestions.clear();
        _highlightedSuggestionIndex = null;
      });
    }

    _searchController.clear();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _requestFocus();
    });
  }

  // Navegación de sugerencias o del carrito de compras
  void _navigateSelection(int direction) {
    // Si el panel de autocompletado está abierto, navegar en sugerencias
    if (_suggestions.isNotEmpty) {
      setState(() {
        if (_highlightedSuggestionIndex == null) {
          _highlightedSuggestionIndex = direction > 0 ? 0 : _suggestions.length - 1;
        } else {
          _highlightedSuggestionIndex = (_highlightedSuggestionIndex! + direction + _suggestions.length) % _suggestions.length;
        }
      });
      return;
    }

    // Si el panel está cerrado, navegar en el carrito
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

  // Abre el diálogo para editar la línea del carrito
  void _editCartItem(int index) async {
    if (index < 0 || index >= _cartItems.length) return;

    final currentItem = _cartItems[index];
    final updatedItem = await showDialog<CartItem>(
      context: context,
      barrierDismissible: false,
      builder: (context) => EditCartItemDialog(item: currentItem),
    );

    if (updatedItem != null) {
      setState(() {
        _cartItems[index] = updatedItem;
        _selectedIndex = index;
      });
    }
    _requestFocus();
  }

  // Elimina la fila del carrito seleccionada
  void _deleteSelectedRow() {
    if (_selectedIndex != null && _selectedIndex! >= 0 && _selectedIndex! < _cartItems.length) {
      setState(() {
        _cartItems.removeAt(_selectedIndex!);
        _selectedIndex = null;
      });
      _requestFocus();
    }
  }

  // Cancela selección o cierra sugerencias
  void _cancelSelection() {
    setState(() {
      if (_suggestions.isNotEmpty) {
        _suggestions.clear();
        _highlightedSuggestionIndex = null;
      } else {
        _selectedIndex = null;
      }
    });
    _requestFocus();
  }

  // Manejo de la tecla ENTER
  void _handleEnterKey() {
    final query = _searchController.text;
    if (_suggestions.isNotEmpty && _highlightedSuggestionIndex != null) {
      // Agregar sugerencia resaltada
      _addProduct(_suggestions[_highlightedSuggestionIndex!].code);
    } else if (query.trim().isEmpty && _selectedIndex != null) {
      // Abrir edición si la búsqueda está vacía y hay una fila seleccionada
      _editCartItem(_selectedIndex!);
    } else {
      // Comportamiento por defecto
      _addProduct(query);
    }
  }

  @override
  Widget build(BuildContext context) {
    final subtotal = _cartItems.fold<double>(0.0, (sum, item) => sum + item.subtotal);
    final discount = _cartItems.fold<double>(0.0, (sum, item) => sum + item.discount);
    final tax = subtotal * 0.15;
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
          } else if (key == LogicalKeyboardKey.enter || key == LogicalKeyboardKey.numpadEnter) {
            _handleEnterKey();
            return KeyEventResult.handled;
          } else if (key == LogicalKeyboardKey.f4) {
            if (_selectedIndex != null) {
              _editCartItem(_selectedIndex!);
            }
            return KeyEventResult.handled;
          }
        }
        return KeyEventResult.ignored;
      },
      child: Column(
        children: [
          const CFTopBar(
            userName: 'Cajero Demo',
            branchName: 'Sucursal Centro',
            posTerminalName: 'Caja 01',
            currentTime: '10:43',
            isOnline: true,
            isPrinterConnected: true,
            hasPendingSync: false,
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.m),
              child: Stack(
                clipBehavior: Clip.none,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // A) Entrada y Foco
                      ProductSearchArea(
                        focusNode: _searchFocusNode,
                        controller: _searchController,
                        onSubmitted: _addProduct,
                        onChanged: _onSearchChanged,
                        onClear: () {
                          setState(() {
                            _searchController.clear();
                            _suggestions.clear();
                            _highlightedSuggestionIndex = null;
                          });
                          _requestFocus();
                        },
                      ),
                      const SizedBox(height: AppSpacing.m),
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
                                onRowDoubleTap: _editCartItem,
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
                  // B) Sugerencias Flotantes de autocompletado (dentro de los límites del Stack)
                  if (_suggestions.isNotEmpty)
                    Positioned(
                      top: 78.0,
                      left: 0,
                      right: 0,
                      child: ProductSearchOverlay(
                        suggestions: _suggestions,
                        highlightedIndex: _highlightedSuggestionIndex,
                        onSuggestionSelected: (product) => _addProduct(product.code),
                      ),
                    ),
                ],
              ),
            ),
          ),
          const QuickActionsBar(),
        ],
      ),
    );
  }
}
