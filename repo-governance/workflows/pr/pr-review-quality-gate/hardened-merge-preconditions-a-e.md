---
title: "PR-Review Quality Gate — Hardened Merge Preconditions (a)-(e)"
description: "The normative five-lettered merge preconditions: route-specific review complete, zero blocking findings, branch up-to-date with main, gates green, and surface-conditional tester gates resolved."
when_to_use: "Use when verifying every precondition before merging a PR, or when citing the (a)-(e) letters elsewhere — this is their normative source."
---

# Hardened Merge Preconditions — (a) Through (e)

Being **done** is necessary but not sufficient to merge. A PR merges only when **all five** of the
following hold:

- **(a)** The PR completed its route-specific review: an eligible PR reached
  [its clean exit](./probe-variation-and-exit.md) within its configured ceiling,
  while a noneligible PR has recorded classifier evidence and a green
  `pr-quality-gate.yml` run. A `blocked` route status always blocks merge.
- **(b)** **0 code-related CRITICAL + 0 HIGH + 0 MEDIUM findings outstanding.** A reasoned reject or
  deferral does not erase an unresolved code finding; it remains blocking until resolved in the
  PR's code, shown false with recorded evidence, or **scope-deferred with a filed follow-up** per
  the [Scope Guard](./scope-deferral-exit.md).
- **(c)** The branch is **up-to-date with the latest `origin/main`** at merge time. If it is behind,
  bring it forward by a **non-destructive forward update** — `git fetch origin` then
  `git merge --ff-only origin/main`, or an ordinary forward merge. **Never** a shared-history rewrite,
  and never `reset --hard` or a force-push (see the
  [No Destructive Git Operations Convention](../../../development/workflow/no-destructive-git-operations.md)
  and the [Git Push Safety Convention](../../../development/workflow/git-push-safety.md)).
- **(d)** **All PR quality gates are green** — aggregate CI covers the exact repository/head/base;
  no separate local proof is required.
- **(e)** The **surface-conditional tester gates have been run and their defect findings resolved.**
  The rule this clause enforces is: **every PR that changes behavior a user or caller can reach must
  be exercised through that behavior before it merges.** The surface list below is a routing table for
  that rule, never its boundary — a surface absent from the list does not become exempt by omission.
  - a UI-bearing PR runs **both** UI gates ([`ui/ui-quality-gate.md`](../../ui/ui-quality-gate.md)
    static and [`web/web-ux-test-fixing-planning.md`](../../web/web-ux-test-fixing-planning.md) running
    triad);
  - an API/BE-bearing PR runs [`api/api-quality-gate.md`](../../api/api-quality-gate.md);
  - a PR bearing several of these runs each one.

  **When a PR changes reachable behavior on a surface with no gate listed above** — a CLI such as
  `apps/rhino-cli/**`, a library under `libs/`, a hook, or a CI workflow — it is **not** exempt. The
  author exercises the changed behavior through its own interface (for a CLI: invoke the affected
  subcommands and record the observed output; for a library: exercise it through a consuming caller,
  not only its unit tests) and records what was run and what was observed. Exemption is available
  **only** for a PR that changes no reachable behavior at all — docs, comments, or a pure refactor
  with no behavioral delta — and that claim is recorded **explicitly**, with its classifier evidence,
  rather than left implicit.

See [Hardened Merge Preconditions — Notes and Merge Mechanics](./hardened-merge-preconditions-notes.md) for the normative-lettering note, the merge-command mechanics, and the done-boundary diagram.
