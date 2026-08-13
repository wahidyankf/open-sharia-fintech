import 'package:flutter/material.dart';

/// Browser guidance is intentionally honest: it neither opens a fake window nor
/// claims offline support that the combined runtime does not provide.
final class BrowserShortcutButton extends StatefulWidget {
  const BrowserShortcutButton({super.key});

  @override
  State<BrowserShortcutButton> createState() => _BrowserShortcutButtonState();
}

final class _BrowserShortcutButtonState extends State<BrowserShortcutButton> {
  final _focusNode = FocusNode(debugLabel: 'Help');

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  Future<void> _showGuidance() async {
    await showDialog<void>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Browser Help'),
        content: SingleChildScrollView(
          child: FocusTraversalGroup(
            policy: OrderedTraversalPolicy(),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'This workspace is online only. Browser availability varies by device and browser.',
                ),
                SizedBox(height: 16),
                Semantics(
                  label: 'Browser availability steps',
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('1. Open your browser menu.'),
                      SizedBox(height: 8),
                      Text(
                        '2. Choose an available shortcut or install action.',
                      ),
                      SizedBox(height: 8),
                      Text('3. Confirm the browser prompt if one appears.'),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
        actions: [
          SizedBox(
            height: 44,
            child: TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Close Help'),
            ),
          ),
        ],
      ),
    );
    if (mounted) _focusNode.requestFocus();
  }

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Browser Help', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          const Text(
            'Find browser-specific shortcut guidance. An internet connection is required.',
          ),
          const SizedBox(height: 8),
          FocusableActionDetector(
            focusNode: _focusNode,
            child: SizedBox(
              height: 44,
              child: TextButton.icon(
                onPressed: _showGuidance,
                icon: const Icon(Icons.help_outline),
                label: const Text('Help'),
              ),
            ),
          ),
        ],
      ),
    ),
  );
}
