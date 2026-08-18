---
title: "Agent-Skill Separation — Four Separation Patterns (A-C)"
description: "Defines Separation Patterns A through C for splitting knowledge between agents and agent skills."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when choosing which separation pattern (reference Skill, convention link, or hybrid) fits a piece of agent knowledge.
---

# Agent-Skill Separation — Four Separation Patterns (A-C)

Based on the pilot validation, use these proven patterns when simplifying agents:

## Pattern A: Reference Skill for Standards

**Use when**: Content is a universal standard that doesn't change per-agent.

**Before (in agent)**:

```markdown
## Content Quality Standards

**Active Voice Required**: Use active voice for clarity and directness.

PASS: Good: "The agent validates the content"
FAIL: Bad: "The content is validated by the agent"

**Heading Hierarchy**: Each file MUST have exactly one H1 heading.

[... 50-100 lines of standards ...]
```

**After (in agent)**:

```markdown
## Content Quality Standards

**See `docs-applying-content-quality` Skill for complete standards** on:

- Active voice requirements
- Heading hierarchy (single H1, proper nesting)
- Accessibility compliance (alt text, WCAG AA contrast)
- Professional formatting
```

**Impact**: ~50-100 lines removed per agent, zero loss of knowledge (accessible via Skill).

## Pattern B: Convention Link for Detailed Rules

**Use when**: Technical specifications have a single source of truth in conventions.

**Before (in agent)**:

```markdown
## Report Generation

**File Naming Pattern**: `generated-reports/{agent}__{uuid-chain}__{YYYY-MM-DD--HH-MM}__{type}.md`

**UUID Chain Generation**: 6-char hex UUIDs for parallel execution support.

- Root: `a1b2c3`
- Child: `a1b2c3.d4e5f6`
- Grandchild: `a1b2c3.d4e5f6.g7h8i9`

**Progressive Writing**: Initialize report at start, write findings immediately...

[... 100-200 lines of mechanics ...]
```

**After (in agent)**:

```markdown
## Report Generation

**MANDATORY**: Write findings PROGRESSIVELY to `generated-reports/` per [Temporary Files Convention](../../infra/temporary-files.md).

**Report pattern**: `generated-reports/{agent}__{uuid-chain}__{timestamp}__{type}.md`

**UUID chain generation**: 6-char hex UUIDs for parallel execution. See convention for generation logic.

[Brief 3-5 line summary of workflow, link to convention for details]
```

**Impact**: ~100-200 lines removed per agent, convention becomes single source of truth.

## Pattern C:Skill + Convention Hybrid

**Use when**: Complex domain requires both actionable guidance (Skill) and specifications (convention).

**Before (in agent)**:

```markdown
## Factual Validation

**Verification Workflow**:

1. Identify claim type (command, version, API)
2. Determine authoritative source...
   [... 100 lines of methodology ...]

**Source Prioritization**:

1. Official documentation
2. GitHub repositories...
   [... 50 lines of priority rules ...]

**Confidence Classifications**:

- [Verified]: Confirmed by authoritative source
- [Unverified]: Cannot verify...
  [... 50 lines of classifications ...]
```

**After (in agent)**:

```markdown
## Factual Validation

**See `docs-validating-factual-accuracy` Skill for complete methodology** covering:

- Verification workflow (claim identification → source determination → verification)
- Source prioritization (official docs → GitHub → registries → standards)
- Confidence classifications ([Verified], [Unverified], [Error], [Outdated])

**Technical specs**: [Factual Validation Convention](../../../conventions/writing/factual-validation.md) for confidence classification criteria.
```

**Impact**: ~150-300 lines removed per agent, best-of-both (guidance + specs) via two sources.
