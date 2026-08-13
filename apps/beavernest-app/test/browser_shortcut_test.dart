import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets(
    'Browser Help gives numbered online-only guidance and restores focus',
    (tester) async {
      await tester.pumpWidget(
        MainApp(
          readinessRepository: const _ReadinessRepository(_ready),
          diagnosticsRepository: const _DiagnosticsRepository(_diagnostics),
        ),
      );
      await tester.pumpAndSettle();

      final trigger = find.widgetWithText(TextButton, 'Help');
      await tester.ensureVisible(trigger);
      await tester.tap(trigger);
      await tester.pumpAndSettle();
      expect(find.byType(AlertDialog), findsOneWidget);
      expect(find.text('Browser Help'), findsAtLeastNWidgets(1));
      expect(
        find.textContaining('This workspace is online only.'),
        findsOneWidget,
      );
      expect(find.text('1. Open your browser menu.'), findsOneWidget);
      expect(
        find.text('2. Choose an available shortcut or install action.'),
        findsOneWidget,
      );
      expect(
        find.text('3. Confirm the browser prompt if one appears.'),
        findsOneWidget,
      );
      expect(find.text('Close Help'), findsOneWidget);

      await tester.sendKeyEvent(LogicalKeyboardKey.escape);
      await tester.pumpAndSettle();
      expect(
        find.textContaining('This workspace is online only.'),
        findsNothing,
      );
      expect(FocusManager.instance.primaryFocus?.debugLabel, 'Help');
    },
  );
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
