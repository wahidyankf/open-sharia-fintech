---
title: "Resolved User Decisions Envelope"
description: The exact inbound payload the root passes back to a specialist verbatim once the user has resolved every decision, and the validation the specialist must perform on it.
category: explanation
subcategory: development
tags:
  - planning
  - grill-me
  - user-interaction
  - plan-maker
  - design-decisions
  - interaction
  - agents
created: 2026-05-26
when_to_use: Use when the root is constructing the resolved-decisions payload to pass back to a specialist, or when a specialist must validate that payload before proceeding.
---

# Resolved User Decisions Envelope

After rendering an outbound envelope, the root MUST return this versioned, harness-neutral payload
to the specialist **verbatim**. It is the only inbound representation of a resolved decision:

````markdown
## Resolved User Decisions

```yaml
schema_version: 1
decisions:
  - id: stable_snake_case_id
    answer:
      kind: selected_option
      option_id: original_option_id
  - id: another_stable_snake_case_id
    answer:
      kind: custom_answer
      value: Exact user-supplied answer
```
````

`id` MUST be the original decision ID from `## User Decisions Required`. A `selected_option`
answer MUST name the original leaf ID in `option_id`, including when staged rendering reaches that
leaf through a branch group. A `custom_answer` MUST preserve the user's answer in `value`; the root
MUST NOT recast a write-in as a selected option because its text resembles an option label. These
two discriminated forms make listed selections and user-authored answers unambiguous across every
harness.

Before performing work that depends on an answer, the receiving specialist MUST validate that the
payload has `schema_version: 1`, contains each requested decision ID exactly once and no unknown ID,
uses a known original leaf ID for every `selected_option`, and carries a non-empty `value` for every
`custom_answer`. On failure, it MUST stop and request a corrected resolved-decision payload; it
MUST NOT infer, normalize, or silently repair an answer. The root constructs this payload only after
rendering is complete and passes it unchanged on every resume or reinvocation.
