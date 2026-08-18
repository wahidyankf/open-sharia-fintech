---
title: "Future Work: Cost and Latency Budgeting"
description: "A future per-PR cost and latency budget."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
  - boundary-rules
created: 2026-07-23
when_to_use: "Use when proposing a cost/latency budget for review."
---

# Cost and Latency Budgeting

Cloudflare's own production system — the one this convention's fan-out/coordinator shape is modeled
on (see [Cost-Control & Noise-Control Mechanics](./cost-control-noise-control-mechanics-risk-tier-fan-out.md)) — reports a
median cost of ≈$1 per review. Applied to this repo's shape, a `full`-tier PR fanning out to all
nine specialists across the fixed three-cycle ceiling costs roughly ≈$1 × 9 specialists × 3 cycles
per PR, bounded downward by the [risk-tier fan-out (D12)](./cost-control-noise-control-mechanics-risk-tier-fan-out.md): a `trivial` PR
runs the coordinator alone and a `lite` PR fans out to only four specialists, so its actual per-PR
cost sits well under that ceiling. This convention does not yet mandate a specific budget or alert
threshold. It recommends that whoever owns the
[Post-Cutover Monitoring Plan](./post-cutover-monitoring-rollback-monitoring-plan-part-1.md)'s cost/latency-per-review metric also
track the absolute per-PR dollar figure over time, not only the per-tier trend, so a repo-wide cost
creep is visible before it grows into a rollback-trigger-level concern.
