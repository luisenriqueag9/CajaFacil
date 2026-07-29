import 'package:dio/dio.dart';
import '../../../../shared/cache/memory_cache.dart';
import '../../domain/repositories/product_search_repository.dart';
import '../../presentation/models/product_search_result.dart';
import '../dtos/product_search_dto.dart';
import '../mappers/product_search_mapper.dart';

class HttpProductSearchRepository implements ProductSearchRepository {
  final Dio _dio;
  final MemoryCache<String, List<ProductSearchResult>> _cache;

  HttpProductSearchRepository(this._dio, this._cache);

  @override
  Future<List<ProductSearchResult>> search(String query, {CancelToken? cancelToken}) async {
    final cleanQuery = query.trim();

    // Check memory cache HIT
    final cached = _cache.get(cleanQuery);
    if (cached != null) {
      return cached;
    }

    try {
      final response = await _dio.get(
        '/api/v1/pos/search-products',
        queryParameters: {'search': cleanQuery},
        cancelToken: cancelToken,
      );

      if (response.data != null && response.data['success'] == true) {
        final List<dynamic> dataList = response.data['data'] as List<dynamic>;
        final results = dataList
            .map((json) => ProductSearchMapper.toPresentation(
                  ProductSearchDto.fromJson(json as Map<String, dynamic>),
                ))
            .toList();

        // Save in cache (Cache MISS flow complete)
        _cache.set(cleanQuery, results);
        return results;
      }

      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
        message: response.data?['message'] ?? 'Error desconocido en el servidor.',
      );
    } on DioException catch (e) {
      if (e.type == DioExceptionType.cancel) {
        rethrow;
      }
      rethrow;
    }
  }
}
