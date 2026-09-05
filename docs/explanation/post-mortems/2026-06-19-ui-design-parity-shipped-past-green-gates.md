---
title: "Post-Mortem: ayokoding-www Calculator — Bland, Buggy UI Shipped Past Green Gates"
description: A user-facing calculator was validated to zero findings, archived to plans/done/, and shipped to production bland, off-design, and carrying two calculation bugs — while every automated gate was green.
category: explanation
subcategory: post-mortem
doc_status: reviewed
tags:
  - post-mortem
  - ui
  - planning
  - verification
created: 2026-06-19
---

# Post-Mortem: ayokoding-www Calculator — Bland, Buggy UI Shipped Past Green Gates

| Field              | Value                                      |
| ------------------ | ------------------------------------------ |
| Incident date      | 2026-06-19                                 |
| Investigation date | 2026-06-19                                 |
| Severity           | Sev-3 — Incorrect production functionality |
| Status             | Resolved                                   |
| Author             | Engineering (blameless retrospective)      |

## Summary

The ayokoding-www Cost-of-Living / Salary-Savings Calculator was implemented, validated to **zero
findings** by `plan-execution-checker`, archived to `plans/done/`, and deployed to production — all
with typecheck, lint, unit (1300+), E2E, and CI green. On manual review of the live site the feature
was found **bland and off-design** (unstyled tabs, plain text where colored badges/segmented
controls were specified, one wide table instead of the responsive mockups) and carrying **two
calculation bugs** (a city filter silently ignored, and an inverted minimum-role ranking that placed
higher-savings senior roles below the "does not qualify" divider). No outage occurred; the defect was
incorrect and off-spec user-facing output served in production.

## Impact

- **Surface**: `https://ayokoding.com/[en|id]/tools/cost-of-living-calculator` (public tool).
- **Users**: anyone using the calculator between first deploy and remediation saw an off-design UI
  and, on the Minimum-role tab, an **incorrect ranking** (a real correctness defect, not cosmetic).
- **Duration**: roughly one working session from first production deploy to full remediation.
- **MTTD**: effectively only on human review — no automated signal flagged it (the gates were green).
- **MTTR**: same session, across several fix + redeploy cycles.

## Detection

A human opened the production site and observed the rendered result against the approved design
mockups. Category: **User Report**. No monitoring, test, or gate detected any of the defects.

## Timeline

| Time (WIB UTC+7) | Event                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------ |
| 2026-06-19 early | Calculator plan executed; `plan-execution-checker` reports zero findings.                  |
| 2026-06-19 early | Plan archived to `plans/done/`; feature deployed to `prod-ayokoding-www`.                  |
| 2026-06-19       | First production deploy fails: `vercel.json` `buildCommand` points at a moved path.        |
| 2026-06-19       | Build path fixed; redeploy succeeds; live URL still 404 until CDN/build settles.           |
| 2026-06-19       | Human opens production: UI is bland and off-design vs the mockups.                         |
| 2026-06-19       | Plan reopened to `plans/in-progress/`; styling reconciled to web-ui primitives + brand.    |
| 2026-06-19       | City-filter-ignored bug found and fixed; min-role ranking-inversion bug found and fixed.   |
| 2026-06-19       | Full responsive transform (mobile cards + tablet columns) implemented across three tables. |
| 2026-06-19       | Production re-verified with Playwright at desktop + mobile, both locales; clean.           |

## Root Cause

The **done/archival criterion for user-facing work relied on automated gates plus zero validation
findings, with no production visual or value-bearing sign-off**. The plan-execution workflow's manual
behavioural-verification step (visual check against the mockups) was not performed before archival.
Automated tests asserted **presence** (a `tablist` exists, a divider exists, a badge element exists)
but never **parity** (does it match the mockup?) or **value** (are the right rows above the divider?).
Because nothing compared the rendered result to the design, design-parity gaps and an inverted-logic
ranking were invisible to every gate.

## Trigger

The calculator plan was executed and validated to zero findings, then archived and deployed. The
specific proximate event was declaring the work "done" on the strength of green gates without the
mandatory manual visual verification (workflow Step 2d) against the `assets/` mockups.

## Contributing Factors

- **Presence-only assertions.** Tests asserted element existence, which passes under both correct
  and inverted logic and under bare, unstyled markup.
- **Available primitives not mandated.** The shared `web-ui` `Tabs`/`Badge`/`Toggle` primitives were
  exported but the plan did not require their use, so hand-rolled bare elements satisfied the tests.
- **Responsive mockups unbound.** `*-mobile`/`*-tablet` mockups existed in the plan's `assets/` but
  no delivery step bound them; a single wide table shipped.
- **A trivially-satisfiable test fixture.** The min-role ordering scenario used an input that cleared
  every role, so the qualifying/non-qualifying split was never actually exercised.
- **Untested deploy configuration.** A moved source path left `vercel.json`'s `buildCommand` stale;
  local builds were green while the production build broke.

## Resolution & Mitigations

- **Applied fixes (this incident):** reconciled the UI to web-ui primitives + the ayokoding brand
  (blue tabs/toggles, green/amber/red scheme badges, labelled preview, city-detail card); fixed the
  city-filter-scope bug and the min-role ranking inversion (with a value-bearing regression guard);
  implemented the full responsive transform; corrected the stale deploy path; re-verified production
  with Playwright per breakpoint/locale.
- **Open root-cause fix (tracked in Action Items):** codify the missing gates as durable rules so
  the class of defect cannot recur — delivered as the
  [User-Facing Delivery Hardening Convention](../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
  (fourteen rules), propagated across the governance + agent surface in all three sibling repos.

## Action Items

| #   | Action                                                                                                                                          | Owner       | Priority | Ticket | Status |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | -------- | ------ | ------ |
| 1   | Author + propagate the User-Facing Delivery Hardening Convention (14 rules) across the 3 repos                                                  | Engineering | P0       | —      | Done   |
| 2   | `plan-checker` flags missing visual-parity gate, raw-value mockup colors, presence-only ordering tests, missing per-breakpoint responsive steps | Engineering | P1       | —      | Open   |
| 3   | `plan-execution-checker` blocks archival until production visual sign-off + deploy-config smoke test are recorded                               | Engineering | P1       | —      | Open   |
| 4   | `plan-maker` emits delivery steps for rules 1–8 by default on UI-bearing plans                                                                  | Engineering | P1       | —      | Open   |

## What Went Well

- Once a human looked, every defect was found, root-caused, and fixed in the same session.
- The fixes were captured as durable, propagated governance rather than a one-off patch.
- Reopening the plan (rather than silent edits) kept the trunk and the plan record honest.
- **Where we got lucky:** the incorrect ranking was caught quickly by review. With no visual/value
  sign-off in the pipeline, a less-obvious correctness defect could have persisted unnoticed.

## Lessons Learned

The full set of fourteen generalizable lessons is codified in the
[User-Facing Delivery Hardening Convention](../../../repo-governance/development/quality/user-facing-delivery-hardening.md).
The headline insights:

- **Green gates are necessary, not sufficient.** For user-facing work, "zero findings + CI green" is
  not "done" — a production visual + value-bearing sign-off against the mockups is required before
  archival.
- **Assert parity and value, not presence.** Tests must distinguish correct from a plausible bug, and
  fixtures must actually exercise the branch.
- **Name the primitive; bind every breakpoint; treat deploy config as code.**

## References

- [User-Facing Delivery Hardening Convention](../../../repo-governance/development/quality/user-facing-delivery-hardening.md) — the fourteen durable rules this incident produced.
- [Manual Behavioural Verification Convention](../../../repo-governance/development/quality/manual-behavioural-verification.md) — the verification baseline the convention hardens.
- [Plan Execution Workflow](../../../repo-governance/workflows/plan/plan-execution.md) — finalization/archival gate.
- Plan: `plans/in-progress/ayokoding-www-salary-savings-calculator/` (delivery log §7.6–§7.7 record the fixes and lessons as-built).
