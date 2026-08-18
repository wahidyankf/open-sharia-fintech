---
title: "Mechanize Cross-File Invariants — The Rule"
description: The four-step procedure - identify a single source of truth, generate dependents from it, validate generated output in the normal gate, and never hand-edit a generated file
category: explanation
subcategory: development
tags:
  - generate-and-validate
  - drift
  - automation
  - governance
created: 2026-08-07
when_to_use: Use when you've identified a rule that must hold across two or more files and need the concrete steps to mechanize it.
---

# The Rule

When you notice a rule, value, or structure that must hold identically across two or more files:

1. **Identify (or create) the single source of truth** — a schema, a registry file, a config key —
   that the rule's content should live in exactly once.
2. **Generate every dependent file from that source**, mechanically, rather than hand-authoring each
   copy to match.
3. **Validate the generated output against the source** as part of the normal quality gate (pre-commit,
   pre-push, or CI) — a generated file that has drifted from what the generator would currently
   produce is a failure, not a warning.
4. **Never hand-edit a generated file directly.** A generated file's git history should show only
   regenerated diffs; a hand-edit that happens to match what the generator would have produced is
   still a drift risk the next time the source changes.

This is not a special case reserved for any one subsystem — it is the default response whenever a
normative rule would otherwise need to be stated once in prose and then trusted to be followed
identically in two or more places that prose cannot mechanically check.
