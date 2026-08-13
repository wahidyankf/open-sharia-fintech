import 'package:beavernest_app/domain/diagnostics.dart';

/// Loads the diagnostic snapshot through the current platform adapter.
abstract interface class DiagnosticsRepository {
  Future<WorkspaceDiagnostics> loadDiagnostics();
}
