---
title: "Web Research Delegation Convention"
description: Normative rule requiring AI agents to delegate public-web information gathering to the web-researcher delegated agent, with a narrow documented exception list
category: explanation
subcategory: conventions
tags:
  - ai-agents
  - web-research
  - delegation
  - factual-validation
  - governance
created: 2026-04-16
when_to_use: Read this before adding WebSearch or WebFetch to an agent, skill, or workflow, or before auditing one for compliance.
---

# Web Research Delegation Convention

AI agents frequently need facts that live outside the repository — current API signatures, library versions, specification wording, best-practice guidance. Without a rule, every agent re-implements its own ad-hoc search loop, bloats the caller's context window with raw fetch output, and produces findings whose sourcing is uneven. This convention establishes `web-researcher` as the single default primitive for public-web information gathering across the repository, and defines the narrow exceptions where in-context research remains appropriate.

## Contents

- [Purpose and Scope](./web-research-delegation/purpose-and-scope.md) — the principles behind the convention, what it covers, and what it explicitly does not cover.
- [The Rule](./web-research-delegation/the-rule.md) — the bright-line delegation threshold and the three documented exceptions.
- [Applying the Rule and Examples](./web-research-delegation/applying-the-rule-and-examples.md) — how agent, skill, and workflow files should cite the rule, plus worked good/bad examples.
- [Validation, Tooling, and References](./web-research-delegation/validation-tooling-and-references.md) — the compliance checklist and the agents/skills/workflows that reference this convention.
