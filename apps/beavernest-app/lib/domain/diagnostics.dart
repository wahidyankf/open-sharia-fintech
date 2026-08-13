import 'package:beavernest_app/domain/readiness.dart';

/// A deliberately small operational snapshot safe to display in the workspace.
final class WorkspaceDiagnostics {
  const WorkspaceDiagnostics.ready({
    required this.version,
    required this.uptimeSeconds,
    required this.serverTimeUtc,
    required this.database,
    required this.schema,
  }) : isAvailable = true;

  const WorkspaceDiagnostics.unavailable({
    required this.database,
    required this.schema,
  }) : isAvailable = false,
       version = null,
       uptimeSeconds = null,
       serverTimeUtc = null;

  final bool isAvailable;
  final String? version;
  final int? uptimeSeconds;
  final String? serverTimeUtc;
  final DatabaseReadiness database;
  final SchemaReadiness schema;
}
