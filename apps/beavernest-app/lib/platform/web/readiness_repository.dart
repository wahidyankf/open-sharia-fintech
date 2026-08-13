import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/platform/web/readiness_client.dart';
import 'package:http/http.dart' as http;

/// Maps the Web transport contract to the application's safe readiness model.
final class HttpReadinessRepository implements ReadinessRepository {
  HttpReadinessRepository({ReadinessClient? client})
    : _client = client ?? ReadinessClient(http.Client());

  final ReadinessClient _client;

  @override
  Future<WorkspaceReadiness> loadReadiness() async {
    final response = await _client.getReadiness();
    return switch (response) {
      ReadyReadiness(:final value) => WorkspaceReadiness(
        availability: ReadinessAvailability.ready,
        database: _databaseFromReady(value.components.database),
        schema: _schemaFromReady(value.components.schema),
      ),
      UnavailableReadiness(:final value) => WorkspaceReadiness(
        availability: ReadinessAvailability.unavailable,
        database: _databaseFromUnavailable(value.components.database),
        schema: _schemaFromUnavailable(value.components.schema),
      ),
    };
  }
}

DatabaseReadiness _databaseFromReady(String value) {
  if (value == 'ready') {
    return DatabaseReadiness.ready;
  }
  throw FormatException('Unsupported ready database state: $value');
}

SchemaReadiness _schemaFromReady(String value) {
  if (value == 'current') {
    return SchemaReadiness.current;
  }
  throw FormatException('Unsupported ready schema state: $value');
}

DatabaseReadiness _databaseFromUnavailable(String value) {
  if (value == 'unavailable') {
    return DatabaseReadiness.unavailable;
  }
  throw FormatException('Unsupported unavailable database state: $value');
}

SchemaReadiness _schemaFromUnavailable(String value) {
  if (value == 'unknown') {
    return SchemaReadiness.unknown;
  }
  throw FormatException('Unsupported unavailable schema state: $value');
}
