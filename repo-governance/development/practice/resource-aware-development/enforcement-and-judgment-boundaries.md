---
title: "Enforcement and Judgment Boundaries"
description: Which gates check this practice, and which parts are unenforced by decision with their reasons.
category: explanation
subcategory: development
tags:
  - resource-management
  - parallelism
  - development
  - tooling
created: 2026-09-05
when_to_use: Use when asking how a resource-aware obligation is enforced, or why one deliberately is not.
---

# Enforcement and Judgment Boundaries

Bootstrap, config, entrypoint, mapping, smoke, and upstream scheduler tests gate the executable
contract. Plan validation checks guards, classes, edges, and justified serialization. Novel class
choice and safe human retry remain **unenforced by decision** because they require intent, and
container init because no OSE container runs HIPPO yet.
