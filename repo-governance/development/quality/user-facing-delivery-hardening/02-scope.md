---
title: "Scope"
description: "What this convention applies to."
category: explanation
subcategory: development
tags:
  - quality
  - planning
  - ui
  - verification
  - testing
  - deployment
created: 2026-06-19
when_to_use: "Use when checking whether this convention applies to a plan."
---

# Scope

## What This Convention Covers

- Authoring plans for any user-facing change (web UI, rendered output, public-facing CLI text).
- API feature-change plans (REST or GraphQL endpoints) — the near-end `api-exploratory-tester`
  retest (Rule 16); an API is a user-facing surface for its client and integrator consumers.
- Executing, verifying, and archiving those plans.
- The done/archival criterion for user-facing work.

## What This Convention Does NOT Cover

- Pure library/internal refactors with no observable output (see
  [Manual Behavioral Verification](.././manual-behavioral-verification.md) scope).
- Documentation/governance-only changes.
- Incidental API behavior outside a feature change (covered by the curl path in
  [Manual Behavioral Verification](.././manual-behavioral-verification.md)); API **feature-change**
  plans are covered here — see Rule 16.
