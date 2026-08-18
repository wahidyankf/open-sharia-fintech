---
title: Scenario By-Example Tutorial Convention
description: Standards for scenario-domain by-example tutorials using annotated documents, decisions, and governance artifacts — extends the SWE By-Example Convention for any non-code domain
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - scenario
  - governance
  - decision-making
created: 2026-05-21
when_to_use: Use when writing or reviewing a non-code, scenario-driven by-example tutorial (security governance, ADRs, legal/compliance, risk) and you need the standard this content must follow.
---

# Scenario By-Example Tutorial Convention

This convention extends the SWE By-Example Tutorial Convention for domains where learning happens
through annotated documents, decisions, or governance artifacts rather than runnable code. The
sections below have moved into
[`scenario-by-example/`](./scenario-by-example/) — read them in order for the full convention.

## Contents

1. [Purpose](./scenario-by-example/purpose.md) — What this convention extends, its target audience, and applicable domains.
2. [Artifact Type, Self-Containment, and Annotation Semantics](./scenario-by-example/artifact-type-self-containment-and-annotation-semantics.md) — How artifact type, self-containment, and `# =>` annotation semantics differ from SWE by-example.
3. [Coverage Metric, Diagrams, and Framework Sequencing](./scenario-by-example/coverage-metric-diagrams-and-framework-sequencing.md) — Domain-competency coverage, Mermaid diagram use cases, and the frameworks-last principle.
4. [Five-Part Format (scenario-adapted)](./scenario-by-example/five-part-format-scenario-adapted.md) — The five-part example structure adapted for scenario domains.
5. [Coverage Levels and Applies To](./scenario-by-example/coverage-levels-and-applies-to.md) — Beginner/Intermediate/Advanced coverage bands and which tutorial tracks this convention governs.
6. [Validation Criteria and Principles Implemented/Respected](./scenario-by-example/validation-criteria-and-principles-implemented-respected.md) — The validation checklist and the principles this convention implements.

## Related Documentation

- [SWE By-Example Tutorial Convention](../tutorials/swe-by-example.md) — base convention this extends
- [Security By-Example Tutorial Convention](../tutorials/security-by-example.md) — for security tool/lab content
- [General Tutorial Convention](../tutorials/general.md) — base tutorial standards
- [Diagrams Convention](../formatting/diagrams.md) — Mermaid diagram standards
