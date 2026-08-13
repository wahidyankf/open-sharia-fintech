import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Escape closes browser guidance and restores trigger focus', (
    tester,
  ) async {
    await tester.pumpWidget(
      MainApp(
        readinessRepository: const _ReadinessRepository(_ready),
        diagnosticsRepository: const _DiagnosticsRepository(_diagnostics),
      ),
    );
    await tester.pumpAndSettle();

    final trigger = find.widgetWithText(TextButton, 'Browser shortcut');
    await tester.tap(trigger);
    await tester.pumpAndSettle();
    expect(find.text('Browser shortcut'), findsAtLeastNWidgets(1));
    expect(
      find.textContaining('This workspace is online only.'),
      findsOneWidget,
    );

    await tester.sendKeyEvent(LogicalKeyboardKey.escape);
    await tester.pumpAndSettle();
    expect(find.textContaining('This workspace is online only.'), findsNothing);
    expect(FocusManager.instance.primaryFocus?.debugLabel, 'Browser shortcut');
  });
}

const _ready = WorkspaceReadiness(
  availability: ReadinessAvailability.ready,
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);
const _diagnostics = WorkspaceDiagnostics.unavailable(
  database: DatabaseReadiness.unavailable,
  schema: SchemaReadiness.unknown,
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
