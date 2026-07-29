class _CacheEntry<V> {
  final V value;
  final DateTime expiresAt;

  _CacheEntry(this.value, this.expiresAt);

  bool get isExpired => DateTime.now().isAfter(expiresAt);
}

class MemoryCache<K, V> {
  final Duration ttl;
  final Map<K, _CacheEntry<V>> _cache = {};

  MemoryCache({required this.ttl});

  /// Stores a value in the cache with the configured TTL expiration timestamp.
  void set(K key, V value) {
    _cache[key] = _CacheEntry<V>(value, DateTime.now().add(ttl));
  }

  /// Retrieves a value from cache if it exists and has not expired yet.
  /// Evicts the entry automatically if it has expired.
  V? get(K key) {
    final entry = _cache[key];
    if (entry == null) return null;
    if (entry.isExpired) {
      _cache.remove(key);
      return null;
    }
    return entry.value;
  }

  /// Invalidates a specific cache key manually.
  void invalidate(K key) {
    _cache.remove(key);
  }

  /// Clears the entire cache.
  void clear() {
    _cache.clear();
  }
  
  /// Helper exposing active entries count (useful for tests).
  int get activeEntriesCount {
    // Evict any expired entries first before returning count
    final keys = List<K>.from(_cache.keys);
    for (final key in keys) {
      get(key); 
    }
    return _cache.length;
  }
}
