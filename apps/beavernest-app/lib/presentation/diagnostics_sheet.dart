import 'package:beavernest_app/application/use_cases/load_diagnostics.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:flutter/material.dart';

/// An in-workspace safe support snapshot, never a hidden failure cause.
final class DiagnosticsWorkspace extends StatefulWidget {
  const DiagnosticsWorkspace({
    required this.loadDiagnostics,
    required this.onStatus,
    super.key,
  });

  final LoadDiagnostics loadDiagnostics;
  final VoidCallback onStatus;

  @override
  State<DiagnosticsWorkspace> createState() => _DiagnosticsWorkspaceState();
}

final class _DiagnosticsWorkspaceState extends State<DiagnosticsWorkspace> {
  late Future<WorkspaceDiagnostics> _diagnostics;

  @override
  void initState() {
    super.initState();
    _diagnostics = widget.loadDiagnostics();
  }

  void _retry() {
    setState(() {
      _diagnostics = widget.loadDiagnostics();
    });
  }

  @override
  Widget build(BuildContext context) => FutureBuilder<WorkspaceDiagnostics>(
    future: _diagnostics,
    builder: (context, snapshot) {
      if (!snapshot.hasData) {
        return Semantics(
          label: 'Diagnostics loading',
          liveRegion: true,
          child: Center(child: CircularProgressIndicator()),
        );
      }
      return _DiagnosticsDetails(
        value: snapshot.requireData,
        onRetry: _retry,
        onStatus: widget.onStatus,
      );
    },
  );
}

final class _DiagnosticsDetails extends StatelessWidget {
  const _DiagnosticsDetails({
    required this.value,
    required this.onRetry,
    required this.onStatus,
  });
  final WorkspaceDiagnostics value;
  final VoidCallback onRetry;
  final VoidCallback onStatus;

  @override
  Widget build(BuildContext context) => Semantics(
    label: 'Workspace diagnostics',
    liveRegion: true,
    child: FocusTraversalGroup(
      policy: OrderedTraversalPolicy(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'BEAVERNEST / SUPPORT',
            style: Theme.of(context).textTheme.labelLarge,
          ),
          const SizedBox(height: 4),
          Semantics(
            header: true,
            child: Text(
              'Diagnostics',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Safe support snapshot',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 20),
          if (value.isAvailable)
            _AvailableDiagnostics(value: value)
          else
            const _UnavailableDiagnostics(),
          const SizedBox(height: 24),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: [
              SizedBox(
                height: 44,
                child: FilledButton.icon(
                  onPressed: onRetry,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Retry diagnostics'),
                ),
              ),
              SizedBox(
                height: 44,
                child: OutlinedButton.icon(
                  onPressed: onStatus,
                  icon: const Icon(Icons.arrow_back),
                  label: const Text('Status'),
                ),
              ),
            ],
          ),
        ],
      ),
    ),
  );
}

final class _AvailableDiagnostics extends StatelessWidget {
  const _AvailableDiagnostics({required this.value});
  final WorkspaceDiagnostics value;

  @override
  Widget build(BuildContext context) => LayoutBuilder(
    builder: (context, constraints) {
      final columns = constraints.maxWidth >= 800
          ? 3
          : constraints.maxWidth >= 560
          ? 2
          : 1;
      final metrics = [
        _SafeMetric(
          label: 'Application version',
          value: value.version!,
          description: 'Build identity',
          icon: Icons.code,
        ),
        _SafeMetric(
          label: 'Rounded uptime',
          value: _duration(value.uptimeSeconds!),
          description: 'Current service session',
          icon: Icons.schedule,
        ),
        _SafeMetric(
          label: 'Server UTC time',
          value: value.serverTimeUtc!,
          description: 'Safe snapshot timestamp',
          icon: Icons.calendar_today_outlined,
        ),
      ];
      return Column(
        children: [
          GridView.count(
            crossAxisCount: columns,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            mainAxisSpacing: 12,
            crossAxisSpacing: 12,
            childAspectRatio: columns == 1
                ? 3.4
                : columns == 2
                ? 1.25
                : 1.2,
            children: metrics.map(_SafeMetricCard.new).toList(),
          ),
          const SizedBox(height: 12),
          _ReadinessComponentsCard(value: value),
        ],
      );
    },
  );
}

final class _SafeMetric {
  const _SafeMetric({
    required this.label,
    required this.value,
    required this.description,
    required this.icon,
  });
  final String label;
  final String value;
  final String description;
  final IconData icon;
}

final class _SafeMetricCard extends StatelessWidget {
  const _SafeMetricCard(this.metric);
  final _SafeMetric metric;

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(metric.icon, color: Theme.of(context).colorScheme.primary),
          const SizedBox(height: 12),
          Text(metric.label, style: Theme.of(context).textTheme.titleSmall),
          const SizedBox(height: 8),
          Text(
            metric.value,
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            metric.description,
            style: Theme.of(context).textTheme.bodySmall,
          ),
        ],
      ),
    ),
  );
}

final class _ReadinessComponentsCard extends StatelessWidget {
  const _ReadinessComponentsCard({required this.value});
  final WorkspaceDiagnostics value;

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Readiness components',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 16),
          _ReadinessRow(label: 'Application available', state: 'Ready'),
          const SizedBox(height: 12),
          _ReadinessRow(
            label: 'Database ${value.database.name}',
            state: _titleCase(value.database.name),
          ),
          const SizedBox(height: 12),
          _ReadinessRow(
            label: 'Schema ${value.schema.name}',
            state: _titleCase(value.schema.name),
          ),
        ],
      ),
    ),
  );
}

final class _ReadinessRow extends StatelessWidget {
  const _ReadinessRow({required this.label, required this.state});
  final String label;
  final String state;

  @override
  Widget build(BuildContext context) {
    final available = state == 'Ready' || state == 'Current';
    final color = available
        ? Theme.of(context).colorScheme.primary
        : Theme.of(context).colorScheme.error;
    return Row(
      children: [
        Icon(
          available ? Icons.check_circle : Icons.error_outline,
          color: color,
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Text(label, style: Theme.of(context).textTheme.bodyLarge),
        ),
        _ReadinessBadge(label: state, color: color),
      ],
    );
  }
}

final class _ReadinessBadge extends StatelessWidget {
  const _ReadinessBadge({required this.label, required this.color});
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

final class _UnavailableDiagnostics extends StatelessWidget {
  const _UnavailableDiagnostics();

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(20),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            Icons.warning_amber_rounded,
            color: Theme.of(context).colorScheme.error,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Diagnostics unavailable',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 4),
                Text(
                  'Diagnostics are temporarily unavailable. Retry to request a fresh safe snapshot.',
                  style: Theme.of(context).textTheme.bodyLarge,
                ),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}

String _duration(int seconds) {
  final minutes = seconds ~/ 60;
  final remaining = seconds % 60;
  if (minutes == 0) return '${remaining}s';
  return '${minutes}m ${remaining}s';
}

String _titleCase(String value) =>
    '${value[0].toUpperCase()}${value.substring(1)}';
