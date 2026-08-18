---
title: "What Changed"
description: A changelog of the Step 0.5 preflight addition and the two archived plans that hardened and then resynced it.
when_to_use: Use when tracing why the deterministic preflight step exists or when the rhino-cli category list was last resynced.
---

# What changed

Step 0.5 added 2026-05-12 referencing the archived `2026-05-12__optimize-repo-rules-quality-gate-with-rhino-cli` plan. Hardening edits (broken-command fix, visibility-only codification, hash-reuse documentation, arg-name unification, exit-2 recovery, Skip-list Curation Rules section, Observability Metrics section, Step-0.5 numbering rationale, operator hatch) added by `plans/done/2026-05-12__complete-repo-rules-zero-findings/`.

Ordinal-prefix judgement added 2026-08-18 as an **AI-only** category under Core Repository
Validation: no deterministic gate decides whether a leading `NN-` ordinal marks a real step, so
`repo-rules-checker` judges it against
[Ordinal Filename Prefixes](../../../conventions/structure/ordinal-filename-prefixes.md).

Resynced 2026-06-22 after the `rhino-cli` command-surface refactor (`refactor(rhino-cli)!: regroup by scope + uniform verb-first subcommand surface`): Step 0.5 now documents the real three-category `repo-governance audit` orchestrator (`layer-coherence`, `traceability-audit`, `vendor-audit`) instead of a stale nine-category list, and the `vendor-audit` category was fixed to scan only `repo-governance/` + `AGENTS.md` + `CLAUDE.md` (it previously walked the whole repo — build caches, worktrees, app content, generated reports — emitting ~20k noise findings). The operator hatch, exit-2 debug hint, and Iteration Example were corrected to match.
