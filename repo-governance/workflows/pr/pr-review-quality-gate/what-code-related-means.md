---
title: "PR-Review Quality Gate — What Code-Related Means"
description: "Defines the code-related qualifier that gates the loop's exit, its ceiling block, and merge precondition (b), so a prose-only PR is not accidentally exempt."
when_to_use: "Use when deciding whether an outstanding MEDIUM/HIGH/CRITICAL finding blocks the loop or a merge."
---

# What Code-Related Means

Every exit, block, and merge rule in this workflow is gated on **code-related** MEDIUM/HIGH/CRITICAL
findings, not on findings in general. The qualifier is doing real filtering work, so it needs a
definition rather than an intuition.

**A finding is code-related when it names a defect in an artifact this PR ships.** The shipping
artifact is whatever the PR exists to put on `main`: executable source, configuration, specs, and —
this is the half most easily misread — governance prose, agent definitions, and skill files. On a
PR whose whole purpose is to change the rules, the rules **are** the artifact. A CRITICAL in a
convention blocks exactly as a CRITICAL in a function does.

**Two things are not code-related**, and neither blocks:

- **The correction record.** `plans/**` after cycle 1 — the prose the loop itself authors as it
  works. See the correction-record freeze in
  [Loop-Exit and Block Rules](./loop-exit-and-block-rules.md). On a plans-only PR the plan is the
  shipping artifact, so the exclusion does not apply.
- **The review conversation.** Review comments, replies, and disposition blocks describe the work;
  they are not the work.

## Why the Definition Has to Be Written Down

Read literally as "about executable code", the qualifier would make the loop vacuous on any PR that
ships only prose — the exit condition would be satisfied on cycle 1 no matter how many real defects
the specialists found, because none of them would be about code. Most PRs in this repository are
exactly that shape.

The loop has always been run the broad way in practice. That is the point: a rule whose correct
reading exists only in observed behaviour is one careful reader away from being applied the other
way, and the reader who applies it literally will be the one merging a CRITICAL.

## The Test

Ask what the PR would be reverted for. If a reader on `main` a month from now would call the finding
a defect in what shipped, it is code-related and it blocks.
