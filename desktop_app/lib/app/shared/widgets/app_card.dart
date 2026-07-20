import 'package:flutter/material.dart';

import '../../core/theme/app_radius.dart';
import '../../core/theme/app_shadows.dart';
import '../../core/theme/app_spacing.dart';

class AppCard extends StatelessWidget {
  const AppCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(AppSpacing.lg),
    this.width,
    this.height,
    this.onTap,
    this.showShadow = true,
  });

  final Widget child;
  final EdgeInsetsGeometry padding;
  final double? width;
  final double? height;
  final VoidCallback? onTap;
  final bool showShadow;

  @override
  Widget build(BuildContext context) {
    final content = Container(
      width: width,
      height: height,
      padding: padding,
      decoration: BoxDecoration(
        color: Theme.of(context).cardTheme.color ?? Theme.of(context).colorScheme.surface,
        borderRadius: BorderRadius.circular(AppRadius.large),
        border: Border.all(
          color: Theme.of(context).brightness == Brightness.dark
              ? const Color(0xFF2E2E3E)
              : const Color(0xFFE2E8F0),
        ),
        boxShadow: showShadow ? AppShadows.small : null,
      ),
      child: child,
    );

    if (onTap == null) {
      return content;
    }

    return MouseRegion(
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        onTap: onTap,
        child: content,
      ),
    );
  }
}