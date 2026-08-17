---
title: "Per-Repository Delivery Mode Restrictions (HARD RULE)"
description: States which delivery modes are actually available in ose-public and ose-private given each repo's branch-protection state.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when confirming which delivery modes are actually permitted in the specific repository a plan targets.
---

# Per-Repository Delivery Mode Restrictions (HARD RULE)

The four-mode table and the content restriction above state what is theoretically possible; this
subsection states what is **actually allowed per repository**, and is the narrower, binding rule.
Direct push to `origin main` is a scarce, protected capability going forward — not a convenience
available wherever a plan finds it easier.

- **`ose-public`**: `main` is branch-protected against direct pushes, **including for
  repository admins** — verified live via a legacy `/branches/main/protection` check. Note that a
  repo whose protection is expressed as a repository _ruleset_ is misreported as unprotected by that
  legacy endpoint alone, so check the rulesets API too before concluding a repo is unprotected.
  `worktree-to-origin-main` and `main-to-origin-main` are therefore **unavailable** here — no
  credential or role can push to `main` outside a merged PR.
- **`ose-private`**: `worktree-to-pr` is likewise the required mode for **every plan except**
  infrastructure-as-code plans (Terraform, Ansible, and equivalent state-changing infra work). Those
  plans use **`main-to-origin-main`**, because they need the real `.env` credentials and local
  infrastructure state (Terraform state and similar) that exist only in the primary checkout — never
  in a worktree provisioned fresh from `origin/main` — per the
  [secret- and state-dependent infra operations rule](../../../workflows/plan/plan-execution/14-enter-worktree-preconditions-and-work-branch.md#0-enter-the-designated-worktree-sequential-hard-gate).
  This is narrower than the general `.md`-only / explicit-go-ahead content restriction above: the
  carve-out is granted for the **infrastructure secrets/state reason specifically**, not for any
  `.md`-only plan-docs change or ad-hoc go-ahead. A non-IaC, plan-docs-only change in `ose-private`
  uses `worktree-to-pr` like everything else — the old two-condition test no longer applies there.
  **`ose-private`'s own branch-protection state is unverified as of this PR** — its rules API returned
  `403 Upgrade to GitHub Pro` when checked live, so this rule's restriction there rests on a
  convention-enforced (not independently confirmed mechanically-enforced) footing until it is checked
  with sufficient API access.

See [Per-Repository Delivery Mode Restrictions — Enforcement and File Naming](./36-per-repository-restrictions-enforcement-and-file-naming.md) for `main-to-pr`'s status in `ose-public` and the enforcement rules.
