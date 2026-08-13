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
  const meadow = Color(0xff14784c);
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
    focusColor: navy,
    fontFamily: 'Roboto',
    filledButtonTheme: FilledButtonThemeData(
      style: _focusableActionStyle(navy),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: _focusableActionStyle(navy),
    ),
    textButtonTheme: TextButtonThemeData(style: _focusableActionStyle(navy)),
    extensions: const [
      WorkspaceStatusColors(
        available: meadow,
        unavailable: ember,
        surfaceTint: mist,
      ),
    ],
  );
}

ThemeData beaverNestDarkTheme() {
  const night = Color(0xff0b1f2a);
  const ice = Color(0xfff3f7fa);
  const aqua = Color(0xff5ed3dc);
  const mint = Color(0xff64d99a);
  const peach = Color(0xffffb58a);
  const deepWater = Color(0xff17384a);
  final scheme = ColorScheme.fromSeed(
    seedColor: aqua,
    brightness: Brightness.dark,
  ).copyWith(surface: night, onSurface: ice, primary: aqua, error: peach);
  return ThemeData(
    colorScheme: scheme,
    scaffoldBackgroundColor: night,
    focusColor: ice,
    fontFamily: 'Roboto',
    filledButtonTheme: FilledButtonThemeData(style: _focusableActionStyle(ice)),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: _focusableActionStyle(ice),
    ),
    textButtonTheme: TextButtonThemeData(style: _focusableActionStyle(ice)),
    extensions: const [
      WorkspaceStatusColors(
        available: mint,
        unavailable: peach,
        surfaceTint: deepWater,
      ),
    ],
  );
}

ButtonStyle _focusableActionStyle(Color focusColor) => ButtonStyle(
  minimumSize: const WidgetStatePropertyAll(Size(44, 44)),
  side: WidgetStateProperty.resolveWith(
    (states) => states.contains(WidgetState.focused)
        ? BorderSide(color: focusColor, width: 3)
        : null,
  ),
);
