import 'package:flutter_riverpod/flutter_riverpod.dart';

abstract class LocalDatabase {
  Future<void> initialize();
  Future<void> close();
  Future<bool> isOpen();
}

class SQLiteLocalDatabase implements LocalDatabase {
  bool _initialized = false;

  @override
  Future<void> initialize() async {
    // Standard SQLite initialization on Windows Desktop:
    // 1. Get Application Documents Directory
    // 2. Open or create database file using sqlite3 (or drift/sqflite_common_ffi)
    // 3. Enable foreign keys: pragma foreign_keys = ON;
    _initialized = true;
  }

  @override
  Future<void> close() async {
    _initialized = false;
  }

  @override
  Future<bool> isOpen() async {
    return _initialized;
  }
}

// Riverpod Provider for local database instance
final localDatabaseProvider = Provider<LocalDatabase>((ref) {
  final db = SQLiteLocalDatabase();
  // Automatically initialize database or defer to app startup lifespan
  return db;
});
