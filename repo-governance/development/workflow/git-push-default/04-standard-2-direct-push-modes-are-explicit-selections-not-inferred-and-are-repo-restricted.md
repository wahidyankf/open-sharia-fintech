---
title: "Standard 2: Direct Push Modes Are Explicit Selections, Not Inferred — and Are Repo-Restricted"
description: Per-repository availability of the two direct-push modes, the explicit selection signals required, and the further content restriction on main-to-origin-main.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - push
  - trunk-based-development
  - ai-agents
created: 2026-04-25
when_to_use: Use when a plan or invocation might call for pushing directly to origin main, to confirm the repository allows it and a valid selection signal is present.
---

# Standard 2: Direct Push Modes Are Explicit Selections, Not Inferred — and Are Repo-Restricted

`worktree-to-origin-main` and `main-to-origin-main` push directly to `origin main` with no PR. Before
either signal below is even relevant, check repository availability first: in `ose-public`,
`main` is branch-protected against direct pushes (including for admins) — **neither
direct-push mode has an executable path there, full stop**.

In `ose-private`, both direct-push modes remain available only for infrastructure-as-code plans
(Terraform, Ansible, and equivalent state-changing infra work needing the primary checkout's real
secrets and local state). Every other plan, in both repositories, uses `worktree-to-pr`. See
[Plans Organization Convention §Per-Repository Delivery Mode Restrictions](../../../conventions/structure/plans/35-per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule)
for the full per-repository rule — this is the current binding constraint, and it applies before the
selection-signal and content-restriction tests below.

Within a repository where a direct-push mode remains available, either mode applies only when
explicitly selected — via an invocation argument or a plan's `## Delivery Mode` field. Absent that
explicit selection, the agent uses the `worktree-to-pr` default.

```bash
# worktree-to-origin-main — explicit selection only
git worktree add worktrees/<plan-id> -b <plan-id>
cd worktrees/<plan-id>
git add <files>
git commit -m "fix(scope): description"
git push origin main
```

Signals that constitute an explicit direct-push selection:

- An invocation argument naming `worktree-to-origin-main` or `main-to-origin-main`.
- A `## Delivery Mode` field in the plan declaring one of those two modes.

No other signal constitutes an implicit selection of a direct-push mode. The agent must not infer a
direct-push intent from:

- The size or risk of the change.
- A desire to "save time" or "skip review".
- Past sessions in which direct push was used.

**`main-to-origin-main` carries a further content restriction that `worktree-to-origin-main` does
not.** An explicit selection signal above is necessary but not sufficient for `main-to-origin-main` —
working directly in the primary checkout skips both PR review and worktree isolation, so it is valid
only when **one** of two conditions also holds:

1. the change set is **`.md` files only** (no source, config, spec, or generated-mirror files), or
2. the user has given **explicit, standing go-ahead** for that specific change.

Absent one of these two, use `worktree-to-pr` even with a valid selection signal present. See
[Plans Organization Convention — Delivery Mode](../../../conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode)
for the canonical statement of this restriction and its relationship to the
[Plan-Docs-Only Carve-Out](../../../workflows/plan/plan-planning/07-plan-docs-only-carve-out.md#the-plan-docs-only-carve-out-superseded--retired-in-ose-public).
