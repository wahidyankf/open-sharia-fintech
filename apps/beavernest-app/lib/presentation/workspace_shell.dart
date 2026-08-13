import 'package:beavernest_app/application/use_cases/load_diagnostics.dart';
import 'package:beavernest_app/application/use_cases/load_readiness.dart';
import 'package:beavernest_app/application/use_cases/refresh_readiness.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:beavernest_app/presentation/browser_shortcut_dialog.dart';
import 'package:beavernest_app/presentation/diagnostics_sheet.dart';
import 'package:beavernest_app/presentation/status_dashboard.dart';
import 'package:flutter/material.dart';

/// The accessible, route-independent status workspace for the Flutter Web root.
final class WorkspaceShell extends StatefulWidget {
  const WorkspaceShell({
    required this.loadReadiness,
    required this.refreshReadiness,
    required this.loadDiagnostics,
    super.key,
  });

  final LoadReadiness loadReadiness;
  final RefreshReadiness refreshReadiness;
  final LoadDiagnostics loadDiagnostics;

  @override
  State<WorkspaceShell> createState() => _WorkspaceShellState();
}

final class _WorkspaceShellState extends State<WorkspaceShell> {
  late Future<WorkspaceReadiness> _readiness;

  @override
  void initState() {
    super.initState();
    _readiness = widget.loadReadiness();
  }

  void _refresh() {
    setState(() {
      _readiness = widget.refreshReadiness();
    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    body: SafeArea(
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 1120),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: FutureBuilder<WorkspaceReadiness>(
              future: _readiness,
              builder: (context, snapshot) {
                if (!snapshot.hasData) {
                  return Semantics(
                    label: 'Foundation status shell loading',
                    liveRegion: true,
                    child: const Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          CircularProgressIndicator(),
                          SizedBox(height: 12),
                          Text('Foundation status shell'),
                        ],
                      ),
                    ),
                  );
                }
                return Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    StatusDashboard(readiness: snapshot.requireData),
                    const SizedBox(height: 24),
                    Wrap(
                      spacing: 12,
                      runSpacing: 12,
                      children: [
                        Semantics(
                          label: 'Refresh status',
                          button: true,
                          child: SizedBox(
                            height: 44,
                            child: FilledButton.icon(
                              onPressed: _refresh,
                              icon: const Icon(Icons.refresh),
                              label: const Text('Refresh status'),
                            ),
                          ),
                        ),
                        Semantics(
                          label: 'Open workspace diagnostics',
                          button: true,
                          child: SizedBox(
                            height: 44,
                            child: OutlinedButton.icon(
                              onPressed: () => showDiagnosticsSheet(
                                context,
                                widget.loadDiagnostics,
                              ),
                              icon: const Icon(Icons.monitor_heart_outlined),
                              label: const Text('Diagnostics'),
                            ),
                          ),
                        ),
                        const BrowserShortcutButton(),
                      ],
                    ),
                  ],
                );
              },
            ),
          ),
        ),
      ),
    ),
  );
}
