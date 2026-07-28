import 'package:flutter/material.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';
import '../theme/app_colors.dart';
import '../components/buttons/cf_button.dart';
import '../components/buttons/cf_icon_button.dart';
import '../components/inputs/cf_text_field.dart';
import '../components/inputs/cf_search_field.dart';
import '../components/inputs/cf_number_field.dart';
import '../components/dialogs/cf_dialog.dart';
import '../components/dialogs/cf_confirm_dialog.dart';
import '../components/feedback/cf_toast.dart';
import '../components/feedback/cf_loading_indicator.dart';
import '../components/feedback/cf_progress_indicator.dart';
import '../components/layout/cf_panel.dart';
import '../components/layout/cf_section.dart';
import '../components/navigation/cf_top_bar.dart';
import '../components/data/cf_data_table.dart';
import '../components/data/cf_empty_state.dart';

/// ComponentShowcaseScreen: Pantalla oficial de visualización y pruebas de la biblioteca de componentes.
///
/// Propósito:
/// - Mostrar en vivo el comportamiento de todos los componentes.
/// - Validar contrastes y estados del Design System en resoluciones adaptativas.
class ComponentShowcaseScreen extends StatefulWidget {
  const ComponentShowcaseScreen({super.key});

  @override
  State<ComponentShowcaseScreen> createState() => _ComponentShowcaseScreenState();
}

class _ComponentShowcaseScreenState extends State<ComponentShowcaseScreen> {
  int _selectedTableIndex = 0;
  double _numberValue = 1.0;
  double _progressValue = 0.45;

  void _showTestToast(ToastType type, String message) {
    CFToast.show(context, message: message, type: type);
  }

  void _showTestDialog() {
    CFDialog.show(
      context: context,
      title: 'Ventana de Diálogo Base',
      child: const Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Este es el contenido interno del diálogo. Puedes presionar ESC o la X de cierre.'),
        ],
      ),
      actions: [
        CFButton(
          label: 'Aceptar',
          onPressed: () => Navigator.of(context).pop(),
        ),
      ],
    );
  }

  void _showTestConfirmDialog() {
    CFConfirmDialog.show(
      context: context,
      title: 'Confirmación Crítica',
      message: '¿Está seguro de que desea anular la factura actual? Esta acción no se puede revertir.',
      confirmLabel: 'Anular',
      onConfirm: (pin) {
        _showTestToast(ToastType.success, 'Factura anulada con éxito');
      },
    );
  }

  void _showTestSupervisorDialog() {
    CFConfirmDialog.show(
      context: context,
      title: 'Validación de Supervisor',
      message: 'Se requiere autorización para aplicar un descuento del 20%.',
      requiresSupervisorPin: true,
      onConfirm: (pin) {
        _showTestToast(ToastType.success, 'Autorizado con PIN: $pin');
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: AppColors.backgroundLight,
      body: Column(
        children: [
          // Top bar contextual
          CFTopBar(
            userName: 'Luis Enrique AG',
            branchName: 'Tegucigalpa Centro',
            posTerminalName: 'Caja #1',
            isOnline: true,
            isPrinterConnected: true,
            hasPendingSync: true,
            currentTime: '14:04',
            onLogout: () => _showTestToast(ToastType.info, 'Logout pulsado'),
          ),
          // Área principal scrolleable
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(AppSpacing.l),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'BIBLIOTECA OFICIAL DE COMPONENTES',
                    style: TextStyle(
                      fontSize: 24.0,
                      fontWeight: FontWeight.bold,
                      color: AppColors.primary,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.s),
                  Text(
                    'Esta pantalla expone todos los componentes interactivos de CajaFácil para asegurar el cumplimiento del Design System y la velocidad de interfaz.',
                    style: TextStyle(color: theme.hintColor),
                  ),
                  const SizedBox(height: AppSpacing.l),

                  // 1. Botones
                  CFSection(
                    title: '1. Botones (CFButton / CFIconButton)',
                    child: CFPanel(
                      child: Wrap(
                        spacing: AppSpacing.m,
                        runSpacing: AppSpacing.s,
                        children: [
                          CFButton(
                            label: 'Principal (Cobrar)',
                            variant: ButtonVariant.primary,
                            onPressed: () => _showTestToast(ToastType.success, 'Principal pulsado'),
                          ),
                          CFButton(
                            label: 'Secundario',
                            variant: ButtonVariant.secondary,
                            onPressed: () => _showTestToast(ToastType.info, 'Secundario pulsado'),
                          ),
                          CFButton(
                            label: 'Contorno (Outline)',
                            variant: ButtonVariant.outline,
                            onPressed: () => _showTestToast(ToastType.info, 'Outline pulsado'),
                          ),
                          CFButton(
                            label: 'Destructivo (Anular)',
                            variant: ButtonVariant.destructive,
                            onPressed: () => _showTestToast(ToastType.error, 'Destructivo pulsado'),
                          ),
                          const CFButton(
                            label: 'Deshabilitado',
                            enabled: false,
                          ),
                          CFButton(
                            label: 'Cargando',
                            loading: true,
                            onPressed: () {},
                          ),
                          CFIconButton(
                            icon: AppIcons.delete,
                            tooltip: 'Eliminar línea (DEL)',
                            onPressed: () => _showTestToast(ToastType.warning, 'Eliminar pulsado'),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: AppSpacing.l),

                  // 2. Inputs
                  CFSection(
                    title: '2. Inputs (CFSearchField / CFTextField / CFNumberField)',
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          child: CFPanel(
                            child: Column(
                              children: [
                                CFSearchField(
                                  onSubmitted: (val) => _showTestToast(ToastType.info, 'Escaneado: $val'),
                                ),
                                const SizedBox(height: AppSpacing.m),
                                const CFTextField(
                                  label: 'Nombre de Cliente',
                                  placeholder: 'Ingrese el nombre...',
                                ),
                                const SizedBox(height: AppSpacing.m),
                                const CFTextField(
                                  label: 'Error de Validación',
                                  placeholder: 'Ingrese datos...',
                                  errorText: 'El formato del correo es inválido',
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: AppSpacing.m),
                        Expanded(
                          child: CFPanel(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Cantidad / Peso',
                                  style: TextStyle(fontWeight: FontWeight.bold),
                                ),
                                const SizedBox(height: AppSpacing.s),
                                CFNumberField(
                                  value: _numberValue,
                                  min: 0.1,
                                  max: 99.0,
                                  step: 0.5,
                                  onChanged: (val) {
                                    setState(() {
                                      _numberValue = val;
                                    });
                                  },
                                ),
                                const SizedBox(height: AppSpacing.m),
                                Text('Valor actual del campo: $_numberValue'),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.l),

                  // 3. Tablas de Datos
                  CFSection(
                    title: '3. Datos (CFDataTable / CFEmptyState)',
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          flex: 2,
                          child: CFPanel(
                            padding: EdgeInsets.zero,
                            child: CFDataTable(
                              columns: const [
                                CFDataColumn(label: '#', width: 40.0),
                                CFDataColumn(label: 'Descripción'),
                                CFDataColumn(label: 'Cant.', numeric: true, width: 80.0),
                                CFDataColumn(label: 'Total', numeric: true, width: 100.0),
                              ],
                              selectedIndex: _selectedTableIndex,
                              onRowSelected: (index) {
                                setState(() {
                                  _selectedTableIndex = index;
                                });
                              },
                              rows: [
                                [
                                  const Text('1'),
                                  const Text('Leche Sula Entera 1L'),
                                  const Text('2.00', style: TextStyle(fontFamily: 'monospace')),
                                  const Text('L 64.00', style: TextStyle(fontFamily: 'monospace')),
                                ],
                                [
                                  const Text('2'),
                                  const Text('Pan Bimbo Blanco'),
                                  const Text('1.00', style: TextStyle(fontFamily: 'monospace')),
                                  const Text('L 46.00', style: TextStyle(fontFamily: 'monospace')),
                                ],
                                [
                                  const Text('3'),
                                  const Text('Tomate Manzano Libra'),
                                  const Text('1.25', style: TextStyle(fontFamily: 'monospace')),
                                  const Text('L 30.00', style: TextStyle(fontFamily: 'monospace')),
                                ],
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: AppSpacing.m),
                        Expanded(
                          flex: 1,
                          child: CFPanel(
                            child: const CFEmptyState(
                              icon: AppIcons.search,
                              title: 'Sin Productos',
                              description: 'Escanee un código de barra para iniciar la venta.',
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.l),

                  // 4. Diálogos y Retroalimentación
                  CFSection(
                    title: '4. Diálogos, Badges y Feedback',
                    child: CFPanel(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Wrap(
                            spacing: AppSpacing.m,
                            runSpacing: AppSpacing.s,
                            children: [
                              CFButton(
                                label: 'Mostrar Diálogo Base',
                                variant: ButtonVariant.outline,
                                onPressed: _showTestDialog,
                              ),
                              CFButton(
                                label: 'Mostrar Confirmación',
                                variant: ButtonVariant.destructive,
                                onPressed: _showTestConfirmDialog,
                              ),
                              CFButton(
                                label: 'Firma Supervisor',
                                variant: ButtonVariant.secondary,
                                onPressed: _showTestSupervisorDialog,
                              ),
                              CFButton(
                                label: 'Toast Éxito',
                                onPressed: () => _showTestToast(ToastType.success, '¡Venta registrada con éxito!'),
                              ),
                              CFButton(
                                label: 'Toast Error',
                                variant: ButtonVariant.destructive,
                                onPressed: () => _showTestToast(ToastType.error, 'No hay conexión con el servidor local'),
                              ),
                            ],
                          ),
                          const SizedBox(height: AppSpacing.m),
                          // Progreso e indicadores
                          Row(
                            children: [
                              const CFLoadingIndicator(),
                              const SizedBox(width: AppSpacing.m),
                              Expanded(
                                child: CFProgressIndicator(
                                  value: _progressValue,
                                  label: 'Subiendo facturas pendientes...',
                                ),
                              ),
                              const SizedBox(width: AppSpacing.m),
                              CFButton(
                                label: 'Avanzar Sync',
                                onPressed: () {
                                  setState(() {
                                    _progressValue = (_progressValue + 0.15) % 1.0;
                                  });
                                },
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: AppSpacing.xl),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
