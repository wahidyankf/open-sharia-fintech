---
description: PASS and FAIL examples of grilling questions — a well-formed markdown fallback, native-tool usage, and five common violations.
when_to_use: Use when checking whether a specific grilling question is well-formed or violates one of the option-structure rules.
---

# Examples

## PASS: Well-formed grilling question (markdown fallback)

```markdown
**Question**: Where should the new convention live?

- **Option 1 — `development/workflow/grilling-with-options.md`**: Layer-coherent (HOW we
  interact during development); matches adjacent workflow docs; requires updating
  `development/README.md`. _(Recommended — grilling is an interaction workflow, not a
  documentation-writing rule; the conventions/ README explicitly scopes that directory to
  documentation standards)_
- **Option 2 — `conventions/writing/grilling-with-options.md`**: Co-located with other
  writing conventions; simpler path for writers who look in conventions/ first; but fails
  the layer-coherence test because conventions/ is scoped to documentation rules, not
  development workflows.
- **Option 3 — `development/agents/grilling-with-options.md`**: Groups with AI agent
  standards; appropriate if grilling is agent-only; but grilling also applies to
  human-facing orchestration steps, so agents/ is too narrow.
- **Other**: Specify a different path.
```

## PASS: Interactive multiple-choice tool (preferred when available)

When the coding agent supports interactive selection (e.g., via an `AskUserQuestion`-style
tool), use it with 2-4 `options` entries. The platform renders the choices as a single-click
selection UI and always includes a free-form "Other" path.

## FAIL: Open-ended prose question

```markdown
What approach do you want for the grilling convention?
```

**Problems**: No options, no trade-offs, no Recommended, no structure. Shifts cognitive
burden entirely to the user.

## FAIL: Too many options (more than 4)

```markdown
**Question**: Which layer?

- Option 1 — conventions/writing/
- Option 2 — conventions/structure/
- Option 3 — development/workflow/
- Option 4 — development/agents/
- Option 5 — development/pattern/
- Option 6 — development/quality/
```

**Problem**: Six options signals the agent has not pruned the decision space. Maximum is 4.
Narrow the options first by exploring the repo and applying the layer-coherence test, then
ask.

## FAIL: Trade-offs are non-specific filler

```markdown
- **Option 1**: This is the simpler approach.
- **Option 2**: This is the more flexible approach.
```

**Problem**: "Simpler" and "more flexible" are meaningless without context. Each trade-off
must name the specific structural, maintenance, or governance implication for this decision.

## FAIL: Two options marked Recommended

```markdown
- **Option 1**: … _(Recommended)_
- **Option 2**: … _(Also Recommended)_
```

**Problem**: Exactly one option may be Recommended. If options are genuinely equal, the
agent must choose one and state why.

## FAIL: Unrelated decisions bundled

```markdown
**Question**: Which layer? And also, should we update the README? And what filename?
```

**Problem**: Three independent decisions bundled into one prompt. Present "Which layer?" and
"What filename?" together (tightly coupled). Present "Should we update the README?"
separately.
