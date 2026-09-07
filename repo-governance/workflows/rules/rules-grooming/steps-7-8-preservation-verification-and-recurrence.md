---
title: "Steps 7-8 — Preservation Verification and Recurrence"
description: The post-run obligation diff that proves nothing was lost, the revert path when it fails, and the log entry that arms the next sweep's trigger.
when_to_use: Use when verifying a completed grooming sweep preserved every obligation, or recording the run.
---

# Steps 7-8 — Preservation Verification and Recurrence

## Step 7: Preservation Verification (Sequential)

This is the step the whole workflow exists to be able to pass. Every other step is a way of
arriving here with a diff that comes out empty.

**Agent**: `rules-checker`

**Procedure**: Re-run the Step 2 obligation inventory against the post-hand-off corpus under
identical extraction rules, and write it to
`local-tmp/rules-grooming/rules-grooming__<slug>__obligations-post.md`. Diff it against the pre-run
snapshot.

The run passes only if:

- **No obligation disappeared** except those on the approved retirement list. Any other
  disappearance is a semantic loss.
- **No obligation changed** in audience, pass condition, violation condition, qualifier, or
  exception. A changed entry means a reduction rewrote meaning, which no class permits.
- **Every surviving obligation is reachable** from at least one surface that binds its audience. An
  obligation that survives in text but became unreachable is lost in the way that matters.
- **Every `See` link written by a duplication reduction resolves**, and its target covers every
  case the removed text covered.

- **Depends on**: Step 6.
- **On failure**: Halt, and identify the propagation delivery that introduced the loss. Reverting
  that delivery is itself a rule edit, so it is handed back to propagation — grooming does not
  revert by writing. The run ends `halted` with the offending item recorded, and the loss is
  reported to the maintainer whether or not the revert lands.

A halt here is a finding about the workflow, not only about the item. Record which class produced
the loss; a class that produces one is a candidate for tightening its admission rule.

## Step 8: Record and Recurrence (Sequential)

**Procedure**: Append the run record to the corpus grooming log, then re-evaluate the recurrence
trigger against the post-run census so the next sweep's due date is set by measurement rather than
by assumption.

The record carries: run date, `scope`, `classes`, the census before and after, the metrics delta
(file count, total lines, metadata ratio), per-class item counts by disposition, every retirement
with its rationale, every deferred item, and the propagation PRs.

Deferred items carry forward. A rediscovered candidate that was previously rejected is recorded as
rejected-again rather than presented as new, so a maintainer is never asked the same question
twice without being told they already answered it.

- **Output**: Log entry, including the `> Last groomed: YYYY-MM-DD` line the trigger reads.
- **Success criteria**: The log entry is written even when the run ended `partial` or `halted`. A
  run that leaves no record is indistinguishable from one that never happened, and the next sweep
  would then repeat its rejected candidates.
