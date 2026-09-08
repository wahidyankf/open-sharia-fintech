---
description: Standards for scenario-domain by-example tutorials using annotated documents, decisions, and governance artifacts — extends the SWE By-Example Convention for any non-code domain
when_to_use: Use when writing or reviewing a non-code, scenario-driven by-example tutorial (security governance, ADRs, legal/compliance, risk) and you need the standard this content must follow.
---

# Scenario By-Example Tutorial Convention

This convention extends the SWE By-Example Tutorial Convention for domains where learning happens
through annotated documents, decisions, or governance artifacts rather than runnable code. The
sections below have moved into
[`scenario-by-example/`](./scenario-by-example/) — read them in order for the full convention.

## Contents

1. [Artifact Type, Self-Containment, and Annotation Semantics](./scenario-by-example/artifact-type-self-containment-and-annotation-semantics.md) — How artifact type, self-containment, and `# =>` annotation semantics differ from SWE by-example.
2. [Coverage Metric, Diagrams, and Framework Sequencing](./scenario-by-example/coverage-metric-diagrams-and-framework-sequencing.md) — Domain-competency coverage, Mermaid diagram use cases, and the frameworks-last principle.
3. [Five-Part Format (scenario-adapted)](./scenario-by-example/five-part-format-scenario-adapted.md) — The five-part example structure adapted for scenario domains.
4. [Coverage Levels and Applies To](./scenario-by-example/coverage-levels-and-applies-to.md) — Beginner/Intermediate/Advanced coverage bands and which tutorial tracks this convention governs.
5. [Validation Criteria and Principles Implemented/Respected](./scenario-by-example/validation-criteria-and-principles-implemented-respected.md) — The validation checklist and the principles this convention implements.

## Related Documentation

- [SWE By-Example Tutorial Convention](../tutorials/swe-by-example.md) — base convention this extends
- [Security By-Example Tutorial Convention](../tutorials/security-by-example.md) — for security tool/lab content
- [General Tutorial Convention](../tutorials/general.md) — base tutorial standards
- [Diagrams Convention](../formatting/diagrams.md) — Mermaid diagram standards

## Purpose

This convention **extends the [SWE By-Example Tutorial Convention](./swe-by-example.md) for any
domain where learning happens through annotated documents, decisions, or governance artifacts
rather than runnable code**.

**Base requirements**: Scenario by-example tutorials inherit all standards from the
[SWE By-Example Convention](./swe-by-example.md) and override only the differences documented
below.

**Target audience**: Practitioners — engineers, tech leads, managers — who learn best through
realistic annotated scenarios grounded in real organizational contexts.

**Applicable domains** (not exhaustive):

- Security governance and leadership (CISO)
- Software architecture decisions (ADRs, design reviews)
- Legal and compliance scenarios
- Project management and delivery decisions
- Risk management and business continuity
