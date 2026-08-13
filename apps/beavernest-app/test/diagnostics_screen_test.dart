import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('renders a scannable safe diagnostics workspace and retries', (
    tester,
  ) async {
    final diagnostics = _DiagnosticsRepository(_diagnostics);
    await tester.pumpWidget(
      MainApp(
        readinessRepository: const _ReadinessRepository(_ready),
        diagnosticsRepository: diagnostics,
      ),
    );
    await tester.pumpAndSettle();
    final diagnosticsButton = find.widgetWithText(
      OutlinedButton,
      'Diagnostics',
    );
    await tester.ensureVisible(diagnosticsButton);
    await tester.tap(diagnosticsButton);
    await tester.pumpAndSettle();

    expect(find.text('Diagnostics'), findsOneWidget);
    expect(find.text('Safe support snapshot'), findsOneWidget);
    expect(find.text('Application version'), findsOneWidget);
    expect(find.text('0.1.0'), findsOneWidget);
    expect(find.text('Rounded uptime'), findsOneWidget);
    expect(find.text('1m 1s'), findsOneWidget);
    expect(find.text('Server UTC time'), findsOneWidget);
    expect(find.text('2026-08-13T00:00:00Z'), findsOneWidget);
    expect(find.text('Retry diagnostics'), findsOneWidget);
    expect(find.textContaining('cause'), findsNothing);

    final retryButton = find.widgetWithText(FilledButton, 'Retry diagnostics');
    await tester.ensureVisible(retryButton);
    await tester.tap(retryButton);
    await tester.pumpAndSettle();
    expect(diagnostics.calls, 2);
  });

  for (final width in const [768.0, 1280.0]) {
    testWidgets(
      'renders compact support cards and readiness badges at $width pixels',
      (tester) async {
        await tester.binding.setSurfaceSize(Size(width, 900));
        addTearDown(() => tester.binding.setSurfaceSize(null));

        await tester.pumpWidget(
          MainApp(
            readinessRepository: const _ReadinessRepository(_ready),
            diagnosticsRepository: _DiagnosticsRepository(_diagnostics),
          ),
        );
        await tester.pumpAndSettle();
        await tester.tap(
          find.widgetWithText(OutlinedButton, 'Diagnostics').first,
        );
        await tester.pumpAndSettle();

        expect(find.text('Application version'), findsOneWidget);
        expect(find.text('Rounded uptime'), findsOneWidget);
        expect(find.text('Server UTC time'), findsOneWidget);
        expect(find.text('Readiness components'), findsOneWidget);
        expect(find.text('Application available'), findsOneWidget);
        expect(find.text('Database ready'), findsOneWidget);
        expect(find.text('Schema current'), findsOneWidget);
        expect(find.text('Ready'), findsNWidgets(2));
        expect(find.text('Current'), findsOneWidget);
        expect(find.byIcon(Icons.code), findsOneWidget);
        expect(find.byIcon(Icons.schedule), findsOneWidget);
      },
    );
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
  _DiagnosticsRepository(this.value);
  final WorkspaceDiagnostics value;
  var calls = 0;
  @override
  Future<WorkspaceDiagnostics> loadDiagnostics() async {
    calls += 1;
    return value;
  }
}
