import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('renders only safe ready diagnostics', (tester) async {
    await tester.pumpWidget(
      MainApp(
        readinessRepository: const _ReadinessRepository(_ready),
        diagnosticsRepository: const _DiagnosticsRepository(_diagnostics),
      ),
    );
    await tester.pumpAndSettle();
    await tester.tap(find.bySemanticsLabel('Open workspace diagnostics'));
    await tester.pumpAndSettle();

    expect(find.text('Workspace diagnostics'), findsOneWidget);
    expect(find.text('Version 0.1.0'), findsOneWidget);
    expect(find.text('Uptime 1m 1s'), findsOneWidget);
    expect(find.text('Server time 2026-08-13T00:00:00Z'), findsOneWidget);
    expect(find.textContaining('cause'), findsNothing);
  });
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
