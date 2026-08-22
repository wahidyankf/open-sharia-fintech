---
title: "PR-Review Quality Gate — Scope-Deferral Is the Only Other Exit"
description: "How a valid finding deferred on scope grounds leaves the outstanding ledger, so the loop can still reach a clean exit."
category: explanation
subcategory: workflows
created: 2026-08-22
when_to_use: "Use when a reviewer or the fixer defers a valid MEDIUM+ finding as out of scope, or when checking merge precondition (b)."
---

# Scope-Deferral Is the Only Other Exit

A valid MEDIUM+ code-related finding deferred on
[scope grounds](./scope-guard-no-scope-creep.md) cannot be fixed in this PR and is not false.
Without a route out of the ledger it stays outstanding forever and the loop blocks at the ceiling —
a correct finding, correctly deferred, would then be indistinguishable from an unfixed defect.

It leaves the ledger **only** by being recorded elsewhere: file the follow-up, link it on the
thread, and merge precondition (b) is satisfied.

**No filed follow-up, no deferral.** A deferral without a link is an unresolved finding wearing a
different word, and the loop treats it as one.
