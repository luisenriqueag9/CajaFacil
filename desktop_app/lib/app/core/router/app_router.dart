import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../modules/auth/presentation/pages/login_page.dart';
import '../../modules/dashboard/presentation/pages/dashboard_page.dart';
import '../../shared/pages/module_placeholder_page.dart';
import '../config/app_config.dart';
import 'app_routes.dart';

// Riverpod Provider for GoRouter configuration
final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: AppConfig.developmentMode
        ? AppRoutes.dashboard
        : AppRoutes.login,
    debugLogDiagnostics: true,
    routes: [
      GoRoute(
        path: AppRoutes.login,
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: AppRoutes.dashboard,
        builder: (context, state) => const DashboardPage(),
      ),
      GoRoute(
        path: AppRoutes.clientes,
        builder: (context, state) => const ModulePlaceholderPage(
          title: 'Clientes',
          description: 'Administra la información de tus clientes.',
          icon: Icons.people_rounded,
        ),
      ),
      GoRoute(
        path: AppRoutes.productos,
        builder: (context, state) => const ModulePlaceholderPage(
          title: 'Productos',
          description: 'Gestiona el catálogo de productos.',
          icon: Icons.inventory_2_rounded,
        ),
      ),
      GoRoute(
        path: AppRoutes.inventario,
        builder: (context, state) => const ModulePlaceholderPage(
          title: 'Inventario',
          description: 'Controla existencias, entradas y salidas.',
          icon: Icons.warehouse_rounded,
        ),
      ),
      GoRoute(
        path: AppRoutes.ventas,
        builder: (context, state) => const ModulePlaceholderPage(
          title: 'Ventas',
          description: 'Registra y consulta las ventas del negocio.',
          icon: Icons.point_of_sale_rounded,
        ),
      ),
      GoRoute(
        path: AppRoutes.reportes,
        builder: (context, state) => const ModulePlaceholderPage(
          title: 'Reportes',
          description: 'Consulta indicadores y reportes del negocio.',
          icon: Icons.bar_chart_rounded,
        ),
      ),
      GoRoute(
        path: AppRoutes.configuracion,
        builder: (context, state) => const ModulePlaceholderPage(
          title: 'Configuración',
          description: 'Configura las opciones generales del sistema.',
          icon: Icons.settings_rounded,
        ),
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      body: Center(
        child: Text('Error Routing: ${state.error}'),
      ),
    ),
  );
});
