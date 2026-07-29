class ProductSearchResult {
  /// Minimal UI projection representing a product search suggestion.
  /// Strictly decoupling the presentation layout from the raw domain entity (CF-ARCH-008).
  final String id;
  final String code;
  final String name;
  final double price;

  const ProductSearchResult({
    required this.id,
    required this.code,
    required this.name,
    required this.price,
  });

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is ProductSearchResult &&
          runtimeType == other.runtimeType &&
          id == other.id &&
          code == other.code &&
          name == other.name &&
          price == other.price;

  @override
  int get hashCode => id.hashCode ^ code.hashCode ^ name.hashCode ^ price.hashCode;

  @override
  String toString() => 'ProductSearchResult(id: $id, code: $code, name: $name, price: $price)';
}
