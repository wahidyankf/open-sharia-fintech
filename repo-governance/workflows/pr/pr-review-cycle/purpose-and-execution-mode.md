---
title: "PR-Review Cycle — Purpose and Execution Mode"
description: "Defines the optional cycle's purpose and strictly sequential pass-to-fixer execution."
when_to_use: "Use when deciding whether to invoke pr-review-cycle or checking its concurrency rule."
---

# Purpose and Execution Mode

## Purpose

Run a bounded, explicitly requested maker-to-fixer cycle. Each semantic iteration invokes
[`pr-review`](../pr-review.md), authenticates its pass record, optionally fixes posted findings,
waits for exact-head/base aggregate PR CI, and checks cycle-local credit.

The cycle is never a default plan step, classifier, merge precondition, or substitute for the
repository's ordinary PR quality gate. Risk tier, file type, plans, and delivery mode cannot enable
it. Only direct user instruction or a plan step recorded because of that instruction may do so.

## Execution Mode

Run iterations sequentially. Within each `pr-review` pass, route-selected specialists may fan out
concurrently. Never start the fixer before the pass record authenticates, and never start a later
pass before the prior fixer's pushed head has exact-head/base green CI.

For a public/private pair, preserve the existing authenticated handoff and source-merge checks.
Those checks coordinate an explicitly requested paired cycle; they do not make either sibling's
cycle mandatory.
