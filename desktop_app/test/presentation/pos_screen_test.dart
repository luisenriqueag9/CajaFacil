import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:dio/dio.dart';

import 'package:caja_facil/presentation/screens/pos/pos_screen.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/pos_shell.dart';
import 'package:caja_facil/presentation/components/inputs/cf_search_field.dart';
import 'package:caja_facil/presentation/components/inputs/cf_text_field.dart';
import 'package:caja_facil/presentation/components/feedback/cf_toast.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/product_search_overlay.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/search_result_tile.dart';
import 'package:caja_facil/presentation/screens/pos/widgets/edit_cart_item_dialog.dart';

import 'package:caja_facil/app/shared/cache/memory_cache.dart';
import 'package:caja_facil/app/modules/product/presentation/models/product_search_result.dart';
import 'package:caja_facil/app/modules/product/data/repositories/http_product_search_repository.dart';
import 'fake_product_search_repository.dart';

void main() {
  group('Widget Tests - POS Search & Autocomplete (Sprint 44)', () {
    late FakeProductSearchRepository fakeRepo;

    setUp(() {
      fakeRepo = FakeProductSearchRepository();
    });

    testWidgets('PosScreen renders correctly and shows placeholders', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      expect(find.byType(PosShell), findsOneWidget);
      expect(find.textContaining('Caja 01'), findsOneWidget);
      expect(find.text('TOTAL A PAGAR:'), findsOneWidget);
      expect(find.text('Carrito de Ventas Vacío'), findsOneWidget);
    });

    testWidgets('Search by exact code displays matching suggestions in real time', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.pump(const Duration(milliseconds: 250)); // Debounce trigger
      await tester.pumpAndSettle();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);
    });

    testWidgets('Search by partial name matches case-insensitively', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, 'co');
      await tester.pump(const Duration(milliseconds: 250)); // Debounce trigger
      await tester.pumpAndSettle();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);
    });

    testWidgets('Keyboard arrow navigation highlights suggestions, ENTER adds it, and panel closes', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '00');
      await tester.pump(const Duration(milliseconds: 250)); // Debounce trigger
      await tester.pumpAndSettle();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);

      await tester.sendKeyEvent(LogicalKeyboardKey.arrowDown);
      await tester.pump();

      await tester.sendKeyEvent(LogicalKeyboardKey.enter);
      await tester.pump();
      await tester.pumpAndSettle(); // Resolve search addProduct Future

      expect(find.byType(ProductSearchOverlay), findsNothing);
      expect(find.text('Coca Cola 355ml'), findsOneWidget);
    });

    testWidgets('ESC key closes suggestions and retains text field focus', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '00');
      await tester.pump(const Duration(milliseconds: 250)); // Debounce trigger
      await tester.pumpAndSettle();

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
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '002');
      await tester.pump(const Duration(milliseconds: 250)); // Debounce trigger
      await tester.pumpAndSettle();

      expect(find.byType(ProductSearchOverlay), findsOneWidget);

      await tester.tap(find.descendant(
        of: find.byType(SearchResultTile),
        matching: find.text('Pan Blanco'),
      ));
      await tester.pump();
      await tester.pumpAndSettle(); // Resolve addProduct Future

      expect(find.byType(ProductSearchOverlay), findsNothing);
      expect(find.text('Pan Blanco'), findsNWidgets(2)); // Favorites & Cart Row
    });

    testWidgets('Search with network error shows CFToast and retains focus', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));
      fakeRepo.shouldThrowNetworkError = true;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, 'Coca');
      await tester.pump(const Duration(milliseconds: 250)); // Debounce trigger
      await tester.pumpAndSettle();

      // Debería mostrar Toast de error
      expect(find.byType(CFToast), findsOneWidget);
      expect(find.text('Error al conectar con el catálogo.'), findsOneWidget);

      // El overlay no debería abrirse
      expect(find.byType(ProductSearchOverlay), findsNothing);

      // Foco del buscador de productos se mantiene intacto
      final TextField textFieldWidget = tester.widget<TextField>(
        find.descendant(
          of: searchFieldFinder,
          matching: find.byType(TextField),
        ),
      );
      expect(textFieldWidget.focusNode?.hasFocus, isTrue);
    });

    testWidgets('Search with timeout error shows CFToast', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));
      fakeRepo.shouldTimeout = true;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, 'Coca');
      await tester.pump(const Duration(milliseconds: 250)); // Debounce trigger
      await tester.pumpAndSettle();

      expect(find.byType(CFToast), findsOneWidget);
      expect(find.text('Error al conectar con el catálogo.'), findsOneWidget);
    });

    testWidgets('Debouncer prevents intermediate requests when typing quickly', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      
      // Escribir rápidamente letra por letra con pequeños retardos (menores a 200ms)
      await tester.enterText(searchFieldFinder, 'C');
      await tester.pump(const Duration(milliseconds: 50));
      await tester.enterText(searchFieldFinder, 'Co');
      await tester.pump(const Duration(milliseconds: 50));
      await tester.enterText(searchFieldFinder, 'Coc');
      await tester.pump(const Duration(milliseconds: 50));
      await tester.enterText(searchFieldFinder, 'Coca');
      
      // En este punto, no se debe haber disparado ninguna búsqueda en el repositorio aún
      expect(fakeRepo.searchCount, 0);

      // Esperar que pase el tiempo de debounce
      await tester.pump(const Duration(milliseconds: 250));
      await tester.pumpAndSettle();

      // Debe haber exactamente 1 búsqueda realizada
      expect(fakeRepo.searchCount, 1);
    });

    testWidgets('CancelToken cancels previous requests', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));
      // Introducir retardo simulado de red en el fake repo
      fakeRepo.delay = const Duration(milliseconds: 100);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      final searchFieldFinder = find.byType(CFSearchField);
      
      // Iniciar búsqueda A
      await tester.enterText(searchFieldFinder, 'Co');
      await tester.pump(const Duration(milliseconds: 250)); // Dispara debounce de A

      // Escribir nueva consulta B antes de que A termine de responder (100ms de latencia de red)
      await tester.enterText(searchFieldFinder, 'Pan');
      await tester.pump(const Duration(milliseconds: 250)); // Dispara debounce de B y cancela A

      // Dejar que todo termine
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pumpAndSettle();

      // El resultado en el overlay debe coincidir únicamente con la consulta B ("Pan Blanco")
      expect(
        find.descendant(
          of: find.byType(ProductSearchOverlay),
          matching: find.text('Pan Blanco'),
        ),
        findsOneWidget,
      );
      expect(find.text('Coca Cola 355ml'), findsNothing);
    });
  });

  group('Widget Tests - POS Cart Line Management (Sprint 44)', () {
    late FakeProductSearchRepository fakeRepo;

    setUp(() {
      fakeRepo = FakeProductSearchRepository();
    });

    testWidgets('Double clicking on a row opens the EditCartItemDialog', (WidgetTester tester) async {
      await tester.binding.setSurfaceSize(const Size(1920, 1080));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      // Agregar un producto para que haya una fila
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();
      await tester.pumpAndSettle();

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
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      // Agregar Coca Cola
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();
      await tester.pumpAndSettle();

      // Seleccionar la fila del carrito
      await tester.tap(find.text('Coca Cola 355ml'));
      await tester.pump(const Duration(milliseconds: 350)); // Esperar timeout de doble click del InkWell
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
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      // Agregar Coca Cola (precio base 25.00)
      final searchFieldFinder = find.byType(CFSearchField);
      await tester.enterText(searchFieldFinder, '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();
      await tester.pumpAndSettle();

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
        MaterialApp(
          home: Scaffold(
            body: PosScreen(productSearchRepository: fakeRepo),
          ),
        ),
      );

      await tester.pump();

      await tester.enterText(find.byType(CFSearchField), '001');
      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();
      await tester.pumpAndSettle();

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

  group('Unit Tests - Shared MemoryCache & HTTP Repository (Sprint 44)', () {
    test('MemoryCache sets and gets values within TTL', () {
      final cache = MemoryCache<String, String>(ttl: const Duration(seconds: 2));
      cache.set('key1', 'value1');

      expect(cache.get('key1'), 'value1');
      expect(cache.activeEntriesCount, 1);
    });

    test('MemoryCache evicts values after TTL expires', () async {
      final cache = MemoryCache<String, String>(ttl: const Duration(milliseconds: 50));
      cache.set('key1', 'value1');

      // Esperar a que expire
      await Future.delayed(const Duration(milliseconds: 80));

      expect(cache.get('key1'), isNull);
      expect(cache.activeEntriesCount, 0);
    });

    test('HttpProductSearchRepository cache HIT avoids duplicate network calls', () async {
      final cache = MemoryCache<String, List<ProductSearchResult>>(
        ttl: const Duration(minutes: 5),
      );

      // Creamos un wrapper o mock local para HttpProductSearchRepository que redirige a fakeRepo
      // Para simular Dio y verificar que la llamada HTTP no se haga dos veces, podemos inyectar
      // un adaptador en Dio o simplemente testear el cache con el HttpProductSearchRepository real y un MockAdapter.
      // Sin embargo, para mantener los tests desacoplados, podemos usar un Dio con un HttpClientAdapter mockeado.
      final dioMock = Dio(BaseOptions(baseUrl: 'http://localhost:8000'));
      int requestCount = 0;
      
      dioMock.interceptors.add(InterceptorsWrapper(
        onRequest: (options, handler) {
          requestCount++;
          handler.resolve(Response(
            requestOptions: options,
            data: {
              'success': true,
              'message': 'OK',
              'data': [
                {'id': '1', 'code': '001', 'name': 'Coca Cola 355ml', 'price': 25.0}
              ]
            },
            statusCode: 200,
          ));
        },
      ));

      final repo = HttpProductSearchRepository(dioMock, cache);

      // Primera búsqueda (Cache MISS, requestCount debe subir a 1)
      final results1 = await repo.search('Coca');
      expect(results1.length, 1);
      expect(requestCount, 1);

      // Segunda búsqueda exacta (Cache HIT, requestCount debe seguir siendo 1)
      final results2 = await repo.search('Coca');
      expect(results2.length, 1);
      expect(requestCount, 1); // No incrementa la llamada HTTP!
    });
  });
}
