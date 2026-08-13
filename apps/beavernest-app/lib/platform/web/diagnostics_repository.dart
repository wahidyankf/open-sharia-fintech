import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/platform/web/diagnostics_client.dart';
import 'package:http/http.dart' as http;

/// Maps the Web diagnostics response to the safe application model.
final class HttpDiagnosticsRepository implements DiagnosticsRepository {
  HttpDiagnosticsRepository({DiagnosticsClient? client})
    : _client = client ?? DiagnosticsClient(http.Client());

  final DiagnosticsClient _client;

  @override
  Future<WorkspaceDiagnostics> loadDiagnostics() async {
    final response = await _client.getDiagnostics();
    return switch (response) {
      ReadyDiagnostics(:final value) => WorkspaceDiagnostics.ready(
        version: value.version,
        uptimeSeconds: value.uptimeSeconds,
        serverTimeUtc: value.serverTimeUtc,
        database: _readyDatabase(value.components.database),
        schema: _readySchema(value.components.schema),
      ),
      UnavailableDiagnostics(:final value) => WorkspaceDiagnostics.unavailable(
        database: _unavailableDatabase(value.components.database),
        schema: _unavailableSchema(value.components.schema),
      ),
    };
  }
}

DatabaseReadiness _readyDatabase(String value) => value == 'ready'
    ? DatabaseReadiness.ready
    : throw FormatException('Unsupported ready database state: $value');

SchemaReadiness _readySchema(String value) => value == 'current'
    ? SchemaReadiness.current
    : throw FormatException('Unsupported ready schema state: $value');

DatabaseReadiness _unavailableDatabase(String value) => value == 'unavailable'
    ? DatabaseReadiness.unavailable
    : throw FormatException('Unsupported unavailable database state: $value');

SchemaReadiness _unavailableSchema(String value) => value == 'unknown'
    ? SchemaReadiness.unknown
    : throw FormatException('Unsupported unavailable schema state: $value');
