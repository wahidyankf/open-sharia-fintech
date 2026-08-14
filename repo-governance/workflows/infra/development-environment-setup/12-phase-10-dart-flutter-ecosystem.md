---
title: "Phase 10: Dart/Flutter Ecosystem (Sequential)"
description: "Phase 10 (full scope only): install Flutter (bundles Dart) and enable Flutter Web, required for the ose-primer polyglot demo apps."
when_to_use: "Use when setting up Dart/Flutter for the ose-primer polyglot demo apps under full scope."
---

# Phase 10: Dart/Flutter Ecosystem (Sequential)

**Condition**: `{input.scope} == full`

Required for: polyglot demo apps in ose-primer (extracted 2026-04-18)

## 10.1 Install Flutter (includes Dart)

```bash
# macOS
brew install --cask flutter

# Or manual install: https://docs.flutter.dev/get-started/install
```

Flutter bundles the Dart SDK. The minimum Dart SDK version is in the `ose-primer` repository's `pubspec.yaml` under `environment.sdk`.

**Success criteria**: `flutter --version` and `dart --version` both return version strings.
Dart version >= the pubspec constraint.

## 10.2 Enable Flutter Web

```bash
flutter config --enable-web
flutter doctor
```

**Success criteria**: `flutter doctor` shows no critical issues for web development.
