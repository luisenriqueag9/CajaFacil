import 'package:flutter/material.dart';
import 'app_colors.dart';

/// Escala oficial de estilos tipográficos según CF-DOC-056.
/// Implementa Inter para texto y fuentes monospace para números.
abstract final class AppTextStyles {
  // Estilo Base de Fuente
  static const String fontFamilyBase = 'Inter';
  static const String fontFamilyNumeric = 'monospace';

  // 1. Título Gigante (Total)
  static const TextStyle titleGigante = TextStyle(
    fontFamily: fontFamilyNumeric,
    fontSize: 32.0,
    fontWeight: FontWeight.w700, // Bold
    height: 1.2,
    color: AppColors.textPrimary,
  );

  // 2. Título Principal (Sección)
  static const TextStyle titlePrincipal = TextStyle(
    fontFamily: fontFamilyBase,
    fontSize: 20.0,
    fontWeight: FontWeight.w600, // SemiBold
    height: 1.3,
    color: AppColors.textPrimary,
  );

  // 3. Cabecera de Tabla
  static const TextStyle cabeceraTabla = TextStyle(
    fontFamily: fontFamilyBase,
    fontSize: 12.0,
    fontWeight: FontWeight.w500, // Medium
    height: 1.4,
    color: AppColors.textSecondary,
  );

  // 4. Contenido de Tabla (Texto)
  static const TextStyle contenidoTablaTexto = TextStyle(
    fontFamily: fontFamilyBase,
    fontSize: 14.0,
    fontWeight: FontWeight.w400, // Regular
    height: 1.4,
    color: AppColors.textPrimary,
  );

  // 5. Contenido de Tabla (Número)
  static const TextStyle contenidoTablaNumero = TextStyle(
    fontFamily: fontFamilyNumeric,
    fontSize: 14.0,
    fontWeight: FontWeight.w400, // Regular
    height: 1.4,
    color: AppColors.textPrimary,
  );

  // 6. Etiqueta de Botón
  static const TextStyle etiquetaBoton = TextStyle(
    fontFamily: fontFamilyBase,
    fontSize: 14.0,
    fontWeight: FontWeight.w600, // SemiBold
    height: 1.2,
  );

  // 7. Texto de Toast / Notificación
  static const TextStyle textoToast = TextStyle(
    fontFamily: fontFamilyBase,
    fontSize: 12.0,
    fontWeight: FontWeight.w400, // Regular
    height: 1.3,
    color: Colors.white,
  );

  // 8. Badge / Indicador
  static const TextStyle badge = TextStyle(
    fontFamily: fontFamilyBase,
    fontSize: 10.0,
    fontWeight: FontWeight.w700, // Bold
    height: 1.1,
  );
}
