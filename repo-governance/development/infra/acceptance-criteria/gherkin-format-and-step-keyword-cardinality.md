---
title: "Gherkin Format and Journey Coherence"
description: "Gherkin keyword syntax and the coherent-journey rule for repeated primary steps"
category: explanation
subcategory: development
tags: [acceptance-criteria, gherkin, bdd]
created: 2026-01-04
when_to_use: "Use when writing or reviewing a Gherkin scenario."
---

# Gherkin Format and Journey Coherence

Use `Feature` for the capability, optional `Rule` blocks for business-rule groupings, `Background`
for shared preconditions, and `Scenario`/`Scenario Outline` for observable examples.

Every scenario must contain an explicit `When` and `Then`. Use `Given` for preconditions, `When`
for actions/events, and `Then` for independently observable outcomes. `And` and `But` may improve
readability when a step continues the previous semantic phase.

A scenario may repeat `Given`, `When`, or `Then` when the steps form one continuous user journey.
Do not force `And`/`But` or split an existing journey merely to satisfy keyword uniformity. Split
only when actions or outcomes are independently meaningful, can pass/fail separately, or describe
unrelated behaviour.

`Scenario Outline` examples expand into separate executable scenarios. Each expanded row must map
to every applicable adapter under the
[BDD standard](../../behaviour-driven-development.md); syntax/cardinality cannot substitute for
semantic implementation review.

```gherkin
Scenario: A member completes one continuous recovery journey
  Given a member has an expired session
  When the member requests a recovery code
  Then the service records the request
  When the member submits the valid code
  Then the service restores the session
```
