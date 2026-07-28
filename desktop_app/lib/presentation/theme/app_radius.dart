import 'package:flutter/material.dart';

/// Escala oficial de radios de borde según CF-DOC-056.
abstract final class AppRadius {
  static const double s = 4.0;  // Radio pequeño: Botones e inputs
  static const double m = 8.0;  // Radio mediano: Tarjetas, diálogos

  static const BorderRadius borderS = BorderRadius.all(Radius.circular(s));
  static const BorderRadius borderM = BorderRadius.all(Radius.circular(m));
}
