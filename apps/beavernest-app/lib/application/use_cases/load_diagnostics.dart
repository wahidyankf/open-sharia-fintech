import 'package:beavernest_app/application/ports/diagnostics_repository.dart';
import 'package:beavernest_app/domain/diagnostics.dart';

/// Retrieves safe diagnostics for an explicit user request.
final class LoadDiagnostics {
  const LoadDiagnostics(this._repository);

  final DiagnosticsRepository _repository;

  Future<WorkspaceDiagnostics> call() => _repository.loadDiagnostics();
}
