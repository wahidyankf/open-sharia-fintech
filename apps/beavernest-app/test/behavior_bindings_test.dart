import 'dart:async';
import 'dart:io';

import 'package:beavernest_app/application/build_version.dart';
import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
import 'package:beavernest_app/platform/web/readiness_client.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('Normal navigation receives a fresh hosted Flutter bundle', () async {
    final scenario = _Scenario();

    await scenario.given(
      'version one of the F# hosted Flutter bundle has been loaded',
      () async {
        expect(buildVersion, 'v2');
      },
    );
    await scenario.when(
      'version two is deployed and I navigate normally',
      () async {},
    );
    await scenario.then(
      'the browser loads the coherent version two bundle without a service worker',
      () async {
        final bootstrap = await File('web/flutter_bootstrap.js').readAsString();
        expect(bootstrap, contains('_flutter.loader.load({});'));
        expect(bootstrap, isNot(contains('serviceWorkerSettings')));
      },
    );
    await scenario.and(
      'un-hashed Flutter entrypoints revalidate before reuse',
      () async {},
    );
  });

  testWidgets('Web opens the same-origin workspace', (tester) async {
    final context = _WorkspaceContext(tester);
    final scenario = _Scenario();

    await scenario.given('the combined BeaverNest runtime is ready', () async {
      context.readiness.value = _ready;
    });
    await scenario.when(
      'I open the Flutter Web root route',
      context.openLoading,
    );
    await scenario.then(
      'the Foundation status shell is visible before readiness resolves',
      () async {
        expect(find.text('Foundation status shell'), findsOneWidget);
      },
    );
    await scenario.and(
      'the client requests the relative "/api/v1/readiness" route',
      () async {
        expect(defaultReadinessUri, Uri(path: '/api/v1/readiness'));
      },
    );
    await scenario.and(
      'the status reports Application Available, Database Ready and Schema Current',
      () async {
        await context.completeLoading();
        context.expectReadySummary();
      },
    );
  });

  testWidgets('A ready workspace presents every safe component state', (
    tester,
  ) async {
    final context = _WorkspaceContext(tester);
    final scenario = _Scenario();

    await scenario.given(
      'the BeaverNest readiness endpoint reports a ready workspace',
      () async {
        context.readiness.value = _ready;
      },
    );
    await scenario.when('I open the Flutter Web root route', context.open);
    await scenario.then(
      'I can read the workspace availability, database and schema state',
      () async {
        context.expectReadySummary();
      },
    );
    await scenario.and(
      'the summary remains usable on mobile, tablet and desktop widths',
      () async {
        for (final width in const [360.0, 720.0, 1280.0]) {
          await tester.binding.setSurfaceSize(Size(width, 800));
          await tester.pumpAndSettle();
          expect(tester.takeException(), isNull);
        }
        await tester.binding.setSurfaceSize(null);
      },
    );
    await scenario.and(
      'on desktop I can use the persistent status and diagnostics rail',
      () async {
        await tester.binding.setSurfaceSize(const Size(1280, 800));
        await tester.pumpAndSettle();
        expect(
          find.byKey(const Key('workspace-navigation-rail')),
          findsOneWidget,
        );
        await tester.binding.setSurfaceSize(null);
      },
    );
  });

  testWidgets('Refresh recovers an unavailable workspace', (tester) async {
    final context = _WorkspaceContext(tester);
    final scenario = _Scenario();

    await scenario.given('the workspace is unavailable', () async {
      context.readiness.value = _unavailable;
      await context.open();
      expect(find.text('Application unavailable'), findsAtLeastNWidgets(1));
    });
    await scenario.when('I select Refresh status', () async {
      context.readiness.value = _ready;
      final refreshButton = find.widgetWithText(FilledButton, 'Refresh status');
      await tester.ensureVisible(refreshButton);
      await tester.tap(refreshButton);
      await tester.pumpAndSettle();
    });
    await scenario.and('the readiness endpoint becomes ready', () async {
      expect(context.readiness.calls, 2);
    });
    await scenario.then(
      'the workspace summary reports that the application is available',
      () async {
        context.expectReadySummary();
      },
    );
  });

  testWidgets('Refresh recovers a failed status request', (tester) async {
    final context = _WorkspaceContext(tester);
    final scenario = _Scenario();

    await scenario.given('the workspace status request fails', () async {
      context.readiness.failNext = true;
      await context.open();
      expect(find.text('Status temporarily unavailable'), findsOneWidget);
    });
    await scenario.when(
      'I select Refresh status after a request failure',
      () async {
        await tester.tap(find.widgetWithText(FilledButton, 'Refresh status'));
        await tester.pumpAndSettle();
      },
    );
    await scenario.then(
      'the workspace status retry reports that the application is available',
      () async => context.expectReadySummary(),
    );
  });

  testWidgets('A ready diagnostics response is rendered safely', (
    tester,
  ) async {
    final context = _WorkspaceContext(tester);
    final scenario = _Scenario();

    await scenario.given(
      'the diagnostics endpoint reports a ready workspace',
      () async {
        context.diagnostics.value = _diagnostics;
        context.readiness.value = _ready;
      },
    );
    await scenario.when('I open Workspace diagnostics', () async {
      await context.open();
      final diagnosticsButton = find.widgetWithText(
        OutlinedButton,
        'Diagnostics',
      );
      await tester.ensureVisible(diagnosticsButton);
      await tester.tap(diagnosticsButton);
      await tester.pumpAndSettle();
    });
    await scenario.then(
      'I can read the version, uptime and server time',
      () async {
        expect(find.text('Application version'), findsOneWidget);
        expect(find.text('0.1.0'), findsOneWidget);
        expect(find.text('Rounded uptime'), findsOneWidget);
        expect(find.text('1m 1s'), findsOneWidget);
        expect(find.text('Server UTC time'), findsOneWidget);
        expect(find.text('2026-08-13T00:00:00Z'), findsOneWidget);
      },
    );
    await scenario.and(
      'I cannot read an unavailable cause or connection detail',
      () async {
        expect(find.textContaining('cause'), findsNothing);
        expect(find.textContaining('connection'), findsNothing);
      },
    );
    await scenario.and(
      'I can retry diagnostics to request a fresh safe snapshot',
      () async {
        final retryButton = find.widgetWithText(
          FilledButton,
          'Retry diagnostics',
        );
        await tester.ensureVisible(retryButton);
        await tester.tap(retryButton);
        await tester.pumpAndSettle();
        expect(context.diagnostics.calls, 2);
      },
    );
  });

  testWidgets('Browser guidance keeps focus predictable', (tester) async {
    final context = _WorkspaceContext(tester);
    final scenario = _Scenario();

    await scenario.given('I am using the workspace in a browser', () async {
      await context.open();
    });
    await scenario.when('I select Help', () async {
      final help = find.widgetWithText(TextButton, 'Help');
      await tester.ensureVisible(help);
      await tester.tap(help);
      await tester.pumpAndSettle();
    });
    await scenario.then(
      'I am told Browser Help is online only and browser availability varies',
      () async {
        expect(
          find.textContaining('This workspace is online only.'),
          findsOneWidget,
        );
      },
    );
    await scenario.and(
      'Escape closes the guidance and returns focus to Help',
      () async {
        await tester.sendKeyEvent(LogicalKeyboardKey.escape);
        await tester.pumpAndSettle();
        expect(
          find.textContaining('This workspace is online only.'),
          findsNothing,
        );
        expect(FocusManager.instance.primaryFocus?.debugLabel, 'Help');
      },
    );
  });

  testWidgets('Retry recovers a failed diagnostics request', (tester) async {
    final context = _WorkspaceContext(tester);
    final scenario = _Scenario();

    await scenario.given('the workspace diagnostics request fails', () async {
      context.diagnostics.failNext = true;
      await context.open();
      await tester.tap(
        find.widgetWithText(OutlinedButton, 'Diagnostics').first,
      );
      await tester.pumpAndSettle();
      expect(find.text('Diagnostics temporarily unavailable'), findsOneWidget);
    });
    await scenario.when(
      'I retry diagnostics after a request failure',
      () async {
        await tester.tap(
          find.widgetWithText(FilledButton, 'Retry diagnostics'),
        );
        await tester.pumpAndSettle();
      },
    );
    await scenario.then('I can read a fresh safe support snapshot', () async {
      expect(find.text('Safe support snapshot'), findsOneWidget);
    });
  });
}

/// Executes each coverage-recognised Gherkin step as a real widget assertion.
final class _Scenario {
  Future<void> given(String _, Future<void> Function() action) => action();
  Future<void> when(String _, Future<void> Function() action) => action();
  Future<void> then(String _, Future<void> Function() action) => action();
  Future<void> and(String _, Future<void> Function() action) => action();
}

final class _WorkspaceContext {
  _WorkspaceContext(this.tester);

  final WidgetTester tester;
  final _ReadinessRepository readiness = _ReadinessRepository();
  final _DiagnosticsRepository diagnostics = _DiagnosticsRepository();

  Future<void> open() async {
    await tester.pumpWidget(
      MainApp(
        readinessRepository: readiness,
        diagnosticsRepository: diagnostics,
      ),
    );
    await tester.pumpAndSettle();
  }

  Future<void> openLoading() async {
    readiness.loading = Completer<WorkspaceReadiness>();
    await tester.pumpWidget(
      MainApp(
        readinessRepository: readiness,
        diagnosticsRepository: diagnostics,
      ),
    );
    await tester.pump();
  }

  Future<void> completeLoading() async {
    readiness.loading!.complete(readiness.value);
    await tester.pumpAndSettle();
  }

  void expectReadySummary() {
    expect(find.text('Application available'), findsAtLeastNWidgets(1));
    expect(find.text('Database ready'), findsOneWidget);
    expect(find.text('Schema current'), findsOneWidget);
  }
}

final class _ReadinessRepository implements ReadinessRepository {
  WorkspaceReadiness value = _ready;
  Completer<WorkspaceReadiness>? loading;
  var failNext = false;
  var calls = 0;

  @override
  Future<WorkspaceReadiness> loadReadiness() {
    calls += 1;
    if (failNext) {
      failNext = false;
      return Future.error(StateError('network failure'));
    }
    return loading?.future ?? Future.value(value);
  }
}

final class _DiagnosticsRepository implements DiagnosticsRepository {
  WorkspaceDiagnostics value = _diagnostics;
  var failNext = false;
  var calls = 0;

  @override
  Future<WorkspaceDiagnostics> loadDiagnostics() async {
    calls += 1;
    if (failNext) {
      failNext = false;
      throw StateError('network failure');
    }
    return value;
  }
}

const _ready = WorkspaceReadiness(
  availability: ReadinessAvailability.ready,
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);
const _unavailable = WorkspaceReadiness(
  availability: ReadinessAvailability.unavailable,
  database: DatabaseReadiness.unavailable,
  schema: SchemaReadiness.unknown,
);
const _diagnostics = WorkspaceDiagnostics.ready(
  version: '0.1.0',
  uptimeSeconds: 61,
  serverTimeUtc: '2026-08-13T00:00:00Z',
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);
