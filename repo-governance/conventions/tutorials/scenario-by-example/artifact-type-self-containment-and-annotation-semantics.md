---
title: "How It Differs from SWE By-Example: Artifact Type, Self-Containment, and Annotation Semantics"
description: How scenario by-example redefines artifact type, self-containment, and annotation semantics compared to code-first SWE by-example.
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
when_to_use: Use when adapting the SWE by-example rules for artifact type, self-containment, or annotation style to a scenario-domain example.
---

# How It Differs from SWE By-Example: Artifact Type, Self-Containment, and Annotation Semantics

## Artifact type

| SWE By-Example                 | Scenario By-Example                                                            |
| ------------------------------ | ------------------------------------------------------------------------------ |
| Runnable source code           | Annotated policy, risk register, decision record, governance table, case study |
| `go run`/`python` verification | Scenario plausibility and organizational realism                               |
| `// =>` on variable state      | `# =>` or `<!-- => -->` on document lines explaining reasoning                 |

## Self-containment definition

**SWE by-example**: Copy-paste-runnable with a single command.

**Scenario by-example**: Fully standalone with complete organizational context. Each example
must include:

- **Scenario Context** — organization type, size, industry, and decision-maker role
- **Complete artifact** — the full policy excerpt, risk register row, or decision document; no
  "see Example N for the template" cross-references
- **All annotations** — inline comments on every substantive line explaining the reasoning,
  trade-off, or decision rationale

## Annotation semantics

**SWE by-example** (`// =>` on code): Documents variable state and return values.

**Scenario by-example** (`# =>` on document lines or `<!-- => -->` in markdown tables):
Documents the reasoning, constraint, or trade-off behind each element.

```yaml
# Risk Register Entry
risk_id: RISK-003
asset: Customer PII database # => Scope: production database only (dev DBs are separate)
threat: Unauthorized access by insider
vulnerability: Over-privileged DBA accounts
likelihood: 3 # => Medium: 1 DBA with excessive access; IAM review outstanding
impact: 5 # => Catastrophic: 200K records, GDPR notification required
risk_score: 15 # => likelihood × impact = HIGH band (12–19)
# => Exceeds risk appetite threshold of 12 — treatment required, cannot accept
treatment: Mitigate # => Implement least-privilege IAM, not accept/transfer
# => Accept rejected: score > appetite. Transfer rejected: no cyber insurance covering insider.
owner: Head of Engineering
due_date: 2026-07-31
```

**For markdown tables**, use a "Rationale" column or trailing comment row:

```markdown
| Control                    | Status      | Rationale                                                           |
| -------------------------- | ----------- | ------------------------------------------------------------------- |
| MFA on all admin accounts  | Implemented | => Reduces credential stuffing risk; required by ISO 27001 A.9.4.2  |
| Vulnerability scan monthly | Partial     | => Scanner deployed but cloud assets excluded; gap being remediated |
```
