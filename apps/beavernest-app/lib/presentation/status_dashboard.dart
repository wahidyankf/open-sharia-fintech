import 'package:beavernest_app/application/build_version.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/presentation/workspace_theme.dart';
import 'package:flutter/material.dart';

/// Responsive, at-a-glance status dashboard with semantic state cues.
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
      label: 'Foundation status: $availability',
      liveRegion: true,
      child: LayoutBuilder(
        builder: (context, constraints) {
          final columns = constraints.maxWidth >= 800
              ? 3
              : constraints.maxWidth >= 560
              ? 2
              : 1;
          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'BEAVERNEST / FOUNDATION',
                style: Theme.of(context).textTheme.labelLarge,
              ),
              const SizedBox(height: 4),
              Row(
                children: [
                  Expanded(
                    child: Semantics(
                      header: true,
                      child: Text(
                        'Foundation status',
                        style: Theme.of(context).textTheme.headlineMedium,
                      ),
                    ),
                  ),
                  Text('Build $buildVersion'),
                ],
              ),
              const SizedBox(height: 6),
              Text(
                'Operational overview of core foundation services.',
                style: Theme.of(context).textTheme.bodyLarge,
              ),
              const SizedBox(height: 12),
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
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: [
                  for (final card in [
                    _StateCard(
                      label: 'Application',
                      state: availability,
                      description: ready
                          ? 'BeaverNest application is reachable and responding.'
                          : 'BeaverNest application is unavailable. Refresh status to retry.',
                      icon: ready ? Icons.check_circle : Icons.error_outline,
                      color: colour,
                    ),
                    _StateCard(
                      label: 'Database',
                      state: readiness.database.name,
                      description: readiness.database == DatabaseReadiness.ready
                          ? 'Database connection established and healthy.'
                          : 'Database connection is unavailable. Refresh status to retry.',
                      icon: Icons.storage_outlined,
                      color: readiness.database == DatabaseReadiness.ready
                          ? colors.available
                          : colors.unavailable,
                    ),
                    _StateCard(
                      label: 'Schema',
                      state: readiness.schema.name,
                      description: readiness.schema == SchemaReadiness.current
                          ? 'Database schema is up to date.'
                          : 'Database schema needs attention before it is current.',
                      icon: Icons.layers_outlined,
                      color: readiness.schema == SchemaReadiness.current
                          ? colors.available
                          : colors.unavailable,
                    ),
                  ])
                    SizedBox(
                      width:
                          (constraints.maxWidth - (12 * (columns - 1))) /
                          columns,
                      child: card,
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
    required this.state,
    required this.description,
    required this.icon,
    required this.color,
  });
  final String label;
  final String state;
  final String description;
  final IconData icon;
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
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              _StatusIcon(icon: icon, color: color),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  '$label $state',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
              ),
              const SizedBox(width: 8),
              _StateBadge(label: _titleCase(state), color: color),
            ],
          ),
          const SizedBox(height: 12),
          Text(description, style: Theme.of(context).textTheme.bodyMedium),
        ],
      ),
    ),
  );
}

final class _StatusIcon extends StatelessWidget {
  const _StatusIcon({required this.icon, required this.color});
  final IconData icon;
  final Color color;

  @override
  Widget build(BuildContext context) => DecoratedBox(
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.16),
      shape: BoxShape.circle,
    ),
    child: SizedBox(width: 44, height: 44, child: Icon(icon, color: color)),
  );
}

final class _StateBadge extends StatelessWidget {
  const _StateBadge({required this.label, required this.color});
  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) => DecoratedBox(
    decoration: BoxDecoration(
      color: color.withValues(alpha: 0.14),
      borderRadius: BorderRadius.circular(6),
    ),
    child: Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      child: Text(
        label,
        style: Theme.of(context).textTheme.labelLarge?.copyWith(color: color),
      ),
    ),
  );
}

String _titleCase(String value) =>
    '${value[0].toUpperCase()}${value.substring(1)}';
