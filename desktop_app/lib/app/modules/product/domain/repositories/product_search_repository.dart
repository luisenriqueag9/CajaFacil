import 'package:dio/dio.dart';
import '../../presentation/models/product_search_result.dart';

abstract class ProductSearchRepository {
  /// Searches active catalog products matching the query term (barcode, internal code, or name).
  /// Exposes standard presentation projection models to the UI.
  Future<List<ProductSearchResult>> search(String query, {CancelToken? cancelToken});
}
