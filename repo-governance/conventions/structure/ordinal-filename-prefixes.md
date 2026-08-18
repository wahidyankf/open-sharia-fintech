---
title: "Ordinal Filename Prefixes Convention"
description: When a governed markdown filename may carry a leading NN- ordinal, and when the parent index carries order instead
when_to_use: Use when naming or renaming a governed markdown file whose name starts with a number, or when splitting a document into shards.
category: explanation
subcategory: conventions
tags:
  - naming
  - files
  - conventions
  - ordinals
created: 2026-08-18
---

# Ordinal Filename Prefixes Convention

A governed markdown filename may carry a leading ordinal **only when the file is a real step in an
ordered sequence and the ordinal is that step's own number**. A basename never carries two numbering
systems. Failing either test, the file takes a plain lowercase kebab-case name and the **parent index
carries the order**.

This replaces the blanket "no prefixes" clause formerly in [File Naming](./file-naming.md). That ban
was wrong: real step sequences exist, and stripping their ordinals destroys meaning the index cannot
recover.

## The Two Questions

1. **Is it a real step in an ordered sequence?** A word-budget shard, a topic page, or a reference
   module is not a step — it is content that happens to have neighbours.
2. **Is the prefix that step's own number?** A serial position assigned by a split, or a second
   number embedded in the name, means no.

Only **yes** to both keeps the ordinal.

## Worked Cases

Both sides are load-bearing.

| Filename                                        | Verdict                                                                                                                                        |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `29-common-syntax-errors-special-characters.md` | **Fails** — serial position from a word-budget split → `common-syntax-errors-special-characters.md`                                            |
| `04-phase-1-system-package-manager.md`          | **Fails** — two numbering systems → `01-system-package-manager.md`                                                                             |
| `01b-inherited-and-specialized-requirements.md` | **Fails** — insert escape → `inherited-and-specialized-requirements.md`                                                                        |
| `02-step-1-and-2-maker-and-checker.md`          | **Fails** — ordinal 02 labels steps 1–2, so the systems disagree → `02-maker-and-checker.md`, keeping the ordinal because the file _is_ a step |
| `04-step-4-fixer.md`                            | **Keeps its ordinal, sheds the redundant token** → `04-fixer.md`                                                                               |
| `04-fixer.md` (post-rename)                     | **Passes** — a real step whose ordinal is that step's own number                                                                               |

For a step **range**, the ordinal equals the first step:
`05-step-5-and-6-iteration-control-and-finalization.md` passes, becoming
`05-iteration-control-and-finalization.md`.

## The Keep-Clause Is Not Vacuous

In `repo-governance/workflows/ayokoding-web/ayokoding-web-swe-by-example-quality-gate/`,
`03-step-3-user-review.md` and `04-step-4-fixer.md` already carry an ordinal equal to the step's own
number; they fail only on the redundant second token, which this rule strips.

Confirm non-emptiness rather than trusting this:

```bash
find repo-governance/workflows -name '*.md' | grep -E '/[0-9]{2}-' | grep -E 'step-[0-9]+' | while read f; do
  b=$(basename "$f"); ord=$(echo "$b" | grep -oE '^[0-9]{2}' | sed 's/^0//')
  emb=$(echo "$b" | grep -oE 'step-[0-9]+' | grep -oE '[0-9]+$' | head -1)
  [ "$ord" = "$emb" ] && echo "$f"
done
```

With no Passes instances, the rule collapses into the ban it replaces.

## Where Order Comes From

For plain-named files, order lives in the parent `README.md` index, which preserves entry order and
annotations — see [README Completeness](./governance-readme-completeness.md).

## Related

- [File Naming](./file-naming.md) — the kebab-case base rule.
- [Word-Budget Remediation](./governance-word-budget-remediation.md) — splits are the largest source
  of non-step ordinals.
