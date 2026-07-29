import 'package:flutter/material.dart';
import 'widgets/pos_shell.dart';

/// PosScreen: Pantalla principal que sirve como punto de entrada para la terminal del POS.
///
/// Propósito:
/// - Inicializar y estructurar la interfaz del mostrador.
/// - Asegurar el foco por defecto y la captura de teclado.
class PosScreen extends StatelessWidget {
  const PosScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: FocusScope(
        autofocus: true,
        child: PosShell(),
      ),
    );
  }
}
