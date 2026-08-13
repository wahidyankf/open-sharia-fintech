---
title: "Governance Word-Budget Convention"
description: Per-surface word thresholds for auto-loaded instruction files, enforced by rhino-cli and git hooks
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

| Surface                                                    | Target (✅) | Warn (⚠️)  | Fail (❌)  |
| ---------------------------------------------------------- | ----------- | ---------- | ---------- |
| `AGENTS.md` / `CLAUDE.md`                                  | 400 words   | 500 words  | 500 words  |
| `.claude/`, `.cursor/`, `.opencode/`, `.amazonq/` (`*.md`) | 400         | 500        | 500        |
| `**/README.md`                                             | 700 words   | 900 words  | 900 words  |
| Resolved tree (`CLAUDE.md` + imports)                      | 1200 words  | 1500 words | 1500 words |

When a path matches more than one surface glob, the **last-declared** surface wins (select, then
classify) — see `tech-docs.md` §1.3.

## Enforcement Points

Runs at pre-push (changed-path gated), pre-commit (`convention audit`), CI, and as category 4 of
`repo-governance audit`'s preflight. See
[Governance Word-Budget Remediation](./governance-word-budget-remediation.md) for the enforcement
breakdown, the progressive-disclosure fix, and forbidden anti-fixes (deleting a rule, dense
compression, splitting into another auto-loaded file, or an incomplete `See`-link target).

## Updating Thresholds

Edit the `governance-word-budget:` section of `repo-config.yml`, record the rationale as a YAML
comment, and run `npx nx run rhino-cli:governance-word-budget:validation` to confirm. Never adjust
a threshold to paper over a bloated file.

## Vision Supported

This convention serves the [Open Sharia Enterprise Vision](../../vision/open-sharia-enterprise.md)
by ensuring governance rules embedded in instruction files stay reliably loaded, not silently
dropped past a harness limit.

## Principles Implemented/Respected

- **[Progressive Disclosure](../../principles/content/progressive-disclosure.md)**: the sole
  sanctioned remediation for word-budget violations.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  thresholds are declared explicitly in `repo-config.yml`, not embedded in the validator binary.
- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**:
  every enforcement point is automated.
- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: the word
  count is deterministic.

## Related Conventions

- [Governance Word-Budget Remediation](./governance-word-budget-remediation.md) — enforcement
  points, the progressive-disclosure fix, and forbidden anti-fixes
- [Deterministic vs AI Validation Split](./deterministic-vs-ai-validation-split.md)
- [Governance Vendor-Independence Convention](./governance-vendor-independence.md)
- [Multi-Harness Binding Convention](./multi-harness-binding.md)
