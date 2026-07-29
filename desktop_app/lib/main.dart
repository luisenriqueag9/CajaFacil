import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app/app.dart';
import 'app/core/di/dependency_container.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Bootstrap dependency injection setup (CF-ARCH-007)
  DependencyContainer.initialize();

  runApp(
    const ProviderScope(
      child: CajaFacilApp(),
    ),
  );
}