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
  _WorkspaceView _view = _WorkspaceView.status;

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

  void _showStatus() => setState(() => _view = _WorkspaceView.status);

  void _showDiagnostics() => setState(() => _view = _WorkspaceView.diagnostics);

  @override
  Widget build(BuildContext context) => Scaffold(
    body: SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 1120),
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
                return LayoutBuilder(
                  builder: (context, constraints) {
                    final desktop = constraints.maxWidth >= 1024;
                    final content = _view == _WorkspaceView.status
                        ? _StatusWorkspace(
                            readiness: snapshot.requireData,
                            onRefresh: _refresh,
                            onDiagnostics: _showDiagnostics,
                            showDiagnosticsAction: !desktop,
                          )
                        : DiagnosticsWorkspace(
                            loadDiagnostics: widget.loadDiagnostics,
                            onStatus: _showStatus,
                          );
                    if (!desktop) return content;
                    return FocusTraversalGroup(
                      policy: OrderedTraversalPolicy(),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _WorkspaceNavigationRail(
                            view: _view,
                            onStatus: _showStatus,
                            onDiagnostics: _showDiagnostics,
                          ),
                          const SizedBox(width: 32),
                          Expanded(child: content),
                        ],
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ),
      ),
    ),
  );
}

enum _WorkspaceView { status, diagnostics }

final class _StatusWorkspace extends StatelessWidget {
  const _StatusWorkspace({
    required this.readiness,
    required this.onRefresh,
    required this.onDiagnostics,
    required this.showDiagnosticsAction,
  });

  final WorkspaceReadiness readiness;
  final VoidCallback onRefresh;
  final VoidCallback onDiagnostics;
  final bool showDiagnosticsAction;

  @override
  Widget build(BuildContext context) => FocusTraversalGroup(
    policy: OrderedTraversalPolicy(),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        FocusTraversalOrder(
          order: const NumericFocusOrder(1),
          child: StatusDashboard(readiness: readiness),
        ),
        const SizedBox(height: 24),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            FocusTraversalOrder(
              order: const NumericFocusOrder(2),
              child: SizedBox(
                height: 44,
                child: FilledButton.icon(
                  onPressed: onRefresh,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Refresh status'),
                ),
              ),
            ),
            if (showDiagnosticsAction)
              FocusTraversalOrder(
                order: const NumericFocusOrder(3),
                child: SizedBox(
                  height: 44,
                  child: OutlinedButton.icon(
                    onPressed: onDiagnostics,
                    icon: const Icon(Icons.monitor_heart_outlined),
                    label: const Text('Diagnostics'),
                  ),
                ),
              ),
          ],
        ),
        const SizedBox(height: 24),
        const FocusTraversalOrder(
          order: NumericFocusOrder(4),
          child: BrowserShortcutButton(),
        ),
      ],
    ),
  );
}

final class _WorkspaceNavigationRail extends StatelessWidget {
  const _WorkspaceNavigationRail({
    required this.view,
    required this.onStatus,
    required this.onDiagnostics,
  });

  final _WorkspaceView view;
  final VoidCallback onStatus;
  final VoidCallback onDiagnostics;

  @override
  Widget build(BuildContext context) => Semantics(
    label: 'Workspace navigation',
    container: true,
    child: Container(
      key: const Key('workspace-navigation-rail'),
      width: 208,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text('BeaverNest', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 4),
          Text(
            'FOUNDATION WORKSPACE',
            style: Theme.of(context).textTheme.labelSmall,
          ),
          const SizedBox(height: 24),
          NavigationRailDestinationButton(
            icon: Icons.monitor_heart_outlined,
            label: 'Status',
            selected: view == _WorkspaceView.status,
            onPressed: onStatus,
          ),
          const SizedBox(height: 8),
          NavigationRailDestinationButton(
            icon: Icons.fact_check_outlined,
            label: 'Diagnostics',
            selected: view == _WorkspaceView.diagnostics,
            onPressed: onDiagnostics,
          ),
        ],
      ),
    ),
  );
}

final class NavigationRailDestinationButton extends StatelessWidget {
  const NavigationRailDestinationButton({
    required this.icon,
    required this.label,
    required this.selected,
    required this.onPressed,
    super.key,
  });

  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) => OutlinedButton.icon(
    onPressed: onPressed,
    icon: Icon(icon),
    label: Align(alignment: Alignment.centerLeft, child: Text(label)),
    style:
        OutlinedButton.styleFrom(
          alignment: Alignment.centerLeft,
          backgroundColor: selected
              ? Theme.of(context).colorScheme.secondaryContainer
              : null,
        ).copyWith(
          side: WidgetStateProperty.resolveWith(
            (states) => states.contains(WidgetState.focused)
                ? BorderSide(
                    color: Theme.of(context).colorScheme.onSurface,
                    width: 3,
                  )
                : null,
          ),
        ),
  );
}
