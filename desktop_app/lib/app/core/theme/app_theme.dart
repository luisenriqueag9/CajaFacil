import 'package:flutter/material.dart';

class AppTheme {
  // Elegant SaaS Dark Mode Color Palette
  static const Color darkBackground = Color(0xFF0F0F12);
  static const Color darkSurface = Color(0xFF16161F);
  static const Color darkCard = Color(0xFF1E1E2C);
  
  // Vibrant accents
  static const Color primaryAccent = Color(0xFF6366F1);   // Modern Indigo
  static const Color secondaryAccent = Color(0xFF10B981); // Emerald Green
  static const Color warningAccent = Color(0xFFF59E0B);   // Warm Amber
  static const Color dangerAccent = Color(0xFFEF4444);    // Coral Red
  
  // Neutral colors
  static const Color textPrimaryDark = Color(0xFFF3F4F6);
  static const Color textSecondaryDark = Color(0xFF9CA3AF);

  // Light Mode Palette
  static const Color lightBackground = Color(0xFFF9FAFB);
  static const Color lightSurface = Color(0xFFFFFFFF);
  static const Color textPrimaryLight = Color(0xFF111827);
  static const Color textSecondaryLight = Color(0xFF6B7280);

  /// Dark Theme Definition
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: darkBackground,
      colorScheme: const ColorScheme.dark(
        primary: primaryAccent,
        secondary: secondaryAccent,
        surface: darkSurface,
        error: dangerAccent,
      ),
      cardTheme: const CardThemeData(
        color: darkCard,
        elevation: 2,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(16)),
        ),
      ),
      textTheme: const TextTheme(
        headlineLarge: TextStyle(color: textPrimaryDark, fontSize: 32, fontWeight: FontWeight.bold, letterSpacing: -0.5),
        headlineMedium: TextStyle(color: textPrimaryDark, fontSize: 24, fontWeight: FontWeight.w600, letterSpacing: -0.5),
        titleLarge: TextStyle(color: textPrimaryDark, fontSize: 20, fontWeight: FontWeight.w600),
        bodyLarge: TextStyle(color: textPrimaryDark, fontSize: 16, height: 1.5),
        bodyMedium: TextStyle(color: textSecondaryDark, fontSize: 14, height: 1.5),
      ),
      dividerTheme: const DividerThemeData(
        color: Color(0xFF2E2E3E),
        thickness: 1,
      ),
    );
  }

  /// Light Theme Definition
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: lightBackground,
      colorScheme: const ColorScheme.light(
        primary: primaryAccent,
        secondary: secondaryAccent,
        surface: lightSurface,
        error: dangerAccent,
      ),
      cardTheme: const CardThemeData(
        color: lightSurface,
        elevation: 1,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(16)),
        ),
      ),
      textTheme: const TextTheme(
        headlineLarge: TextStyle(color: textPrimaryLight, fontSize: 32, fontWeight: FontWeight.bold, letterSpacing: -0.5),
        headlineMedium: TextStyle(color: textPrimaryLight, fontSize: 24, fontWeight: FontWeight.w600, letterSpacing: -0.5),
        titleLarge: TextStyle(color: textPrimaryLight, fontSize: 20, fontWeight: FontWeight.w600),
        bodyLarge: TextStyle(color: textPrimaryLight, fontSize: 16, height: 1.5),
        bodyMedium: TextStyle(color: textSecondaryLight, fontSize: 14, height: 1.5),
      ),
    );
  }

}
