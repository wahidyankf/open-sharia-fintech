import 'dart:async';

import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('loads readiness through LoadReadiness from the root shell', (
    tester,
  ) async {
    final repository = _ControllableReadinessRepository();

    await tester.pumpWidget(MainApp(readinessRepository: repository));

    expect(find.text('Foundation status shell'), findsOneWidget);
    expect(repository.calls, 1);

    repository.complete(_readyReadiness);
    await tester.pumpAndSettle();

    expect(find.text('Application available'), findsAtLeastNWidgets(1));
    expect(find.text('Database ready'), findsOneWidget);
    expect(find.text('Schema current'), findsOneWidget);
  });

  testWidgets('uses a persistent status and diagnostics rail on desktop', (
    tester,
  ) async {
    await tester.binding.setSurfaceSize(const Size(1280, 800));
    addTearDown(() => tester.binding.setSurfaceSize(null));

    await tester.pumpWidget(
      const MainApp(
        readinessRepository: _ReadyReadinessRepository(),
        diagnosticsRepository: _ReadyDiagnosticsRepository(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.byKey(const Key('workspace-navigation-rail')), findsOneWidget);
    expect(find.text('BeaverNest'), findsOneWidget);
    expect(find.text('Foundation status'), findsOneWidget);
    expect(find.widgetWithText(OutlinedButton, 'Diagnostics'), findsOneWidget);
  });

  testWidgets(
    'starts the persistent desktop rail at the 1024 pixel breakpoint',
    (tester) async {
      await tester.binding.setSurfaceSize(const Size(1024, 800));
      addTearDown(() => tester.binding.setSurfaceSize(null));

      await tester.pumpWidget(
        const MainApp(
          readinessRepository: _ReadyReadinessRepository(),
          diagnosticsRepository: _ReadyDiagnosticsRepository(),
        ),
      );
      await tester.pumpAndSettle();

      expect(
        find.byKey(const Key('workspace-navigation-rail')),
        findsOneWidget,
      );
    },
  );

  testWidgets('offers an in-place readiness retry after a transport failure', (
    tester,
  ) async {
    final repository = _FailThenReadyReadinessRepository();
    await tester.pumpWidget(MainApp(readinessRepository: repository));
    await tester.pumpAndSettle();

    expect(find.text('Status temporarily unavailable'), findsOneWidget);
    final retry = find.widgetWithText(FilledButton, 'Refresh status');
    await tester.tap(retry);
    await tester.pumpAndSettle();

    expect(repository.calls, 2);
    expect(find.text('Application available'), findsAtLeastNWidgets(1));
  });
}

const _readyReadiness = WorkspaceReadiness(
  availability: ReadinessAvailability.ready,
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);

final class _ControllableReadinessRepository implements ReadinessRepository {
  final _result = Completer<WorkspaceReadiness>();
  var calls = 0;

  @override
  Future<WorkspaceReadiness> loadReadiness() {
    calls += 1;
    return _result.future;
  }

  void complete(WorkspaceReadiness readiness) => _result.complete(readiness);
}

final class _ReadyReadinessRepository implements ReadinessRepository {
  const _ReadyReadinessRepository();

  @override
  Future<WorkspaceReadiness> loadReadiness() async => _readyReadiness;
}

final class _FailThenReadyReadinessRepository implements ReadinessRepository {
  var calls = 0;

  @override
  Future<WorkspaceReadiness> loadReadiness() {
    calls += 1;
    if (calls == 1) return Future.error(StateError('network failure'));
    return Future.value(_readyReadiness);
  }
}

final class _ReadyDiagnosticsRepository implements DiagnosticsRepository {
  const _ReadyDiagnosticsRepository();

  @override
  Future<WorkspaceDiagnostics> loadDiagnostics() async => _diagnostics;
}

const _diagnostics = WorkspaceDiagnostics.ready(
  version: '0.1.0',
  uptimeSeconds: 61,
  serverTimeUtc: '2026-08-13T00:00:00Z',
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);
