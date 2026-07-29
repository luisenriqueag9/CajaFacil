import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:caja_facil/presentation/screens/pos/pos_screen.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/pos_shell.dart';
import 'package:caja_facil/presentation/components/inputs/cf_search_field.dart';
import 'package:caja_facil/presentation/components/feedback/cf_toast.dart';

void main() {
  group('Widget Tests - POS Interactive (Sprint 41)', () {
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

      // 3. Verificar los placeholders de Totales e Importes iniciales
      expect(find.text('TOTAL A PAGAR:'), findsOneWidget);
      expect(find.text('L 0.00'), findsNWidgets(4)); // Subtotal, ISV, Descuentos, Total
      expect(find.text('SUBTOTAL:'), findsOneWidget);
      expect(find.text('ISV (15%):'), findsOneWidget);
      expect(find.text('DESCUENTOS:'), findsOneWidget);

      // 4. Verificar la presencia de la grilla vacía
      expect(find.text('Carrito de Ventas Vacío'), findsOneWidget);
      expect(find.text('Líneas: 0'), findsOneWidget);
      expect(find.text('Unidades: 0.00'), findsOneWidget);

      // 5. Verificar los botones de favoritos
      expect(find.text('FAVORITOS / RÁPIDO'), findsOneWidget);
      expect(find.text('Coca Cola'), findsOneWidget);
      expect(find.text('Pan Blanco'), findsOneWidget);

      // 6. Verificar la barra de atajos inferior
      expect(find.text('ENTER'), findsOneWidget);
      expect(find.text('DEL'), findsOneWidget);
      expect(find.text('ESC'), findsOneWidget);
    });

    testWidgets('ProductSearchField has initial autofocus', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      expect(searchFieldFinder, findsOneWidget);

      final TextField textFieldWidget = tester.widget<TextField>(
        find.descendant(
          of: searchFieldFinder,
          matching: find.byType(TextField),
        ),
      );

      expect(textFieldWidget.focusNode?.hasFocus, isTrue);
    });

    testWidgets('Adding a valid product adds a row and updates totals', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      // Buscar el input de búsqueda de productos
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      // Debería desaparecer el empty state y aparecer el producto en la tabla
      expect(find.text('Carrito de Ventas Vacío'), findsNothing);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);

      // Subtotal = 25.00, ISV (15%) = 3.75, Total = 28.75
      expect(find.text('L 25.00'), findsNWidgets(3)); // Precio U., Fila Total y Subtotal
      expect(find.text('L 3.75'), findsOneWidget); // ISV
      expect(find.text('L 28.75'), findsOneWidget); // Total a pagar

      expect(find.text('Líneas: 1'), findsOneWidget);
      expect(find.text('Unidades: 1.00'), findsOneWidget);
    });

    testWidgets('Adding the same product again increments quantity instead of adding a row', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      // Agregar Coca Cola por primera vez
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      // Agregar Coca Cola por segunda vez
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      // No debe haber más de una fila de Coca Cola
      expect(find.text('Coca Cola 355ml'), findsOneWidget);

      // Unidades: 2.00, Subtotal: 50.00, ISV: 7.50, Total: 57.50
      expect(find.text('2.00'), findsOneWidget);
      expect(find.text('L 50.00'), findsNWidgets(2)); // Fila Total y Subtotal
      expect(find.text('L 7.50'), findsOneWidget); // ISV
      expect(find.text('L 57.50'), findsOneWidget); // Total

      expect(find.text('Líneas: 1'), findsOneWidget);
      expect(find.text('Unidades: 2.00'), findsOneWidget);
    });

    testWidgets('Deleting a product row updates the cart and totals', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      // Agregar Coca Cola
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      // Seleccionar la fila haciendo tap en la celda
      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pumpAndSettle();

      // Refocar el buscador de productos para que reciba el evento de teclado y lo propague
      await tester.tap(find.byType(CFSearchField));
      await tester.pumpAndSettle();

      // Presionar la tecla DELETE física simulada
      await tester.sendKeyEvent(LogicalKeyboardKey.delete);
      await tester.pumpAndSettle();

      // Debería vaciarse el carrito y mostrar de nuevo el empty state
      expect(find.text('Carrito de Ventas Vacío'), findsOneWidget);
      expect(find.text('L 0.00'), findsNWidgets(4));
    });

    testWidgets('Adding a non-existent product shows error Toast', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      // Escanear código no registrado
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '999');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      // Debe aparecer el Toast de error
      expect(find.byType(CFToast), findsOneWidget);
      expect(find.text('No se encontró el producto.'), findsOneWidget);
    });

    testWidgets('Autofocus is preserved after adding a product', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      // El TextField interno debe conservar el foco
      final TextField textFieldWidget = tester.widget<TextField>(
        find.descendant(
          of: searchFieldFinder,
          matching: find.byType(TextField),
        ),
      );
      expect(textFieldWidget.focusNode?.hasFocus, isTrue);
    });
  });
}
