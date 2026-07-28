import 'package:flutter/material.dart';
import '../../theme/app_spacing.dart';

/// CFLoadingIndicator: Spinner concéntrico oficial de CajaFácil.
class CFLoadingIndicator extends StatelessWidget {
  const CFLoadingIndicator({
    super.key,
    this.message,
    this.size = 32.0,
  });

  final String? message;
  final double size;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    final child = SizedBox(
      width: size,
      height: size,
      child: CircularProgressIndicator(
        strokeWidth: 3.0,
        valueColor: AlwaysStoppedAnimation<Color>(colorScheme.primary),
      ),
    );

    if (message != null) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            child,
            const SizedBox(height: AppSpacing.s),
            Text(
              message!,
              style: theme.textTheme.bodyMedium?.copyWith(
                color: colorScheme.onSurface.withOpacity(0.7),
              ),
            ),
          ],
        ),
      );
    }

    return Center(child: child);
  }
}
