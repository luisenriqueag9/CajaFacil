import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:caja_facil/presentation/screens/pos/pos_screen.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/pos_shell.dart';
import 'package:caja_facil/presentation/components/inputs/cf_search_field.dart';
import 'package:caja_facil/presentation/components/inputs/cf_text_field.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/product_search_overlay.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/search_result_tile.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/edit_cart_item_dialog.dart';

void main() {
  group('Widget Tests - POS Search & Autocomplete (Sprint 42)', () {
    testWidgets('PosScreen renders correctly and shows placeholders', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      expect(find.byType(PosShell), findsOneWidget);
      expect(find.textContaining('Cajero: Cajero Demo'), findsOneWidget);
      expect(find.text('TOTAL A PAGAR:'), findsOneWidget);
      expect(find.text('Carrito de Ventas Vacío'), findsOneWidget);
    });

    testWidgets('Search by exact code displays matching suggestions in real time', (WidgetTester tester) async {
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
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);
    });

    testWidgets('Search by partial name matches case-insensitively', (WidgetTester tester) async {
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
      await tester.enterText(searchFieldFinder, 'co');
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);
    });

    testWidgets('Keyboard arrow navigation highlights suggestions, ENTER adds it, and panel closes', (WidgetTester tester) async {
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
      await tester.enterText(searchFieldFinder, '00');
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);

      await tester.sendKeyEvent(LogicalKeyboardKey.arrowDown);
      await tester.pump();

      await tester.sendKeyEvent(LogicalKeyboardKey.enter);
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsNothing);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);
    });

    testWidgets('ESC key closes suggestions and retains text field focus', (WidgetTester tester) async {
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
      await tester.enterText(searchFieldFinder, '00');
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);

      await tester.sendKeyEvent(LogicalKeyboardKey.escape);
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsNothing);

      final TextField textFieldWidget = tester.widget<TextField>(
        find.descendant(
          of: searchFieldFinder,
          matching: find.byType(TextField),
        ),
      );
      expect(textFieldWidget.focusNode?.hasFocus, isTrue);
    });

    testWidgets('Tapping on a suggestion adds it to the cart and closes panel', (WidgetTester tester) async {
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
      await tester.enterText(searchFieldFinder, '002');
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);

      await tester.tap(find.descendant(
        of: find.byType(SearchResultTile),
        matching: find.text('Pan Blanco'),
      ));
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsNothing);
      expect(find.text('Pan Blanco'), findsNWidgets(2));
    });
  });

  group('Widget Tests - POS Cart Line Management (Sprint 43)', () {
    testWidgets('Double clicking on a row opens the EditCartItemDialog', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      // Agregar un producto para que haya una fila
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      // Hacer doble click en el producto de la grilla
      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pump(const Duration(milliseconds: 50));
      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pumpAndSettle();

      // Debe estar abierto el diálogo
      expect(find.byType(EditCartItemDialog), findsOneWidget);
      expect(find.text('Editar Línea de Venta'), findsOneWidget);
    });

    testWidgets('Pressing F4 on a selected row opens the EditCartItemDialog', (WidgetTester tester) async {
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

      // Seleccionar la fila del carrito
      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pumpAndSettle();

      // Refocar el buscador de productos para propagar el teclado
      await tester.tap(find.byType(CFSearchField));
      await tester.pumpAndSettle();

      // Presionar la tecla de función F4
      await tester.sendKeyEvent(LogicalKeyboardKey.f4);
      await tester.pumpAndSettle();

      expect(find.byType(EditCartItemDialog), findsOneWidget);
    });

    testWidgets('Modifying quantity and discount updates cart row and totals upon saving', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      // Agregar Coca Cola (precio base 25.00)
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      // Abrir diálogo por doble tap
      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pump(const Duration(milliseconds: 50));
      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pumpAndSettle();

      // Cambiar cantidad a '5'
      final qtyInput = find.descendant(
        of: find.widgetWithText(CFTextField, 'Cantidad'),
        matching: find.byType(TextField),
      );
      await tester.enterText(qtyInput, '5');

      // Cambiar descuento a '10'
      final descInput = find.descendant(
        of: find.widgetWithText(CFTextField, 'Descuento (L)'),
        matching: find.byType(TextField),
      );
      await tester.enterText(descInput, '10');
      await tester.pump();

      // Dar click en el botón Guardar
      await tester.tap(find.text('Guardar'));
      await tester.pumpAndSettle();

      // El diálogo debe cerrarse
      expect(find.byType(EditCartItemDialog), findsNothing);

      // Los valores del mostrador deben cambiar en vivo:
      // Subtotal = 25.00 * 5 = 125.00
      // Descuento = 10.00
      // ISV (15%) = 125.00 * 0.15 = 18.75
      // Total = 125.00 + 18.75 - 10.00 = 133.75
      expect(find.text('L 125.00'), findsOneWidget); // Desglose subtotal
      expect(find.text('L 115.00'), findsOneWidget); // Fila total (125 - 10)
      expect(find.text('L 10.00'), findsNWidgets(2)); // Descuento en la fila y en desglose
      expect(find.text('L 18.75'), findsOneWidget); // ISV
      expect(find.text('L 133.75'), findsOneWidget); // Total
    });

    testWidgets('Canceling the edit dialog leaves values unchanged', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      await tester.enterText(find.byType(CFSearchField), '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pump(const Duration(milliseconds: 50));
      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pumpAndSettle();

      // Cambiar cantidad a '99'
      final qtyInput = find.descendant(
        of: find.widgetWithText(CFTextField, 'Cantidad'),
        matching: find.byType(TextField),
      );
      await tester.enterText(qtyInput, '99');
      await tester.pump();

      // Dar click en Cancelar
      await tester.tap(find.text('Cancelar'));
      await tester.pumpAndSettle();

      // El diálogo debe cerrarse y mantener los valores iniciales (Cantidad 1.00, subtotal 25.00)
      expect(find.byType(EditCartItemDialog), findsNothing);
      expect(find.text('1.00'), findsOneWidget);
      expect(find.text('L 25.00'), findsNWidgets(3));
    });
  });
}
