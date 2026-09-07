---
description: How scenario by-example measures coverage, which Mermaid diagram types it uses, and why framework introduction is sequenced after the underlying concept.
when_to_use: Use when scoping coverage percentages, choosing a Mermaid diagram type, or deciding when to introduce a named framework in a scenario-domain example.
---

# How It Differs from SWE By-Example: Coverage Metric, Diagrams, and Framework Sequencing

## Coverage metric

**SWE by-example**: 95% of programming language/framework features.

**Scenario by-example**: Coverage of domain competency — the breadth of decisions, frameworks,
and scenarios a practitioner in that domain regularly encounters.

Coverage percentages per level:

- Beginner: 0–40% (foundational concepts, simple decisions)
- Intermediate: 40–75% (production scenarios, compliance/frameworks in context)
- Advanced: 75–95% (complex multi-stakeholder decisions, crisis scenarios, program-level leadership)

## Mermaid diagram use cases

Scenario by-example diagrams visualize:

- **Decision trees**: Branching decision logic (e.g., breach notification decision tree)
- **Workflow diagrams**: Process flows (e.g., vendor onboarding, incident escalation)
- **Organizational charts**: RACI matrices, governance structures
- **Risk matrices**: Heat maps showing likelihood vs impact
- **Timeline diagrams**: Regulatory deadlines, program milestones
- **Compliance mapping**: Framework control mapping across multiple standards

Same color-blind palette applies (Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC,
Brown #CA9161).

## No "core features first" constraint

The core-features-first principle from SWE by-example does not apply — scenario content has no
"dependency installation" concern. Instead, apply:

**Frameworks-last principle**: Introduce specific frameworks (ISO 27001, NIST CSF, FAIR) only
after the underlying concept is established. Do not open beginner examples by applying a framework
without first explaining what problem it solves.

Example:

```markdown
## PASS: Concept first, then framework

### Example 5: Scoring Risk Likelihood and Impact (Beginner)

A 5×5 risk matrix lets you compare risks by multiplying two factors...
[Example shows a blank matrix and manual scoring]

### Example 36: Applying FAIR for Quantitative Risk (Intermediate)

The FAIR model (Factor Analysis of Information Risk) structures the likelihood/impact
factors from Example 5 into financial loss estimates...
```

```markdown
## FAIL: Framework before concept

### Example 5: FAIR Risk Quantification (Beginner)

FAIR is the international standard for quantitative cyber risk...
(Reader hasn't learned what risk likelihood and impact mean yet)
```
