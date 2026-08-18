---
title: "Quality Gates: Selective Adversarial Verification (D4)"
description: "Adversarial re-verification for selected findings."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
  - boundary-rules
created: 2026-07-23
when_to_use: "Use when a finding warrants adversarial re-verification."
---

# Selective Adversarial Verification (D4)

For most findings, the coordinator's tool-verify function is enough. For **high-risk** diffs, this
convention adds a second, independent verification pass that runs before the finding is posted at
all — a deliberately narrow, **adversarial** check reserved for the categories most likely to hide
subtle, high-consequence defects:

- **High-risk scope**: authentication/authorization, payments, database or schema migrations,
  security-sensitive code paths, and public-API or contract surfaces.
- **The verification pass**: a second, independent reviewer re-derives the finding from the diff
  rather than merely rubber-stamping the first specialist's conclusion — the adversarial posture
  is the point, not agreement.
- **Cross-model-diversity note**: the verifier should ideally differ in model family from the
  original finder. Two passes from the same model family risk sharing the same blind spots, which
  defeats the purpose of a second, independent pass.

This high-risk scope is deliberately narrower than the
[risk-tier fan-out's security-sensitive path list](./cost-control-noise-control-mechanics-risk-tier-fan-out.md) that forces all nine
specialists into a review — a diff can be `full`-tier without touching auth, payments, migrations,
or a public API, in which case this adversarial pass does not apply. The two mechanics are related
but distinct: one controls how many specialists review a diff, the other controls whether a
second, independent pass re-checks a specific finding before it is posted.
