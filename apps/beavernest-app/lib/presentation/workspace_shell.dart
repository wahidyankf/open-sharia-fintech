import 'package:beavernest_app/application/use_cases/load_readiness.dart';
import 'package:beavernest_app/domain/readiness.dart';
import 'package:flutter/material.dart';

/// The small, route-independent status shell for the Flutter Web root route.
final class WorkspaceShell extends StatefulWidget {
  const WorkspaceShell({required this.loadReadiness, super.key});

  final LoadReadiness loadReadiness;

  @override
  State<WorkspaceShell> createState() => _WorkspaceShellState();
}

final class _WorkspaceShellState extends State<WorkspaceShell> {
  late final Future<WorkspaceReadiness> _readiness;

  @override
  void initState() {
    super.initState();
    _readiness = widget.loadReadiness();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    body: Center(
      child: FutureBuilder<WorkspaceReadiness>(
        future: _readiness,
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return Semantics(
              label: 'Foundation status shell loading',
              child: Text('Foundation status shell'),
            );
          }
          return _ReadinessStatus(readiness: snapshot.requireData);
        },
      ),
    ),
  );
}

final class _ReadinessStatus extends StatelessWidget {
  const _ReadinessStatus({required this.readiness});

  final WorkspaceReadiness readiness;

  @override
  Widget build(BuildContext context) => Semantics(
    label: readiness.isReady
        ? 'Application Available, Database Ready, Schema Current'
        : 'Application Unavailable, Database Unavailable, Schema Unknown',
    child: const Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text('Application Available'),
        Text('Database Ready'),
        Text('Schema Current'),
      ],
    ),
  );
}
