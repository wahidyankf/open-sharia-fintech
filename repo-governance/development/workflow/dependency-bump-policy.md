---
title: "Dependency Bump Stability & Safety Policy"
description: Three-path decision tree (LTS, 60-day soak, security waiver) governing every dependency bump across the polyglot monorepo.
category: explanation
subcategory: development
tags:
  - dependencies
  - security
  - versioning
  - reproducibility
  - workflow
created: 2026-05-15
when_to_use: Use whenever bumping a dependency, runtime, or base image version, to classify the path and pin exactly.
---

# Dependency Bump Stability & Safety Policy

Every dependency bump MUST satisfy three constraints before it is merged: (1) reproducibility via exact pinning, (2) stability via LTS-first or 60-day soak, and (3) security via CVE clearance. This rule prevents shipping fresh versions whose breakage profile is undiscovered while ensuring known vulnerabilities are patched.

## Contents

- [Principles and Conventions Implemented](./dependency-bump-policy/principles-and-conventions-implemented.md) — Why this policy exists.
- [Scope](./dependency-bump-policy/scope.md) — Which manifests are covered.
- [Three-Path Decision Tree](./dependency-bump-policy/three-path-decision-tree.md) — Path A (LTS), Path B (60-day), Path C (waiver).
- [KEV Fast-Track and EPSS Escalation](./dependency-bump-policy/kev-fast-track-and-epss-escalation.md) — Actively-exploited-CVE overrides.
- [Selection Rules Within Every Path](./dependency-bump-policy/selection-rules-within-every-path.md) — Recency and functional stability.
- [Pinning Policy (Hard Rule)](./dependency-bump-policy/pinning-policy-hard-rule.md) — Exact-pin form per manifest.
- [CVE Clearance Process](./dependency-bump-policy/cve-clearance-process.md) — The five sources and the clearance status values.
- [Cutoff Date Computation and Plan Duration](./dependency-bump-policy/cutoff-date-computation-and-plan-duration.md) — Stating the cutoff, and re-checking on long plans.
- [Examples](./dependency-bump-policy/examples.md) — Worked Path A/B/C decisions.
- [Application Workflow](./dependency-bump-policy/application-workflow.md) — The twelve-step procedure.
- [Tools, Automation, and References](./dependency-bump-policy/tools-automation-and-references.md) — Enforcement tools and the full reference list.
