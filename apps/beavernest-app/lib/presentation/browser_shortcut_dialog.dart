import 'package:flutter/material.dart';

/// Browser guidance is intentionally honest: it neither opens a fake window nor
/// claims offline support that the combined runtime does not provide.
final class BrowserShortcutButton extends StatefulWidget {
  const BrowserShortcutButton({super.key});

  @override
  State<BrowserShortcutButton> createState() => _BrowserShortcutButtonState();
}

final class _BrowserShortcutButtonState extends State<BrowserShortcutButton> {
  final _focusNode = FocusNode(debugLabel: 'Browser shortcut');

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  Future<void> _showGuidance() async {
    await showDialog<void>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Browser shortcut'),
        content: const Text(
          'This workspace is online only. Use your browser’s own shortcut or menu to manage tabs and bookmarks.',
        ),
        actions: [
          SizedBox(
            height: 44,
            child: TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Close'),
            ),
          ),
        ],
      ),
    );
    if (mounted) _focusNode.requestFocus();
  }

  @override
  Widget build(BuildContext context) => FocusableActionDetector(
    focusNode: _focusNode,
    child: Semantics(
      label: 'Browser shortcut',
      button: true,
      child: SizedBox(
        height: 44,
        child: TextButton.icon(
          onPressed: _showGuidance,
          icon: const Icon(Icons.open_in_browser_outlined),
          label: const Text('Browser shortcut'),
        ),
      ),
    ),
  );
}
