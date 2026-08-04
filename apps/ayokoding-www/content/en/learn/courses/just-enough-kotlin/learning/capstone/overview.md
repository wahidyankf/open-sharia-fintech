---
title: "Kotlin Availability CLI"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Build a short command-line program that reports which requested products are available. The point is
consolidation, not a framework project: keep the program small enough that every feature remains
visible.

## Goal and acceptance criteria

The finished program uses nullable lookup plus `?:`, a `data class`, a collection `map`, an
interface with an implementation, and one suspending calculation. It prints a useful availability
report, dispatches through the interface, and completes the coroutine before the process exits.

## Build it

1. From `code/`, run `gradle run` with an installed Gradle distribution. Confirm a missing SKU prints
   `unavailable` rather than throwing.
2. Add a second `Inventory` implementation that always returns an empty result. The report should
   still work because it depends on the interface, not a concrete map.
3. Change the list of requested SKUs and verify the `map` pipeline preserves input order while the
   suspending lookup completes before output appears.

## Why this is the right-sized capstone

An Android application would introduce UI state, lifecycle ownership, Gradle plugins, and SDK APIs
before the language mechanics can settle. This CLI keeps the proof focused: Kotlin records absence
in the type, immutable data is easy to transform, interfaces preserve a seam, and a suspending
operation belongs to a structured coroutine scope.
