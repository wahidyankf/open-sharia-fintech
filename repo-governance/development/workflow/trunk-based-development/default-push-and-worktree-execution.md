---
description: Overview framing that the four delivery modes are defined once canonically, and this document explains how each plays out for TBD and worktree execution.
when_to_use: Use as the entry point before reading the specific delivery-mode child documents that follow.
---

# Default Push and Worktree Execution

This section clarifies the default delivery mode and how git worktrees relate to it. The default is
consistent across all execution contexts and is defined once, canonically, in the
[Plans Organization Convention — Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode):
four modes (`worktree-to-pr` **(default)**, `worktree-to-origin-main`, `main-to-origin-main`,
`main-to-pr`), each fixing a work location, an integration target, and a merge authority, resolved by
a three-tier precedence (invocation argument > plan field > default). This document does not redefine
that vocabulary — it explains how each mode plays out for TBD and for worktree execution specifically.
