import 'package:flutter/material.dart';

abstract final class AppShadows {
  static const List<BoxShadow> small = [
    BoxShadow(
      color: Color(0x140F172A),
      blurRadius: 8,
      offset: Offset(0, 2),
    ),
  ];

  static const List<BoxShadow> medium = [
    BoxShadow(
      color: Color(0x1A0F172A),
      blurRadius: 16,
      offset: Offset(0, 6),
    ),
  ];

  static const List<BoxShadow> large = [
    BoxShadow(
      color: Color(0x240F172A),
      blurRadius: 28,
      offset: Offset(0, 12),
    ),
  ];
}