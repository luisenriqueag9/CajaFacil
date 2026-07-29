/// MockProduct: Modelo de producto simulado para la fase de prototipado.
class MockProduct {
  const MockProduct({
    required this.code,
    required this.name,
    required this.price,
  });

  final String code;
  final String name;
  final double price;
}

/// Catálogo de productos simulado oficial de CajaFácil para el Sprint 41.
/// Este catálogo es temporal y está completamente aislado de la capa de datos o negocio.
abstract final class MockProductsCatalog {
  static const List<MockProduct> products = [
    MockProduct(code: '001', name: 'Coca Cola 355ml', price: 25.0),
    MockProduct(code: '002', name: 'Pan Blanco', price: 18.0),
    MockProduct(code: '003', name: 'Hielo Bolsa', price: 20.0),
    MockProduct(code: '004', name: 'Agua 600ml', price: 15.0),
    MockProduct(code: '005', name: 'Leche Entera 1L', price: 38.0),
  ];

  /// Busca un producto por su código de barra en el catálogo mock.
  static MockProduct? findByCode(String code) {
    for (final product in products) {
      if (product.code == code) {
        return product;
      }
    }
    return null;
  }

  /// Busca un producto por su nombre en el catálogo mock.
  static MockProduct? findByName(String name) {
    for (final product in products) {
      if (product.name.toLowerCase() == name.toLowerCase()) {
        return product;
      }
    }
    return null;
  }
}
