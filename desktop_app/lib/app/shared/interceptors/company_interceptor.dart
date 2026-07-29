import 'package:dio/dio.dart';
import '../context/application_context.dart';

class CompanyInterceptor extends Interceptor {
  final ApplicationContext _context;

  CompanyInterceptor(this._context);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    // Dynamically inject the active company ID header from the application context.
    options.headers['X-Company-ID'] = _context.currentCompanyId;
    super.onRequest(options, handler);
  }
}
