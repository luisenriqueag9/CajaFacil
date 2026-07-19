class Formatters {
  /// Formats a double to currency representation
  static String formatCurrency(double value) {
    return '\$${value.toStringAsFixed(2)}';
  }

  /// Formats raw decimal string to standard representation
  static String formatDecimal(double value, {int decimalPlaces = 2}) {
    return value.toStringAsFixed(decimalPlaces);
  }
}
