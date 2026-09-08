---
description: Standards for security-domain by-example tutorials using tool output, lab scenarios, and annotated security artifacts — extends the SWE By-Example Convention
when_to_use: Use when authoring, reviewing, or scoping a security-domain by-example tutorial (Foundations, Red Team, or Blue Team) and need the security-specific adaptations of the SWE By-Example convention.
---

# Security By-Example Tutorial Convention

This convention defines security-domain by-example tutorial standards, extending the SWE
By-Example convention for tool output, lab scenarios, and annotated security artifacts. The
sections below have moved into [`security-by-example/`](./security-by-example/) — read them in
order for the full convention.

## Contents

1. [Artifact Type, Self-Containment, and Annotation Semantics](./security-by-example/artifact-type-self-containment-and-annotation-semantics.md) — How artifacts, self-containment, and `# =>` annotations differ from SWE By-Example.
2. [Coverage Metric, Diagram Use Cases, and Core-First Tooling](./security-by-example/coverage-metric-diagrams-and-core-first-tooling.md) — Coverage measurement, Mermaid diagram use cases, and core-first tool introduction order.
3. [Five-Part Format (Security-Adapted)](./security-by-example/five-part-format-security-adapted.md) — The security-domain adaptation of the five-part example structure.
4. [Coverage Levels and Applies To](./security-by-example/coverage-levels-and-applies-to.md) — Beginner/Intermediate/Advanced coverage definitions and which content tracks this convention governs.
5. [Validation Criteria, Principles, and Related Documentation](./security-by-example/validation-criteria-principles-and-related-documentation.md) — The quality checklist, implemented principles, and related conventions.

## Ethical Use Requirements (Red Team Content Only)

Every Red Team level page (`beginner.md`, `intermediate.md`, `advanced.md`) MUST open with:

```markdown
> **Ethical Use:** All examples are for authorized penetration testing, CTF competitions,
> lab environments, and defensive understanding only. Never apply these techniques against
> systems without explicit written authorization.
```

Foundations and Blue Team level pages do not require this notice.

## Purpose

This convention **extends the [SWE By-Example Tutorial Convention](./swe-by-example.md) for the
security domain**, adapting the code-first model to security tool output, lab scenarios, shell
sessions, and annotated security artifacts.

**Base requirements**: Security by-example tutorials inherit all standards from the
[SWE By-Example Convention](./swe-by-example.md) and override only the differences documented
below.

**Target audience**: Software engineers without a formal security background who want to learn
security through hands-on scenarios rather than abstract theory.
