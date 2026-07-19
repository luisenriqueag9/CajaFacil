import 'package:flutter/material.dart';

extension BuildContextExtensions on BuildContext {
  /// Quick shortcut to access the current ThemeData
  ThemeData get theme => Theme.of(this);

  /// Quick shortcut to access the current TextTheme
  TextTheme get textTheme => theme.textTheme;

  /// Quick shortcut to access the current ColorScheme
  ColorScheme get colorScheme => theme.colorScheme;

  /// Utility to check if system or theme is currently in dark mode
  bool get isDarkMode => theme.brightness == Brightness.dark;

  /// Short-hand to access media query size
  Size get screenSize => MediaQuery.sizeOf(this);
}
