import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:caja_facil/presentation/components/buttons/cf_button.dart';
import 'package:caja_facil/presentation/components/buttons/cf_icon_button.dart';
import 'package:caja_facil/presentation/components/inputs/cf_text_field.dart';
import 'package:caja_facil/presentation/components/inputs/cf_search_field.dart';
import 'package:caja_facil/presentation/components/dialogs/cf_dialog.dart';
import 'package:caja_facil/presentation/components/feedback/cf_toast.dart';

void main() {
  group('Widget Tests - Biblioteca de Componentes CajaFácil', () {
    // 1. Test para CFButton
    testWidgets('CFButton renderiza label y reacciona a taps', (WidgetTester tester) async {
      bool pressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CFButton(
              label: 'Pagar',
              onPressed: () {
                pressed = true;
              },
            ),
          ),
        ),
      );

      // Verificar que se renderiza el texto del botón
      expect(find.text('Pagar'), findsOneWidget);

      // Pulsar el botón
      await tester.tap(find.text('Pagar'));
      await tester.pump();

      // Verificar que el callback se ejecutó
      expect(pressed, isTrue);
    });

    testWidgets('CFButton deshabilitado no reacciona a taps', (WidgetTester tester) async {
      bool pressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CFButton(
              label: 'Pagar',
              enabled: false,
              onPressed: () {
                pressed = true;
              },
            ),
          ),
        ),
      );

      await tester.tap(find.text('Pagar'));
      await tester.pump();

      // El callback NO debe ejecutarse
      expect(pressed, isFalse);
    });

    // 2. Test para CFTextField
    testWidgets('CFTextField renderiza label y placeholder, y permite entrada de texto', (WidgetTester tester) async {
      final controller = TextEditingController();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CFTextField(
              controller: controller,
              label: 'Usuario',
              placeholder: 'Ingrese su usuario',
            ),
          ),
        ),
      );

      // Verificar label y placeholder
      expect(find.text('Usuario'), findsOneWidget);
      expect(find.text('Ingrese su usuario'), findsOneWidget);

      // Escribir texto
      await tester.enterText(find.byType(TextField), 'luis.ag');
      await tester.pump();

      // Verificar que el controlador contiene el valor escrito
      expect(controller.text, 'luis.ag');
    });

    // 3. Test para CFSearchField
    testWidgets('CFSearchField expone boton de limpiar cuando tiene texto', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CFSearchField(
              placeholder: 'Buscar...',
            ),
          ),
        ),
      );

      // Escribir en el buscador
      await tester.enterText(find.byType(TextField), 'Leche');
      await tester.pumpAndSettle();

      // Debería aparecer el botón de limpiar (el IconButton con icono de limpiar/clear)
      expect(find.byType(IconButton), findsOneWidget);

      // Limpiar texto
      await tester.tap(find.byType(IconButton));
      await tester.pumpAndSettle();

      // El texto en el TextField debe estar vacío
      final textField = tester.widget<TextField>(find.byType(TextField));
      expect(textField.controller?.text, isEmpty);
    });

    // 4. Test para CFDialog
    testWidgets('CFDialog se dibuja con titulo y responde a boton de cierre', (WidgetTester tester) async {
      bool closed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Builder(
              builder: (context) {
                return CFButton(
                  label: 'Abrir',
                  onPressed: () {
                    CFDialog.show(
                      context: context,
                      title: 'Mi Diálogo',
                      onClose: () {
                        closed = true;
                        Navigator.of(context).pop();
                      },
                      child: const Text('Contenido'),
                    );
                  },
                );
              },
            ),
          ),
        ),
      );

      // Hacer tap para abrir diálogo
      await tester.tap(find.text('Abrir'));
      await tester.pumpAndSettle();

      // Verificar que se renderiza el diálogo y su título
      expect(find.text('Mi Diálogo'), findsOneWidget);
      expect(find.text('Contenido'), findsOneWidget);

      // Buscar el botón de cierre (el X icon button)
      final closeBtn = find.byType(CFIconButton);
      expect(closeBtn, findsOneWidget);

      await tester.tap(closeBtn);
      await tester.pumpAndSettle();

      // Verificar que se invocó el callback de cierre
      expect(closed, isTrue);
    });

    // 5. Test para CFToast
    testWidgets('CFToast renderiza el mensaje', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CFToast(
              message: 'Conexión Restablecida',
              type: ToastType.success,
            ),
          ),
        ),
      );

      expect(find.text('Conexión Restablecida'), findsOneWidget);
    });
  });
}
