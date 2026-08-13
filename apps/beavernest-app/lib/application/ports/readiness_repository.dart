import 'package:beavernest_app/domain/readiness.dart';

/// Loads the safe readiness state from the current platform adapter.
abstract interface class ReadinessRepository {
  Future<WorkspaceReadiness> loadReadiness();
}
