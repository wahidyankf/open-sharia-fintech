---
title: "Governance Word-Budget Convention"
description: Per-surface word thresholds for auto-loaded instruction files, enforced by rhino-cli and git hooks
when_to_use: Use when a governance or instruction file may be approaching or over its word-count threshold.
category: explanation
subcategory: conventions
tags:
  - instruction-files
  - agents-md
  - word-budget
  - governance
  - rhino-cli
created: 2026-06-27
---

# Governance Word-Budget Convention

Coding-agent harnesses auto-load certain instruction files before the first user message. Past
harness limits, instructions are **silently truncated or ignored**. This convention sets
per-surface word thresholds and the one sanctioned remediation (progressive disclosure). The metric
is a raw whole-file `split_whitespace()` word count, not bytes, with no in-file exclusions.

## Monitored Surfaces

Configured in the `governance-word-budget:` section of `repo-config.yml`; enforced by
`rhino-cli governance word-budget validate`.

| Surface                                                             | Target (✅) | Warn (⚠️)  | Fail (❌)  |
| ------------------------------------------------------------------- | ----------- | ---------- | ---------- |
| `repo-governance/**/*.md`                                           | 400 words   | 500 words  | 500 words  |
| `AGENTS.md` / `CLAUDE.md`                                           | 400 words   | 500 words  | 500 words  |
| Every harness binding directory in the `harness:` registry (`*.md`) | 400         | 500        | 500        |
| `**/README.md`                                                      | 700 words   | 900 words  | 900 words  |
| Resolved tree (`CLAUDE.md` + imports)                               | 1200 words  | 1500 words | 1500 words |

`repo-governance/**/*.md` is the largest surface by file count.

**A surface is its glob minus the registered exclude prefixes** — the seven `args.exclude` path
prefixes on the gate are part of the published rule, not an implementation detail. `plans/`,
`docs/`, and `specs/` are among them, so a `plans/` README of any length passes. The full list is
in the Excluded Prefixes child below.

When a path matches more than one surface glob, the **last-declared** surface wins (select, then
classify). This is a declaration-order invariant, not a glob-specificity comparison: a
more-specific glob MUST be declared after any more-general surface it overlaps. `**/README.md` is
the only overlapping surface today — every other surface's directory glob also matches its
README.md files — which is why it is declared last. A reorder, or a new general glob inserted after
it, silently misclassifies every README.md with no error signal;
`application::governance::word_budget::tests::surfaces_declares_readme_glob_last` enforces the
order against the live config. Update that test if a change legitimately needs a different one.

## Enforcement Points

Runs at pre-push (changed-path gated), in CI, and as category 4 of `repo-governance audit`'s
preflight. No pre-commit surface. See
[Governance Word-Budget Remediation](../structure/governance-word-budget-remediation.md) for the enforcement
breakdown, the progressive-disclosure fix, and forbidden anti-fixes (deleting a rule, dense
compression, splitting into another auto-loaded file, or an incomplete `See`-link target).

## Updating Thresholds

Edit the `governance-word-budget:` section of `repo-config.yml`, record the rationale as a YAML
comment, and run `npx nx run rhino-cli:governance-word-budget:validation` to confirm. Never adjust
a threshold to paper over a bloated file.

## Children

- [Vision and Principles](./governance-word-budget/vision-and-principles.md) — vision alignment, principles implemented, and related conventions.
- [Excluded Prefixes](./governance-word-budget/excluded-prefixes.md) — The seven path prefixes the word-budget gate excludes, and why. Use when checking whether a file is actually measured.
