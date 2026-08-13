import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/application/use_cases/load_readiness.dart';
import 'package:beavernest_app/platform/web/readiness_repository.dart';
import 'package:beavernest_app/presentation/workspace_shell.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key, this.readinessRepository});

  final ReadinessRepository? readinessRepository;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: WorkspaceShell(
        loadReadiness: LoadReadiness(
          readinessRepository ?? HttpReadinessRepository(),
        ),
      ),
    );
  }
}
