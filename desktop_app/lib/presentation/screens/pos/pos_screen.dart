import 'package:flutter/material.dart';
import '../../../app/modules/product/domain/repositories/product_search_repository.dart';
import 'widgets/pos_shell.dart';

/// PosScreen: Pantalla principal que sirve como punto de entrada para la terminal del POS.
///
/// Propósito:
/// - Inicializar y estructurar la interfaz del mostrador.
/// - Asegurar el foco por defecto y la captura de teclado.
class PosScreen extends StatelessWidget {
  final ProductSearchRepository productSearchRepository;

  const PosScreen({
    super.key,
    required this.productSearchRepository,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FocusScope(
        autofocus: true,
        child: PosShell(
          productSearchRepository: productSearchRepository,
        ),
      ),
    );
  }
}
