import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../shared/widgets/app_sidebar.dart';

class MainLayout extends StatelessWidget {
  const MainLayout({
    super.key,
    required this.child,
  });

  final Widget child;

  @override
  Widget build(BuildContext context) {
    final currentRoute = GoRouterState.of(context).uri.path;

    return Scaffold(
      body: Row(
        children: [
          AppSidebar(
            currentRoute: currentRoute,
            onNavigate: (route) {
              if (route != currentRoute) {
                context.go(route);
              }
            },
          ),
          Expanded(
            child: Container(
              color: Theme.of(context).scaffoldBackgroundColor,
              child: child,
            ),
          ),
        ],
      ),
    );
  }
}