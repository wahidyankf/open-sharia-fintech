import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('refresh retries readiness and reports recovery', (tester) async {
    final readiness = _SequenceReadinessRepository([_unavailable, _ready]);

    await tester.pumpWidget(
      MainApp(
        readinessRepository: readiness,
        diagnosticsRepository: const _DiagnosticsRepository(_diagnostics),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Application unavailable'), findsAtLeastNWidgets(1));
    final refreshButton = find.widgetWithText(FilledButton, 'Refresh status');
    await tester.ensureVisible(refreshButton);
    await tester.tap(refreshButton);
    await tester.pumpAndSettle();

    expect(readiness.calls, 2);
    expect(find.text('Application available'), findsAtLeastNWidgets(1));
    expect(find.text('Foundation status'), findsOneWidget);
  });
}

const _unavailable = WorkspaceReadiness(
  availability: ReadinessAvailability.unavailable,
  database: DatabaseReadiness.unavailable,
  schema: SchemaReadiness.unknown,
);
const _ready = WorkspaceReadiness(
  availability: ReadinessAvailability.ready,
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);
const _diagnostics = WorkspaceDiagnostics.unavailable(
  database: DatabaseReadiness.unavailable,
  schema: SchemaReadiness.unknown,
);

final class _SequenceReadinessRepository implements ReadinessRepository {
  _SequenceReadinessRepository(this._values);
  final List<WorkspaceReadiness> _values;
  var calls = 0;
  @override
  Future<WorkspaceReadiness> loadReadiness() async => _values[calls++];
}

final class _DiagnosticsRepository implements DiagnosticsRepository {
  const _DiagnosticsRepository(this.value);
  final WorkspaceDiagnostics value;
  @override
  Future<WorkspaceDiagnostics> loadDiagnostics() async => value;
}
