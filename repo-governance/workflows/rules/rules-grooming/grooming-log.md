---
title: "Grooming Log"
description: One terse entry per rules-grooming run, carrying the census delta and the last-groomed date the recurrence trigger reads.
when_to_use: Use when evaluating the recurrence trigger, or recording a completed grooming run.
---

# Grooming Log

The durable record Step 8 appends to and Step 1's recurrence trigger reads. Entries are
deliberately terse: one line of prose per run plus its census row. The per-run manifest, candidate
evidence, and obligation snapshots live in `local-tmp/rules-grooming/` and are swept — this file is
what survives, so it carries only what the next run needs to decide whether it is due.

If this file approaches its word budget, drop the oldest rows: git history retains them, and the
trigger only ever reads the most recent.

> Last groomed: 2026-09-07

## Runs

| Date       | Classes       |         Files |             Lines |  Metadata ratio |                    Merged | Net lines |
| ---------- | ------------- | ------------: | ----------------: | --------------: | ------------------------: | --------: |
| 2026-09-07 | fragmentation | 3,173 → 3,074 | 165,006 → 163,461 | 19.64% → 19.06% | 99 shards into 69 parents |    −1,446 |

### 2026-09-07 — first run

Bootstrap run; the elapsed-time condition fired by definition with no prior baseline. Class
`fragmentation` only — `duplication` discovered 65 groups across 129 files but was deferred
unapproved, and `retirement` was not enabled.

Preservation proved twice: line-level containment (1,045 of 1,045 merged lines present) and an
obligation-set diff (3,661 before, 3,661 after, zero lost).

Surfaced six pre-existing broken links that had been latent inside shards, invisible to the index
gate because it inspects index references rather than shard bodies. All six repaired in the same
delivery.

Corrected seven defects in the workflow itself — see the delivery PR. The load-bearing ones: the
first-run trigger was undefined, making the workflow unrunnable; per-shard packing over-reported
yield 3.6×; and packing to the budget ceiling would have left 52 parents above 90% of budget,
against the word-budget convention's own statement that thresholds are capacity ceilings rather
than targets.

**Deferred to a later run**: 65 duplication groups; the `created:` frontmatter key (1,892 files),
withheld because the Timestamp convention mandates it and removing it is a convention change.
