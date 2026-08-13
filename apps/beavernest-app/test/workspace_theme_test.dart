import 'package:beavernest_app/presentation/workspace_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('light semantic status text meets AA contrast on its card fill', () {
    final theme = beaverNestTheme();
    final colors = theme.extension<WorkspaceStatusColors>()!;

    for (final color in [colors.available, colors.unavailable]) {
      expect(
        _contrastRatio(color, _cardFill(color, theme.colorScheme.surface)),
        greaterThanOrEqualTo(4.5),
      );
    }
  });

  test('dark theme provides AA semantic status contrast', () {
    final theme = beaverNestDarkTheme();
    final colors = theme.extension<WorkspaceStatusColors>()!;

    expect(theme.brightness, Brightness.dark);
    for (final color in [colors.available, colors.unavailable]) {
      expect(
        _contrastRatio(color, _cardFill(color, theme.colorScheme.surface)),
        greaterThanOrEqualTo(4.5),
      );
    }
  });
}

Color _cardFill(Color color, Color surface) =>
    Color.alphaBlend(color.withValues(alpha: 0.10), surface);

double _contrastRatio(Color first, Color second) {
  final lighter = first.computeLuminance() > second.computeLuminance()
      ? first
      : second;
  final darker = identical(lighter, first) ? second : first;
  return (lighter.computeLuminance() + 0.05) /
      (darker.computeLuminance() + 0.05);
}
