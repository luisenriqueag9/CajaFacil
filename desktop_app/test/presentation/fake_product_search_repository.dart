import 'package:dio/dio.dart';
import 'package:caja_facil/app/modules/product/domain/repositories/product_search_repository.dart';
import 'package:caja_facil/app/modules/product/presentation/models/product_search_result.dart';

class FakeProductSearchRepository implements ProductSearchRepository {
  bool shouldThrowNetworkError = false;
  bool shouldTimeout = false;
  int searchCount = 0;
  Duration delay = Duration.zero;

  final List<ProductSearchResult> mockDatabase = const [
    ProductSearchResult(id: '1', code: '001', name: 'Coca Cola 355ml', price: 25.0),
    ProductSearchResult(id: '2', code: '002', name: 'Pan Blanco', price: 18.0),
    ProductSearchResult(id: '3', code: '003', name: 'Hielo Bolsa', price: 20.0),
    ProductSearchResult(id: '4', code: '004', name: 'Agua 600ml', price: 15.0),
    ProductSearchResult(id: '5', code: '005', name: 'Leche Entera 1L', price: 38.0),
  ];

  @override
  Future<List<ProductSearchResult>> search(String query, {CancelToken? cancelToken}) async {
    searchCount++;

    if (delay > Duration.zero) {
      await Future.delayed(delay);
    }

    if (cancelToken?.isCancelled ?? false) {
      throw DioException(
        requestOptions: RequestOptions(path: ''),
        type: DioExceptionType.cancel,
        message: 'Request cancelled',
      );
    }

    if (shouldThrowNetworkError) {
      throw DioException(
        requestOptions: RequestOptions(path: ''),
        type: DioExceptionType.connectionError,
        message: 'No internet connection',
      );
    }

    if (shouldTimeout) {
      throw DioException(
        requestOptions: RequestOptions(path: ''),
        type: DioExceptionType.connectionTimeout,
        message: 'Connection timed out',
      );
    }

    final cleanQuery = query.trim();
    if (cleanQuery.isEmpty) return [];

    return mockDatabase.where((product) {
      final codeMatch = product.code.startsWith(cleanQuery) || product.code == cleanQuery;
      final nameMatch = product.name.toLowerCase().contains(cleanQuery.toLowerCase());
      return codeMatch || nameMatch;
    }).toList();
  }
}
