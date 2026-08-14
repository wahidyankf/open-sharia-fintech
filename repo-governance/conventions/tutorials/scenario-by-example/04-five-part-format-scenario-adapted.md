---
title: Five-Part Format (scenario-adapted)
description: The five-part example structure adapted for scenario domains — coverage statement, scenario context, annotated artifact, key takeaway, and why it matters.
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
when_to_use: Use when drafting or reviewing an individual scenario by-example example and you need the required five-part structure.
---

# Five-Part Format (scenario-adapted)

## Part 1: What This Covers (2-3 sentences)

Same as SWE by-example. Must answer:

- What governance concept, decision type, or framework element does this example demonstrate?
- Why does it matter to the practitioner's role?
- When would this decision or artifact arise in a real organization?

## Part 2: Scenario Context (1-2 sentences)

Replace "Scenario" with organizational framing:

- Organization type and size (e.g., "You are the security manager at AcmeSoft, a 200-person SaaS
  company")
- Decision-maker role and the immediate business context
- Use fictional but plausible organization names (AcmeSoft, Nexatech, Meridian Health, etc.)

```markdown
**Scenario:** You are the newly appointed security manager at AcmeSoft, a 200-person SaaS
company with no formal risk register. Your CTO has asked for a first pass before the board
meeting next quarter.
```

## Part 3: Annotated Document or Decision

The core artifact — fully annotated with `# =>` or `<!-- => -->`:

- Show the complete policy excerpt, risk register entry, compliance table, or decision record
- Every substantive line has an annotation explaining reasoning, constraint, or trade-off
- Use realistic fictional values (plausible dollar amounts, risk scores, dates)
- Density target: same 1.0–2.25 annotation lines per substantive non-blank content line per example

**Annotation quality**: Annotations explain WHY a decision was made, not just WHAT the field is.

```yaml
# FAIL: Annotation describes field, not reasoning
likelihood: 3  # => This is the likelihood score

# PASS: Annotation explains reasoning
likelihood: 3  # => Medium: attack requires insider access + active exploitation of a
               # => known vulnerability — not easily automated by external attacker
```

## Part 4: Key Takeaway (1-2 sentences)

Same as SWE by-example. The core decision insight to retain:

```markdown
**Key Takeaway:** A risk register is not a documentation exercise — it is a prioritization
tool. Every entry without a named owner and a due date is a finding waiting to be ignored.
```

## Part 5: Why It Matters (50-100 words)

Same as SWE by-example. Production-focused, active voice, specific to the scenario.
