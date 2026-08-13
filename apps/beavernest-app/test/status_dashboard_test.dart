import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
import 'package:beavernest_app/presentation/status_dashboard.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  for (final width in const [360.0, 720.0, 1280.0]) {
    testWidgets('renders a readable dashboard at $width pixels', (
      tester,
    ) async {
      await tester.binding.setSurfaceSize(Size(width, 800));
      addTearDown(() => tester.binding.setSurfaceSize(null));

      await tester.pumpWidget(
        MainApp(
          readinessRepository: _ReadinessRepository(_ready),
          diagnosticsRepository: _DiagnosticsRepository(_diagnostics),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Workspace status'), findsOneWidget);
      expect(find.text('Application available'), findsAtLeastNWidgets(1));
      expect(find.text('Database ready'), findsOneWidget);
      expect(find.text('Schema current'), findsOneWidget);
      expect(find.byType(StatusDashboard), findsOneWidget);
      expect(tester.takeException(), isNull);
    });
  }
}

const _ready = WorkspaceReadiness(
  availability: ReadinessAvailability.ready,
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);

const _diagnostics = WorkspaceDiagnostics.ready(
  version: '0.1.0',
  uptimeSeconds: 61,
  serverTimeUtc: '2026-08-13T00:00:00Z',
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);

final class _ReadinessRepository implements ReadinessRepository {
  const _ReadinessRepository(this.value);
  final WorkspaceReadiness value;
  @override
  Future<WorkspaceReadiness> loadReadiness() async => value;
}

final class _DiagnosticsRepository implements DiagnosticsRepository {
  const _DiagnosticsRepository(this.value);
  final WorkspaceDiagnostics value;
  @override
  Future<WorkspaceDiagnostics> loadDiagnostics() async => value;
}
