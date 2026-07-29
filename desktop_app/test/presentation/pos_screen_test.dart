import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:caja_facil/presentation/screens/pos/pos_screen.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/pos_shell.dart';
import 'package:caja_facil/presentation/components/inputs/cf_search_field.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/product_search_overlay.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/search_result_tile.dart';

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
      expect(find.text('ENTER'), findsOneWidget);
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

      // Teclear '001'
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.pump(); // Procesar el onChanged

      // Debería aparecer el overlay de sugerencias con Coca Cola
      expect(find.byType(ProductSearchOverlay), findsOneWidget);
      expect(find.byType(SearchResultTile), findsOneWidget);
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

      // Teclear 'co' (coincidencia parcial para Coca Cola y Leche Entera si Leche Entera tuviese 'co', pero Coca Cola es única)
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, 'co');
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);
    });

    testWidgets('Partial code matching returns multiple suggestions', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: PosScreen(),
          ),
        ),
      );

      await tester.pump();

      // Teclear '00' (debe coincidir con todos los códigos mock '001' a '005')
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '00');
      await tester.pump();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);
      expect(find.byType(SearchResultTile), findsNWidgets(5)); // Muestra las 5 sugerencias del catálogo mock
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

      // Deberían verse las sugerencias, pero ninguna resaltada por defecto
      expect(find.byType(ProductSearchOverlay), findsOneWidget);

      // Presionar Flecha Abajo para resaltar la primera sugerencia (Coca Cola 355ml)
      await tester.sendKeyEvent(LogicalKeyboardKey.arrowDown);
      await tester.pump();

      // Presionar ENTER para registrar el producto resaltado
      await tester.sendKeyEvent(LogicalKeyboardKey.enter);
      await tester.pump();

      // La sugerencia debe agregarse al carrito y el panel de autocompletado debe cerrarse
      expect(find.byType(ProductSearchOverlay), findsNothing);
      expect(find.text('Carrito de Ventas Vacío'), findsNothing);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);
      expect(find.text('Líneas: 1'), findsOneWidget);
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

      // Presionar la tecla ESC física simulada
      await tester.sendKeyEvent(LogicalKeyboardKey.escape);
      await tester.pump();

      // El panel flotante debe desaparecer
      expect(find.byType(ProductSearchOverlay), findsNothing);

      // El buscador debe mantener el foco
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

      // Tapor en la sugerencia de Pan Blanco en el panel flotante
      await tester.tap(find.descendant(
        of: find.byType(SearchResultTile),
        matching: find.text('Pan Blanco'),
      ));
      await tester.pump();

      // Debe cerrarse el panel y agregarse al carrito
      expect(find.byType(ProductSearchOverlay), findsNothing);
      expect(find.text('Pan Blanco'), findsNWidgets(2)); // En el carrito y en favoritos
      expect(find.text('Líneas: 1'), findsOneWidget);
    });
  });
}
