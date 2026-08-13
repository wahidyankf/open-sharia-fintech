import 'dart:convert';

import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/application/use_cases/load_readiness.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/platform/web/readiness_client.dart';
import 'package:beavernest_app/platform/web/readiness_repository.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;

void main() {
  test('loads readiness through the repository port', () async {
    final repository = _FakeReadinessRepository(_readyReadiness);

    final readiness = await LoadReadiness(repository).call();

    expect(readiness, _readyReadiness);
    expect(repository.calls, 1);
  });

  test('maps the ready transport variant inside the Web adapter', () async {
    final repository = HttpReadinessRepository(
      client: ReadinessClient(_JsonClient(_readyPayload, 200)),
    );

    final readiness = await repository.loadReadiness();

    expect(readiness.availability, ReadinessAvailability.ready);
    expect(readiness.database, DatabaseReadiness.ready);
    expect(readiness.schema, SchemaReadiness.current);
  });

  test(
    'maps the unavailable transport variant inside the Web adapter',
    () async {
      final repository = HttpReadinessRepository(
        client: ReadinessClient(_JsonClient(_unavailablePayload, 503)),
      );

      final readiness = await repository.loadReadiness();

      expect(readiness.availability, ReadinessAvailability.unavailable);
      expect(readiness.database, DatabaseReadiness.unavailable);
      expect(readiness.schema, SchemaReadiness.unknown);
    },
  );
}

const _readyReadiness = WorkspaceReadiness(
  availability: ReadinessAvailability.ready,
  database: DatabaseReadiness.ready,
  schema: SchemaReadiness.current,
);

const _readyPayload = {
  'status': 'ready',
  'components': {'database': 'ready', 'schema': 'current'},
};

const _unavailablePayload = {
  'status': 'not-ready',
  'components': {'database': 'unavailable', 'schema': 'unknown'},
};

final class _FakeReadinessRepository implements ReadinessRepository {
  _FakeReadinessRepository(this._readiness);

  final WorkspaceReadiness _readiness;
  var calls = 0;

  @override
  Future<WorkspaceReadiness> loadReadiness() async {
    calls += 1;
    return _readiness;
  }
}

final class _JsonClient extends http.BaseClient {
  _JsonClient(this._payload, this._statusCode);

  final Object _payload;
  final int _statusCode;

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async =>
      http.StreamedResponse(
        Stream.value(utf8.encode(jsonEncode(_payload))),
        _statusCode,
        request: request,
      );
}
