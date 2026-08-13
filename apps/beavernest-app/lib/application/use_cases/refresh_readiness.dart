import 'package:beavernest_app/application/ports/readiness_repository.dart';
import 'package:beavernest_app/domain/readiness.dart';

/// Re-reads readiness after a user explicitly asks to retry.
final class RefreshReadiness {
  const RefreshReadiness(this._repository);

  final ReadinessRepository _repository;

  Future<WorkspaceReadiness> call() => _repository.loadReadiness();
}
