---
title: "User-Facing Delivery Hardening Convention"
description: Sixteen durable rules for planning, executing, verifying, and archiving user-facing feature work so design-parity and behavioural defects cannot ship past green gates
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
when_to_use: "Use when planning, executing, or archiving a user-facing (UI or API) feature-change plan."
---

# User-Facing Delivery Hardening Convention

This convention states sixteen durable rules -- spanning authoring, execution, and verification -- so design-parity and behavioural defects cannot ship past green automated gates on user-facing work.

## Documents

- [Principles and Conventions Implemented/Respected](./user-facing-delivery-hardening/principles-and-conventions-implemented-respected.md) — Principles/conventions implemented. Use to trace this convention's rationale.
- [Scope](./user-facing-delivery-hardening/scope.md) — What this convention applies to. Use when checking whether this convention applies to a plan.
- [The Sixteen Rules (1-6)](./user-facing-delivery-hardening/the-sixteen-rules-1-6.md) — Rules 1-6: visual-parity gate, primitive naming, responsive parity, filter coverage, value-bearing tests, labeled numbers. Use when authoring a UI plan and checking against rules 1-6.
- [The Sixteen Rules (7-10)](./user-facing-delivery-hardening/the-sixteen-rules-7-10.md) — Rules 7-10: green gates insufficient, theme-token colors, per-breakpoint responsive, done means verified. Use when authoring or verifying a UI plan against rules 7-10.
- [The Sixteen Rules (11-14)](./user-facing-delivery-hardening/the-sixteen-rules-11-14.md) — Rules 11-14: deploy config as code, distinguishing assertions, checkbox lockstep, clean re-entry. Use when executing or verifying a UI plan against rules 11-14.
- [The Sixteen Rules (15)](./user-facing-delivery-hardening/the-sixteen-rules-15.md) — Rule 15: the near-end web-UI live tester triad retest before archival. Use when a web-UI feature-change plan is nearing archival.
- [The Sixteen Rules (16, part 1)](./user-facing-delivery-hardening/the-sixteen-rules-16-part-1.md) — Rule 16: the near-end api-exploratory-tester retest before archival. Use when an API feature-change plan is nearing archival.
- [The Sixteen Rules (16, part 2, and progressive-disclosure caution)](./user-facing-delivery-hardening/the-sixteen-rules-16-part-2.md) — Rule 16's surface-conditional gate mapping, plus the progressive-disclosure density caution. Use when mapping a plan's surface to its required tester gate, or evaluating a density fix.
- [Examples](./user-facing-delivery-hardening/examples.md) — Worked examples of the sixteen rules applied. Use for a concrete example of these rules applied.
- [Tools and Automation](./user-facing-delivery-hardening/tools-and-automation.md) — The agents and gates that enforce these sixteen rules. Use when locating the automated enforcement for one of the sixteen rules.
- [References](./user-facing-delivery-hardening/references.md) — References and related documentation for this convention. Use when you need a related workflow or convention document.
