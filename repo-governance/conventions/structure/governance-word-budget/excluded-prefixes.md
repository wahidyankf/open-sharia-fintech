---
title: "Excluded Prefixes"
description: The path prefixes the word-budget gate excludes, and why.
when_to_use: Use when checking whether a file is actually measured.
category: explanation
subcategory: conventions
tags:
  - word-budget
  - governance
  - rhino-cli
created: 2026-08-18
---

# Excluded Prefixes

**A surface is its glob minus the registered exclude prefixes.** The list is part of the published
rule, not an implementation detail — a glob alone does not tell you what is measured.

The `governance-word-budget` gate in `repo-config.yml` registers `args.exclude` entries,
which `governance word-budget validate` also folds into a bare CLI run. They are repo-relative path
**prefixes** matched with `str::starts_with`, not globs:

| Prefix        | Why it is excluded                                           |
| ------------- | ------------------------------------------------------------ |
| `plans/`      | Content tree; the budget was never meant to reach it         |
| `docs/`       | Content tree                                                 |
| `specs/`      | Content tree                                                 |
| `.fvm/`       | Local Flutter SDK cache; absent from CI and from most clones |
| `.fvm-cache/` | Same cache                                                   |

All five exist because `**/README.md` matches every README in the repository, including trees
this convention never claimed.

This is not a per-file waiver on an in-scope surface, which stays forbidden. Every hand-authored
`.claude/` source and its generated mirror remains fully gated.

## The Practical Consequence

A `plans/**/README.md` of any length passes. Trimming one satisfies a budget that was never going
to be measured — verified by writing a 1200-word `plans/in-progress/probe/README.md` and confirming
`governance word-budget validate` exits 0 with no finding naming it.

## Related

- [Governance Word-Budget Convention](../governance-word-budget.md) — the surfaces and thresholds.
