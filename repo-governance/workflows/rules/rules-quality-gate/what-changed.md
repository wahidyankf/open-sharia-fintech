---
title: "What Changed"
description: A changelog of the Step 0.5 preflight addition and the two archived plans that hardened and then resynced it.
when_to_use: Use when tracing why the deterministic preflight step exists or when the rhino-cli category list was last resynced.
---

# What changed

Lifecycle ownership filtering added 2026-08-27. The quality gate now delegates registered vendor
and word-budget predicates, retains layer coherence and traceability as domain findings, and never
uses missing evidence as permission for an AI fallback.

Step 0.5 added 2026-05-12 referencing the archived `2026-05-12__optimize-rules-quality-gate-with-rhino-cli` plan. Hardening edits (broken-command fix, visibility-only codification, hash-reuse documentation, arg-name unification, exit-2 recovery, Skip-list Curation Rules section, Observability Metrics section, Step-0.5 numbering rationale, operator hatch) added by `plans/done/2026-05-12__complete-repo-rules-zero-findings/`.

Ordinal-prefix judgement added 2026-08-18 as an **AI-only** category under Core Repository
Validation: no deterministic gate decides whether a leading `NN-` ordinal marks a real step, so
`repo-rules-checker` judges it against
[Ordinal Filename Prefixes](../../../conventions/structure/ordinal-filename-prefixes.md).

Resynced 2026-08-27 with the four-category `repo-governance audit` orchestrator. This workflow
retains `layer-coherence` and `traceability-audit`; lifecycle owners supply exact evidence for
`vendor-audit` and `governance-word-budget`. The vendor category scans only `repo-governance/`,
`AGENTS.md`, and `CLAUDE.md`, avoiding build caches, worktrees, app content, and generated reports.
