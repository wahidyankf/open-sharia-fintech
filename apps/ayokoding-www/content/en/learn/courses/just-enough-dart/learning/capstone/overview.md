---
title: "Dart Availability CLI"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Build a short console program that reports which requested product codes are available. This is a
light language consolidation exercise, not a Flutter project: every feature stays small enough to
inspect without platform setup.

## Goal and acceptance criteria

The completed program uses null-safe lookup and `??`, a class with a mixin, a generic collection,
an `async`/`await` `Future`, and an `await for` stream consumer. It prints an availability report
in request order, handles a missing code without throwing, and has a `dart test` that verifies the
stream results.

## Build it

1. From `code/`, run `dart pub get`, then `dart run`. Confirm the absent code reports
   `unavailable` rather than throwing.
2. Read `lib/availability.dart` and identify where nullable map lookup becomes a display label.
   Change the request list and confirm the output preserves that order.
3. Run `dart test`. Add one requested code to the test input and assert its matching report line.

## Why this is the right-sized capstone

Flutter would add widget lifecycle, platform setup, rendering, and state ownership before the Dart
surface can settle. This CLI focuses the proof: a typed generic model uses a mixin, missing data
has an explicit fallback, asynchronous work returns a `Future`, and a `Stream` delivers ordered
report lines. Those are the language contracts you will read inside Hybrid App Development.
