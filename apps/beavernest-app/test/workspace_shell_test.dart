import 'dart:async';

import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/main.dart';
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

    expect(find.text('Application Available'), findsOneWidget);
    expect(find.text('Database Ready'), findsOneWidget);
    expect(find.text('Schema Current'), findsOneWidget);
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
