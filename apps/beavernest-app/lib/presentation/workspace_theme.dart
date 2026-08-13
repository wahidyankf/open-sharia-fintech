import 'package:flutter/material.dart';

/// Semantic status colours kept independent of Material's surface palette.
@immutable
final class WorkspaceStatusColors
    extends ThemeExtension<WorkspaceStatusColors> {
  const WorkspaceStatusColors({
    required this.available,
    required this.unavailable,
    required this.surfaceTint,
  });

  final Color available;
  final Color unavailable;
  final Color surfaceTint;

  @override
  WorkspaceStatusColors copyWith({
    Color? available,
    Color? unavailable,
    Color? surfaceTint,
  }) => WorkspaceStatusColors(
    available: available ?? this.available,
    unavailable: unavailable ?? this.unavailable,
    surfaceTint: surfaceTint ?? this.surfaceTint,
  );

  @override
  WorkspaceStatusColors lerp(
    ThemeExtension<WorkspaceStatusColors>? other,
    double t,
  ) {
    if (other is! WorkspaceStatusColors) return this;
    return WorkspaceStatusColors(
      available: Color.lerp(available, other.available, t)!,
      unavailable: Color.lerp(unavailable, other.unavailable, t)!,
      surfaceTint: Color.lerp(surfaceTint, other.surfaceTint, t)!,
    );
  }
}

ThemeData beaverNestTheme() {
  const navy = Color(0xff102a43);
  const river = Color(0xff1f6f78);
  const meadow = Color(0xff157a4d);
  const ember = Color(0xffb54708);
  const mist = Color(0xffedf5f5);
  const cloud = Color(0xfff8fbfc);
  final scheme = ColorScheme.fromSeed(
    seedColor: river,
    brightness: Brightness.light,
  ).copyWith(surface: cloud, onSurface: navy, primary: river, error: ember);
  return ThemeData(
    colorScheme: scheme,
    scaffoldBackgroundColor: cloud,
    extensions: const [
      WorkspaceStatusColors(
        available: meadow,
        unavailable: ember,
        surfaceTint: mist,
      ),
    ],
  );
}
