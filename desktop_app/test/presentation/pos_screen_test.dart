import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:caja_facil/presentation/screens/pos/pos_screen.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/pos_shell.dart';
import 'package:caja_facil/presentation/components/inputs/cf_search_field.dart';

void main() {
  group('Widget Tests - POS Base Shell (Sprint 40)', () {
    testWidgets('PosScreen renders correctly and shows all basic placeholders', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      // 1. Verificar la renderización del Shell principal
      expect(find.byType(PosShell), findsOneWidget);

      // 2. Verificar la presencia de los placeholders obligatorios en la cabecera
      expect(find.textContaining('Cajero: Cajero Demo'), findsOneWidget);
      expect(find.textContaining('Sucursal: Sucursal Centro'), findsOneWidget);
      expect(find.textContaining('Terminal: Caja 01'), findsOneWidget);

      // 3. Verificar los placeholders de Totales e Importes
      expect(find.text('TOTAL A PAGAR:'), findsOneWidget);
      expect(find.text('L 0.00'), findsNWidgets(4));
      expect(find.text('SUBTOTAL:'), findsOneWidget);
      expect(find.text('ISV (15%):'), findsOneWidget);
      expect(find.text('DESCUENTOS:'), findsOneWidget);

      // 4. Verificar la presencia de la grilla vacía
      expect(find.text('Carrito de Ventas Vacío'), findsOneWidget);
      expect(find.text('Líneas: 0'), findsOneWidget);
      expect(find.text('Unidades: 0.00'), findsOneWidget);

      // 5. Verificar los botones de favoritos
      expect(find.text('FAVORITOS / RÁPIDO'), findsOneWidget);
      expect(find.text('Hielo Bolsa'), findsOneWidget);
      expect(find.text('Pan Blanco'), findsOneWidget);

      // 6. Verificar la barra de atajos inferior
      expect(find.text('F2'), findsOneWidget);
      expect(find.text('F12'), findsOneWidget);
      expect(find.text('Cobrar'), findsOneWidget);
    });

    testWidgets('ProductSearchField has initial autofocus', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Scaffold(
              body: const PosScreen(),
            ),
          ),
        ),
      );

      // Dejar que se procese el frame y el Callback de post-frame
      await tester.pump();

      // Encontrar el TextField del buscador de productos
      final searchFieldFinder = find.byType(CFSearchField);
      expect(searchFieldFinder, findsOneWidget);

      final TextField textFieldWidget = tester.widget<TextField>(
        find.descendant(
          of: searchFieldFinder,
          matching: find.byType(TextField),
        ),
      );

      // Verificar que tiene asignado un FocusNode y que está enfocado
      expect(textFieldWidget.focusNode?.hasFocus, isTrue);
    });
  });
}
