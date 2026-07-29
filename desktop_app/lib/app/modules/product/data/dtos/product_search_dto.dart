class ProductSearchDto {
  /// Data Transfer Object representing the deserialized backend payload.
  final String id;
  final String code;
  final String name;
  final double price;

  const ProductSearchDto({
    required this.id,
    required this.code,
    required this.name,
    required this.price,
  });

  factory ProductSearchDto.fromJson(Map<String, dynamic> json) {
    return ProductSearchDto(
      id: json['id'] as String,
      code: json['code'] as String,
      name: json['name'] as String,
      price: (json['price'] as num).toDouble(),
    );
  }
}
