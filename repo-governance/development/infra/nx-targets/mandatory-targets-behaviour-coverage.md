---
title: "Mandatory Static Behaviour Coverage"
description: "Contract for test:coverage:behaviour and the per-adapter static coverage validators"
category: explanation
subcategory: development
tags: [nx, targets, gherkin, coverage]
created: 2026-02-23
when_to_use: "Use when adding or debugging static Gherkin coverage validation."
---

# Mandatory Static Behaviour Coverage

Every behaviour owner and dedicated E2E project exposes `test:coverage:behaviour`. It recursively
discovers the canonical corpus and statically rejects empty/malformed features, missing explicit
When/Then steps, undefined or ambiguous steps, unused bindings, incomplete applicable adapters,
missing Unit proof, forbidden `@wip`/positive selection tags, and invalid exemptions.

Layer-specific `test:coverage:<layer>` targets prove exactly-one implementation or a valid
higher-layer exemption for every expanded scenario. Coverage targets never execute tests and never
depend on runtime targets. Every applicable validator runs through `test:quick`, directly or via
`test:coverage`.

Static coverage cannot prove that a binding invokes production code or observes independent
evidence. Material changes also require the
[Gherkin implementation review](../../../workflows/gherkin-implementation-review.md).
