import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/readiness.dart';

/// Retrieves the readiness state required by the workspace shell.
final class LoadReadiness {
  const LoadReadiness(this._repository);

  final ReadinessRepository _repository;

  Future<WorkspaceReadiness> call() => _repository.loadReadiness();
}
