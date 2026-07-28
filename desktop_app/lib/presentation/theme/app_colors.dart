import 'package:flutter/material.dart';

/// Paleta de colores oficial de CajaFácil según CF-DOC-056.
/// Todos los componentes deben consumir estos colores a través de ThemeData
/// o de constantes estáticas referenciando esta clase.
abstract final class AppColors {
  // Colores principales de la marca (Slate Palette)
  static const Color primary = Color(0xFF1E293B);    // Gris Slate Profundo
  static const Color secondary = Color(0xFF475569);  // Gris Slate Medio
  static const Color accent = Color(0xFF3B82F6);     // Azul Acento (Foco/CTA)

  // Colores de estado semánticos
  static const Color success = Color(0xFF10B981);    // Verde Éxito
  static const Color error = Color(0xFFEF4444);      // Rojo Error
  static const Color warning = Color(0xFFF59E0B);    // Ámbar Advertencia
  static const Color info = Color(0xFF06B6D4);       // Cian Información

  // Fondos y bordes
  static const Color backgroundLight = Color(0xFFF8FAFC); // Gris Claro Fondo
  static const Color backgroundDark = Color(0xFF0F172A);  // Gris Muy Oscuro
  static const Color surface = Color(0xFFFFFFFF);         // Blanco Puro Tarjeta
  static const Color surfaceDark = Color(0xFF1E293B);     // Gris Slate Tarjeta
  static const Color border = Color(0xFFE2E8F0);          // Divisores y Bordes
  static const Color borderDark = Color(0xFF334155);      // Bordes Tema Oscuro

  // Textos
  static const Color textPrimary = Color(0xFF1E293B);     // Texto Oscuro Principal
  static const Color textPrimaryDark = Color(0xFFF1F5F9); // Texto Claro Principal
  static const Color textSecondary = Color(0xFF64748B);   // Texto Gris
  static const Color textSecondaryDark = Color(0xFF94A3B8); // Texto Gris Claro
}
