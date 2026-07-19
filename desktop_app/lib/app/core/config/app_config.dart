import 'package:flutter_riverpod/flutter_riverpod.dart';

enum AppEnvironment {
  development,
  production,
}

class AppConfig {
  final AppEnvironment environment;
  final String apiBaseUrl;
  final bool enableDebugLogs;

  const AppConfig({
    required this.environment,
    required this.apiBaseUrl,
    required this.enableDebugLogs,
  });

  factory AppConfig.development() {
    return const AppConfig(
      environment: AppEnvironment.development,
      apiBaseUrl: 'http://localhost:8000',
      enableDebugLogs: true,
    );
  }

  factory AppConfig.production() {
    return const AppConfig(
      environment: AppEnvironment.production,
      apiBaseUrl: 'https://api.cajafacil.com',
      enableDebugLogs: false,
    );
  }

  // Backwards compatibility flag for legacy routing references
  static const bool developmentMode = true;
}

// Riverpod Provider for accessing environment configurations dynamically
final appConfigProvider = Provider<AppConfig>((ref) {
  return AppConfig.development();
});
