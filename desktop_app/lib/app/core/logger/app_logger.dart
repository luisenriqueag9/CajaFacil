import 'dart:developer' as developer;
import 'package:flutter/foundation.dart';

class AppLogger {
  static void debug(String message, {String? tag}) {
    _log('DEBUG', message, tag: tag);
  }

  static void info(String message, {String? tag}) {
    _log('INFO', message, tag: tag);
  }

  static void warning(String message, {String? tag}) {
    _log('WARNING', message, tag: tag);
  }

  static void error(String message, {String? tag, Object? error, StackTrace? stackTrace}) {
    if (kDebugMode) {
      developer.log(
        '[ERROR] ${tag != null ? '[$tag] ' : ''}$message',
        name: 'caja_facil',
        error: error,
        stackTrace: stackTrace,
        level: 1000,
      );
    }
  }

  static void _log(String level, String message, {String? tag}) {
    if (kDebugMode) {
      final String timestamp = DateTime.now().toIso8601String().split('T').last.substring(0, 8);
      developer.log(
        '[$timestamp] [$level] ${tag != null ? '[$tag] ' : ''}$message',
        name: 'caja_facil',
      );
    }
  }
}
