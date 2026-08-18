---
title: "Exemptions"
description: "Narrow exemptions to knowledge capture."
category: explanation
subcategory: development
tags:
  - knowledge-capture
  - learnings
  - plans
  - triage
  - safety-gates
  - post-mortems
created: 2026-07-05
when_to_use: "Use when checking a plan's exemption status."
---

# Exemptions

Pure-docs and trivial plans MAY skip elaborate Knowledge Capture — this mirrors the existing
exemption pattern in [Feature Change Completeness](../feature-change-completeness/two-paths-with-a-plan-and-without-a-plan.md#two-paths-with-a-plan-and-without-a-plan)
for the specs/Gherkin two-path rule. A one-line rename, a single broken link fix, or an equivalently
trivial plan does not require a populated `learnings.md`; the explicit "none" escape above (or an
equally explicit note in `delivery.md`) satisfies the requirement without inventing insight from a
change that had none to offer.
