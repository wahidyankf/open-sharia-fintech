---
title: "Model Tiers — Ultra"
description: "Defines the ultra tier: the frontier grade reserved for work that demonstrably exceeds the planning grade."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2026-09-06
when_to_use: Use when deciding whether an agent's task genuinely exceeds the planning grade and justifies the ultra tier.
---

# Model Tiers — Ultra

**Status**: defined and accepted by the tooling; **currently assigned to no agent**. The grade exists
so that a promotion is a one-line frontmatter change rather than a convention change. Admitting the
first member requires the evidence described under Admission Evidence below.

**When to use**: Work whose failure the planning grade cannot reliably prevent — frontier-difficulty
reasoning where a wrong answer is expensive to detect and expensive to undo.

**Cognitive profile**: Everything the planning grade offers, plus sustained coherence across a very
large working set and a materially lower rate of confidently-wrong output on novel problems.

**Task characteristics**:

- Cross-cutting design whose blast radius spans several delivery units
- Reasoning over a working set too large to hold coherently at the planning grade
- Problems where a plausible-but-wrong answer survives review and surfaces much later
- Novel work with no template, no prior art in the repository, and no cheap verification

**Agent examples**: none yet — see Status above.

**Frontmatter**: Specify `model: fable` explicitly.

```yaml
---
name: example-ultra-agent
description: Illustrative only; no agent declares this grade today...
tools: [Read, Write, Edit, Glob, Grep, Bash]
model: fable
effort: high
color: blue
---
```

## Admission Evidence

The ultra grade costs roughly twice the planning grade per token, so a promotion is justified by
observed failure, never by anticipated difficulty. Before moving an agent here, record in its
Model Selection Justification block:

1. **The observed failure** — a specific task the agent got wrong at the planning grade, not a
   worry that it might.
2. **Why a cheaper fix does not apply** — a tighter skill, a narrower charter, or a
   maker-checker-fixer split resolves most quality complaints without a grade change.
3. **How the improvement will be noticed** — the promotion is reversible, so name what would send
   the agent back down.

An agent that cannot supply all three stays at the planning grade. "Defaulting to the highest grade
just in case" is the same mistake [Common Mistakes](./common-mistakes.md) has always named, one
grade higher.

## Before the First Ultra Agent Lands

The Codex model this grade maps to is behind a restricted-access programme, so the mirror can emit a
`model` value the running account cannot use. The first agent promoted to this grade must be
smoke-tested on the Codex binding before it lands — see
[Platform Binding Examples](./platform-binding-examples.md#where-a-grade-does-not-mean-the-same-thing).
This costs nothing while the grade has no members, which is exactly why it is written down now.
