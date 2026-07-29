import '../dtos/product_search_dto.dart';
import '../../presentation/models/product_search_result.dart';

class ProductSearchMapper {
  /// Converts the network DTO into the decoupled presentation layer model.
  static ProductSearchResult toPresentation(ProductSearchDto dto) {
    return ProductSearchResult(
      id: dto.id,
      code: dto.code,
      name: dto.name,
      price: dto.price,
    );
  }
}
