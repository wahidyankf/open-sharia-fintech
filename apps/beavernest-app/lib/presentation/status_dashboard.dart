import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/presentation/workspace_theme.dart';
import 'package:flutter/material.dart';

/// Responsive status dashboard with semantic state, rather than colour alone.
final class StatusDashboard extends StatelessWidget {
  const StatusDashboard({required this.readiness, super.key});
  final WorkspaceReadiness readiness;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).extension<WorkspaceStatusColors>()!;
    final ready = readiness.isReady;
    final colour = ready ? colors.available : colors.unavailable;
    final availability = ready ? 'available' : 'unavailable';
    return Semantics(
      label: 'Workspace status: $availability',
      liveRegion: true,
      child: LayoutBuilder(
        builder: (context, constraints) {
          final columns = constraints.maxWidth >= 920
              ? 3
              : constraints.maxWidth >= 560
              ? 2
              : 1;
          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Workspace status',
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  Icon(
                    ready ? Icons.check_circle : Icons.error_outline,
                    color: colour,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Application $availability',
                      style: Theme.of(
                        context,
                      ).textTheme.titleMedium?.copyWith(color: colour),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              GridView.count(
                crossAxisCount: columns,
                childAspectRatio: columns == 1 ? 2.8 : 2.35,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                mainAxisSpacing: 12,
                crossAxisSpacing: 12,
                children: [
                  _StateCard(
                    label: 'Application',
                    value: availability,
                    color: colour,
                  ),
                  _StateCard(
                    label: 'Database',
                    value: readiness.database.name,
                    color: readiness.database == DatabaseReadiness.ready
                        ? colors.available
                        : colors.unavailable,
                  ),
                  _StateCard(
                    label: 'Schema',
                    value: readiness.schema.name,
                    color: readiness.schema == SchemaReadiness.current
                        ? colors.available
                        : colors.unavailable,
                  ),
                ],
              ),
            ],
          );
        },
      ),
    );
  }
}

final class _StateCard extends StatelessWidget {
  const _StateCard({
    required this.label,
    required this.value,
    required this.color,
  });
  final String label;
  final String value;
  final Color color;

  @override
  Widget build(BuildContext context) => DecoratedBox(
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.10),
      border: Border.all(color: color.withValues(alpha: 0.35)),
      borderRadius: BorderRadius.circular(12),
    ),
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(label, style: Theme.of(context).textTheme.labelLarge),
          const SizedBox(height: 4),
          Text(
            '$label $value',
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(color: color),
          ),
        ],
      ),
    ),
  );
}
