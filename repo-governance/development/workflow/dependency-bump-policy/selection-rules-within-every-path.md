---
title: "Selection Rules Within Every Path"
description: The two rules — recency and functional stability — that narrow a chosen path's eligible versions down to the single version to pin.
category: explanation
subcategory: development
tags:
  - dependencies
  - security
  - versioning
  - reproducibility
  - workflow
created: 2026-05-15
when_to_use: Use once a path (A, B, or C) is chosen, to select the exact version to pin from that path's eligible set.
---

# Selection Rules Within Every Path

Once a path is chosen, two rules narrow the eligible set to the single version to pin. Both apply on top of paths A, B, and C — they never override the 60-day, CVE, or LTS constraints.

## Rule 5a — Recency (prefer the most recent eligible version)

Among ALL versions that satisfy the chosen path's constraints (latest LTS patch for Path A; released ≥ 60 days ago AND CVE-clean for Path B; CVE-patched for Path C), always select the **most recent eligible** version. Never pin an older eligible version when a newer eligible one exists.

Rationale: staying as current as the constraints allow minimizes the upgrade gap and accumulated drift, while rules 1–4 still bound how new "current" is allowed to be.

## Rule 5b — Functional Stability (reject versions with known fatal defects)

The selected version MUST be free of known **fatal functional defects** for the capability it provides. Reject a candidate version — even when it is CVE-clean and older than 60 days — if any of the following hold:

- It is **yanked or deprecated** on its registry (`npm view <pkg> deprecated`, crates.io yank flag, NuGet unlisted, etc.)
- It carries an **open release-blocker / regression advisory** from the upstream maintainer
- It has a **widely-reported broken-build, data-loss, or crash bug** affecting its primary function

When the newest eligible version fails this gate, fall back to the most recent eligible version that passes, and record the skip and reason (see the
[`FUNCTIONAL-HOLD` clearance status](./cve-clearance-process.md#cve-clearance-process-mandatory-for-every-bump)).

Sources to check: the project's GitHub releases/issues page ("do not use" notices, yanked tags), the package registry deprecation flag, and the changelog/release notes known-issue callouts.
