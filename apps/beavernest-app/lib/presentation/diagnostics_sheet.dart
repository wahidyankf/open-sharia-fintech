import 'package:beavernest_app/application/use_cases/load_diagnostics.dart';
import 'package:beavernest_app/domain/diagnostics.dart';
import 'package:flutter/material.dart';

/// Displays a user-requested diagnostic snapshot, never a hidden failure cause.
Future<void> showDiagnosticsSheet(BuildContext context, LoadDiagnostics load) =>
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      builder: (context) => FutureBuilder<WorkspaceDiagnostics>(
        future: load(),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const SizedBox(
              height: 160,
              child: Center(child: CircularProgressIndicator()),
            );
          }
          return _DiagnosticsDetails(value: snapshot.requireData);
        },
      ),
    );

final class _DiagnosticsDetails extends StatelessWidget {
  const _DiagnosticsDetails({required this.value});
  final WorkspaceDiagnostics value;

  @override
  Widget build(BuildContext context) {
    final details = value.isAvailable
        ? [
            'Version ${value.version}',
            'Uptime ${_duration(value.uptimeSeconds!)}',
            'Server time ${value.serverTimeUtc}',
          ]
        : const ['A ready diagnostic snapshot is not available.'];
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(24, 0, 24, 24),
        child: Semantics(
          label: 'Workspace diagnostics',
          liveRegion: true,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Workspace diagnostics',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 16),
              for (final detail in details)
                Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Text(detail),
                ),
              SizedBox(
                height: 44,
                child: TextButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text('Close diagnostics'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

String _duration(int seconds) {
  final minutes = seconds ~/ 60;
  final remaining = seconds % 60;
  if (minutes == 0) return '${remaining}s';
  return '${minutes}m ${remaining}s';
}
