import '../../../mock/mock_products.dart';

/// CartItem: Modelo de línea del carrito de compras para el POS.
class CartItem {
  CartItem({
    required this.product,
    this.quantity = 1.0,
    this.discount = 0.0,
    this.observation = '',
  });

  final MockProduct product;
  double quantity;
  double discount;
  String observation;

  double get subtotal => product.price * quantity;
  double get total => subtotal - discount;
}
