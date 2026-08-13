/// The safe availability states reported by the BeaverNest runtime.
enum ReadinessAvailability { ready, unavailable }

/// The safe database states declared by the readiness contract.
enum DatabaseReadiness { ready, unavailable }

/// The safe schema states declared by the readiness contract.
enum SchemaReadiness { current, unknown }

/// Immutable readiness information that the workspace may render.
final class WorkspaceReadiness {
  const WorkspaceReadiness({
    required this.availability,
    required this.database,
    required this.schema,
  });

  final ReadinessAvailability availability;
  final DatabaseReadiness database;
  final SchemaReadiness schema;

  bool get isReady => availability == ReadinessAvailability.ready;
}
