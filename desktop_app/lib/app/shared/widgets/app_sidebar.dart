import 'package:flutter/material.dart';

import '../../core/theme/app_colors.dart';
import '../../core/theme/app_radius.dart';
import '../../core/theme/app_spacing.dart';

class AppSidebar extends StatelessWidget {
  const AppSidebar({
    super.key,
    required this.currentRoute,
    required this.onNavigate,
  });

  final String currentRoute;
  final ValueChanged<String> onNavigate;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 250,
      color: AppColors.primary,
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const _SidebarHeader(),
          const SizedBox(height: AppSpacing.xl),
          const Text(
            'MENÚ PRINCIPAL',
            style: TextStyle(
              color: Color(0xFFC5F0ED),
              fontSize: 12,
              fontWeight: FontWeight.w600,
              letterSpacing: 1,
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          _SidebarItem(
            icon: Icons.dashboard_outlined,
            selectedIcon: Icons.dashboard_rounded,
            label: 'Dashboard',
            route: '/dashboard',
            currentRoute: currentRoute,
            onTap: onNavigate,
          ),
          _SidebarItem(
            icon: Icons.people_outline_rounded,
            selectedIcon: Icons.people_rounded,
            label: 'Clientes',
            route: '/clientes',
            currentRoute: currentRoute,
            onTap: onNavigate,
          ),
          _SidebarItem(
            icon: Icons.inventory_2_outlined,
            selectedIcon: Icons.inventory_2_rounded,
            label: 'Productos',
            route: '/productos',
            currentRoute: currentRoute,
            onTap: onNavigate,
          ),
          _SidebarItem(
            icon: Icons.warehouse_outlined,
            selectedIcon: Icons.warehouse_rounded,
            label: 'Inventario',
            route: '/inventario',
            currentRoute: currentRoute,
            onTap: onNavigate,
          ),
          _SidebarItem(
            icon: Icons.point_of_sale_outlined,
            selectedIcon: Icons.point_of_sale_rounded,
            label: 'Ventas',
            route: '/ventas',
            currentRoute: currentRoute,
            onTap: onNavigate,
          ),
          _SidebarItem(
            icon: Icons.bar_chart_outlined,
            selectedIcon: Icons.bar_chart_rounded,
            label: 'Reportes',
            route: '/reportes',
            currentRoute: currentRoute,
            onTap: onNavigate,
          ),
          const Spacer(),
          _SidebarItem(
            icon: Icons.settings_outlined,
            selectedIcon: Icons.settings_rounded,
            label: 'Configuración',
            route: '/configuracion',
            currentRoute: currentRoute,
            onTap: onNavigate,
          ),
        ],
      ),
    );
  }
}

class _SidebarHeader extends StatelessWidget {
  const _SidebarHeader();

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 44,
          height: 44,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(AppRadius.medium),
          ),
          child: const Icon(
            Icons.point_of_sale_rounded,
            color: AppColors.primary,
            size: 26,
          ),
        ),
        const SizedBox(width: AppSpacing.md),
        const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'CajaFácil',
              style: TextStyle(
                color: Colors.white,
                fontSize: 22,
                fontWeight: FontWeight.w700,
              ),
            ),
            Text(
              'Punto de venta',
              style: TextStyle(
                color: Color(0xFFC5F0ED),
                fontSize: 12,
              ),
            ),
          ],
        ),
      ],
    );
  }
}

class _SidebarItem extends StatelessWidget {
  const _SidebarItem({
    required this.icon,
    required this.selectedIcon,
    required this.label,
    required this.route,
    required this.currentRoute,
    required this.onTap,
  });

  final IconData icon;
  final IconData selectedIcon;
  final String label;
  final String route;
  final String currentRoute;
  final ValueChanged<String> onTap;

  bool get isSelected => currentRoute == route;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.sm),
      child: Material(
        color: isSelected
            ? Colors.white.withValues(alpha: 0.16)
            : Colors.transparent,
        borderRadius: BorderRadius.circular(AppRadius.medium),
        child: InkWell(
          onTap: () => onTap(route),
          borderRadius: BorderRadius.circular(AppRadius.medium),
          child: Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.md,
              vertical: 13,
            ),
            child: Row(
              children: [
                Icon(
                  isSelected ? selectedIcon : icon,
                  color: Colors.white,
                  size: 22,
                ),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: Text(
                    label,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 14,
                      fontWeight:
                          isSelected ? FontWeight.w600 : FontWeight.w400,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}