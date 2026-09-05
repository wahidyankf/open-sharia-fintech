---
title: "The Sixteen Rules (1-6)"
description: "Rules 1-6: visual-parity gate, primitive naming, responsive parity, filter coverage, value-bearing tests, labeled numbers."
category: explanation
subcategory: development
tags:
  - quality
  - planning
  - ui
  - verification
  - testing
  - deployment
created: 2026-06-19
when_to_use: "Use when authoring a UI plan and checking against rules 1-6."
---

# The Sixteen Rules (1-6)

1. **(Authoring) A UI plan MUST carry a manual visual-parity gate, executed before archival.** Gap:
   automated tests asserted DOM/behaviour presence; none compared the rendered pixels to the
   approved `assets/` mockups, and the workflow's Playwright visual step was skipped. Apply: any
   plan that ships UI carries an explicit, checked "screenshot vs each mockup, per breakpoint, per
   locale" step; `plan-checker` flags its absence the way it flags a missing design funnel. The
   sign-off step MUST save screenshots to `evidence/` and reference them in `delivery.md`; a
   step without committed evidence is not signed off. See [Evidence Capture Convention](.././evidence-capture.md).

2. **(Authoring) Name the design-system primitive in the delivery step — never assume it.** Gap:
   the shared `Tabs`/`Badge`/`Toggle` primitives existed and were exported, yet the build
   hand-rolled bare `<button role="tab">` / `<span>` / `<select>`. Apply: when a mockup shows a
   known primitive (tabs, badge, segmented control, card), the step names the primitive and asserts
   its presence.

3. **(Authoring) Responsive parity is a first-class, per-breakpoint deliverable.** Gap: `*-mobile`
   and `*-tablet` mockups existed in `assets/` but no delivery step bound them; the build shipped
   one wide desktop table. Apply: each responsive mockup gets its own RED/GREEN step plus a
   viewport-specific visual assertion (see Rule 9 for the technique).

4. **(Authoring) Filter/scope coverage MUST be exhaustive over the cascade.** Gap: the city-only
   filter path (city set, country/region null) had no test, so a "filter silently ignored" bug
   shipped. Apply: for any cascading filter, the plan's Gherkin enumerates **each** level
   independently (region-only, country-only, city-only) and the meaningful combinations — not just
   the happy cascade.

5. **(Authoring) Ordering/threshold features need value-bearing tests, not presence tests.** Gap: a
   "a divider exists + some rows are dimmed" assertion held true under both correct and **inverted**
   logic. Apply: assert concrete positions/identities ("Staff SWE is above the minimum, SWE I
   below") and choose fixture inputs that actually produce the split — probe the data when
   authoring. (See Rule 12 for the execution-side sharpening.)

6. **(Authoring) Every displayed number needs a visible label.** Gap: a preview rendered eight bare
   currency chips with no legend. Apply: a plan presenting computed figures requires a label/legend
   for each value in its acceptance criteria.
