import 'package:dio/dio.dart';
import '../../modules/product/data/repositories/http_product_search_repository.dart';
import '../../modules/product/domain/repositories/product_search_repository.dart';
import '../../modules/product/presentation/models/product_search_result.dart';
import '../../shared/cache/memory_cache.dart';
import '../../shared/context/application_context.dart';
import '../../shared/interceptors/company_interceptor.dart';
import '../config/app_config.dart';

class DependencyContainer {
  /// Central bootstrap Composition Root managing dependency lifecycles (CF-ARCH-007).
  static late final ApplicationContext applicationContext;
  static late final Dio dio;
  static late final MemoryCache<String, List<ProductSearchResult>> searchCache;
  static late final ProductSearchRepository productSearchRepository;

  static void initialize() {
    applicationContext = const ApplicationContext();

    dio = Dio(BaseOptions(
      baseUrl: AppConfig.development().apiBaseUrl,
      connectTimeout: const Duration(seconds: 5),
      receiveTimeout: const Duration(seconds: 5),
    ));

    dio.interceptors.add(CompanyInterceptor(applicationContext));

    searchCache = MemoryCache<String, List<ProductSearchResult>>(
      ttl: const Duration(minutes: 5),
    );

    productSearchRepository = HttpProductSearchRepository(dio, searchCache);
  }
}
