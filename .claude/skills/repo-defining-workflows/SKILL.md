---
name: repo-defining-workflows
description: Workflow pattern standards for creating multi-agent orchestrations including YAML frontmatter (name, goal, termination, inputs, outputs), execution phases (sequential/parallel/conditional), agent coordination patterns, and Gherkin success criteria. Essential for defining reusable, validated workflow processes.
---

# Defining Workflows

## Purpose

This Skill provides comprehensive guidance for **defining workflows** - multi-agent orchestrations that coordinate multiple agents in sequence, parallel, or conditionally to accomplish complex tasks. Workflows enable reusable, validated processes.

**When to use this Skill:**

- Creating new workflow documents
- Defining multi-agent coordination patterns
- Structuring sequential or parallel agent execution
- Writing workflow acceptance criteria
- Documenting workflow parameters and inputs

## Workflow Structure

See [Workflow Structure](./reference/workflow-structure.md) for the required YAML frontmatter schema (name, goal, termination, inputs, outputs), YAML colon-quoting rule, and the full workflow content template (Purpose, Agents Involved, Input Parameters, Execution Phases, Success Criteria, Example Usage, Related Workflows).

## Execution Patterns

See [Execution Patterns](./reference/execution-patterns.md) for worked Sequential, Parallel, Conditional, and Mixed execution examples.

## Standard Input Parameters

Most workflows support:

- **max-concurrency** (number, default: 3): Background agents run concurrently — the N in the N+1 model (`1 main thread + N background agents = N+1 total`). The DAG governs the actual fan-out; N only caps it. Never self-promoted beyond the declared value
- **dry-run** (boolean, default: false): Preview without executing
- **verbose** (boolean, default: false): Detailed logging

## Common Mistakes

### ❌ Mistake 1: Unquoted colons in YAML

**Wrong**:

```yaml
description: Workflow name: detailed description
```

**Right**:

```yaml
description: "Workflow name: detailed description"
```

### ❌ Mistake 2: Missing agent dependencies

**Wrong**: Parallel execution when agent-2 needs agent-1 output
**Right**: Sequential execution with explicit dependency

### ❌ Mistake 3: No success criteria

**Wrong**: Workflow without Gherkin validation criteria
**Right**: Clear Gherkin scenarios for success validation

### ❌ Mistake 4: Missing parameters documentation

**Wrong**: Undocumented parameters that users must guess
**Right**: Table with all parameters, types, defaults, descriptions

## Workflow File Naming

**Convention**: `[workflow-name].md`. Shards are plain-named; a step keeps its own number —
[Ordinal Prefixes](../../../repo-governance/conventions/structure/ordinal-filename-prefixes.md).

**Examples**:

- `plan-quality-gate.md` - Plan quality gate workflow
- `repo-rules-quality-gate.md` - Repo rules quality gate workflow

## Quality Checklist

Before publishing workflow:

- [ ] Valid YAML frontmatter (all colons quoted)
- [ ] name field matches filename
- [ ] goal is clear and concise
- [ ] termination criteria defined (success/failure)
- [ ] All inputs documented (type, required, default)
- [ ] All outputs documented (type, pattern for file outputs)
- [ ] Execution phases clearly defined
- [ ] Dependencies explicit (sequential vs parallel)
- [ ] Success criteria in Gherkin format
- [ ] Example usage provided
- [ ] Related workflows linked

## References

**Primary Convention**: [Workflow Pattern Convention](../../../repo-governance/workflows/meta/workflow-identifier.md)

**Related Conventions**:

- [Maker-Checker-Fixer Pattern](../../../repo-governance/development/pattern/maker-checker-fixer.md) - Three-stage workflow pattern
- [Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria.md) - Gherkin format

**Related Skills**:

- `repo-applying-maker-checker-fixer` - MCF workflow pattern
- `plan-writing-gherkin-criteria` - Success criteria format

---

This Skill packages workflow definition standards for creating reusable multi-agent orchestrations with clear coordination patterns. For comprehensive details, consult the primary convention document.
