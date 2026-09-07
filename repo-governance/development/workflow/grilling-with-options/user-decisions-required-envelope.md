---
description: The exact outbound envelope a subagent returns to the root orchestrator instead of rendering a user prompt itself.
when_to_use: Use when a subagent must hand an unresolved design decision back to the root orchestrator instead of asking the user directly.
---

# User Decisions Required Envelope

A subagent MUST NOT render markdown as if it were asking the user. It returns this exact envelope to
the root orchestrator and stops before work that depends on the answer:

````markdown
## User Decisions Required

```yaml
decisions:
  - id: stable_snake_case_id
    question: One self-contained decision prompt
    recommended:
      option_id: recommended_option_id
      rationale: One context-grounded recommendation rationale
    options:
      - id: recommended_option_id
        label: Recommended option label
        tradeoff: One decision-specific trade-off
      - id: alternative_option_id
        label: Alternative option label
        tradeoff: One decision-specific trade-off
```
````

The stable `id` identifies the decision across reinvocation. `options` exhaustively lists every
substantive leaf with its trade-off; the root adds the standing chat option and relies on the
client's implicit custom answer. After the envelope, the specialist stops. The root presents the
decision through its native UI, then resumes or reinvokes the specialist with the resolved answer.
Direct custom-agent callers receive the same envelope.
