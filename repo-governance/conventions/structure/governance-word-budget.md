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
per-surface word thresholds and the single sanctioned remediation (progressive disclosure). Word
count, not byte count, is the metric: a raw whole-file `split_whitespace()` count, no exclusions.

## Monitored Surfaces

Configured in the `governance-word-budget:` section of `repo-config.yml`; enforced by
`rhino-cli governance word-budget validate`.

| Surface                                                                       | Target (✅) | Warn (⚠️)  | Fail (❌)  |
| ----------------------------------------------------------------------------- | ----------- | ---------- | ---------- |
| `repo-governance/**/*.md`                                                     | 400 words   | 500 words  | 500 words  |
| `AGENTS.md` / `CLAUDE.md`                                                     | 400 words   | 500 words  | 500 words  |
| `.claude/`, `.cursor/`, `.codex/`, `.opencode/`, `.pi/`, `.amazonq/` (`*.md`) | 400         | 500        | 500        |
| `**/README.md`                                                                | 700 words   | 900 words  | 900 words  |
| Resolved tree (`CLAUDE.md` + imports)                                         | 1200 words  | 1500 words | 1500 words |

`repo-governance/**/*.md` is the largest surface by file count and the primary target of the
`optimize-governance-md` plan this convention's word-count metric belongs to.

When a path matches more than one surface glob, the **last-declared** surface wins (select, then
classify) — see `tech-docs.md` §1.3. This is a declaration-order invariant, not a mechanical
glob-specificity comparison: a more-specific surface glob MUST be declared after any more-general
surface it overlaps. Today `**/README.md` is the only surface that overlaps others (every other
surface's directory globs also match README.md files), which is why it is declared last in
`repo-config.yml`. A future reorder, or a new general glob inserted after it, silently
misclassifies every README.md under the wrong budget with no error signal —
`application::governance::word_budget::tests::surfaces_declares_readme_glob_last` in `rhino-cli`
enforces this mechanically against the live config; update that test if a future change
legitimately needs a different declaration order.

## Enforcement Points

Runs at pre-push (changed-path gated), in CI, and as category 4 of `repo-governance audit`'s
preflight. No pre-commit surface is declared. See
[Governance Word-Budget Remediation](../structure/governance-word-budget-remediation.md) for the enforcement
breakdown, the progressive-disclosure fix, and forbidden anti-fixes (deleting a rule, dense
compression, splitting into another auto-loaded file, or an incomplete `See`-link target).

## Updating Thresholds

Edit the `governance-word-budget:` section of `repo-config.yml`, record the rationale as a YAML
comment, and run `npx nx run rhino-cli:governance-word-budget:validation` to confirm. Never adjust
a threshold to paper over a bloated file.

## Children

- [Vision and Principles](./governance-word-budget/01-vision-and-principles.md) — vision alignment, principles implemented, and related conventions.
