import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/application/use_cases/load_diagnostics.dart';
import 'package:beavernest_app/application/use_cases/load_readiness.dart';
import 'package:beavernest_app/application/use_cases/refresh_readiness.dart';
import 'package:beavernest_app/platform/web/diagnostics_repository.dart';
import 'package:beavernest_app/platform/web/readiness_repository.dart';
import 'package:beavernest_app/presentation/workspace_shell.dart';
import 'package:beavernest_app/presentation/workspace_theme.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({
    super.key,
    this.readinessRepository,
    this.diagnosticsRepository,
  });

  final ReadinessRepository? readinessRepository;
  final DiagnosticsRepository? diagnosticsRepository;

  @override
  Widget build(BuildContext context) {
    final readiness = readinessRepository ?? HttpReadinessRepository();
    final diagnostics = diagnosticsRepository ?? HttpDiagnosticsRepository();
    return MaterialApp(
      title: 'BeaverNest',
      debugShowCheckedModeBanner: false,
      theme: beaverNestTheme(),
      darkTheme: beaverNestDarkTheme(),
      themeMode: ThemeMode.system,
      home: WorkspaceShell(
        loadReadiness: LoadReadiness(readiness),
        refreshReadiness: RefreshReadiness(readiness),
        loadDiagnostics: LoadDiagnostics(diagnostics),
      ),
    );
  }
}
