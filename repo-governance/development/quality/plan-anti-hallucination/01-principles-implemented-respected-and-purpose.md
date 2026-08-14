---
title: "Principles/Purpose"
description: "Principles implemented, and why this convention exists."
category: explanation
subcategory: development
tags:
  - plans
  - ai-agents
  - factual-validation
  - anti-hallucination
  - web-research
  - verification
created: 2026-05-03
when_to_use: "Use to trace this convention's rationale."
---

# Principles Implemented/Respected and Purpose

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Every non-trivial factual claim in a plan carries an inline confidence label (`[Repo-grounded]`, `[Web-cited]`, `[Judgment call]`, `[Unverified]`). The author's confidence is explicit text, not implicit tone.
- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: When verification fails, the author refuses to write the claim rather than papering over uncertainty. The defect surfaces at authoring time where it is cheapest to fix.
- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: Verification commands are repeatable. A reader audits the same claim by running the same `Glob`, `Grep`, `WebFetch`, or `web-researcher` invocation the author ran.
- **[Documentation First](../../../principles/content/documentation-first.md)**: External claims cite the source inline (URL + access date + excerpt). Future readers verify the claim from the plan alone, even after the URL rots.

## Purpose

This convention exists to:

- Establish bright-line **pre-write verification rituals** for every category of factual claim that appears in plan content (file paths, Nx targets, package versions, API signatures, command syntax, KPIs).
- Make **repo-grounding** mandatory — every internal reference (file path, symbol, project, target) MUST be verified to exist in the current repo before being written.
- Make **web-researcher delegation** the default for any external claim that requires more than a single-shot fetch.
- Establish **refuse-on-uncertainty** as a positive virtue — the author who writes `[Unverified]` or refuses the claim entirely is preferred over the author who writes a plausible-sounding fabrication.
- Catalog known **hallucination anti-patterns** so plan-checker can flag them mechanically and plan-fixer can rewrite them deterministically.
- Align the four plan agents (`plan-maker`, `plan-checker`, `plan-fixer`, `plan-execution-checker`) and the two plan workflows (`plan-quality-gate`, `plan-execution`) to one verification standard.
