---
title: "Steps 1-2: Maker and Checker"
description: Documents the maker step (manual/AI-assisted example creation scoped to "just enough") and the checker step (validation against Primer standards, including scope discipline).
when_to_use: Use when creating or updating Primer tutorial content, or when running/interpreting the apps-ayokoding-www-primer-checker agent.
---

# Steps 1-2: Maker and Checker

## 1. Maker - Create/Update Examples (Manual/AI-Assisted)

**Objective**: Create or update Primer tutorial content, scoped to "just enough to be productive"

**Approaches**:

**Option A: Manual creation** (human author)

- Write examples following the anatomy documented in `apps-ayokoding-www-primer-maker`
- Focus on educational value within the primer's scoped surface
- Don't worry about perfect compliance (checker will catch issues)

**Option B: AI-assisted creation** (`apps-ayokoding-www-primer-maker`)

- Identify the topics that depend on this primer and derive the minimum productive surface
- Generate initial examples authored at By-Example pace within that scope
- Human review and refinement

**Outputs**:

- Tutorial files: `overview.md` (stating scope + dependent topics), example page(s), `capstone/`
  (light consolidation exercise), `code/`
- 75-85 examples across the scoped surface
- Mermaid diagrams where appropriate
- Educational annotations and comments

**Next step**: Proceed to step 2

## 2. Checker - Validate Quality (Sequential)

**Objective**: Identify gaps and issues against Primer standards, including scope discipline

**Agent**: `apps-ayokoding-www-primer-checker`

**Execution**:

```bash
# Invoke via Task tool
subagent_type: apps-ayokoding-www-primer-checker
prompt: "Validate apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/just-enough-go/learning/ for compliance with Primer standards"
```

**Validation areas**:

1. **Coverage and count**: 75-85 examples (floor: 75)
2. **Annotation density**: 1.0-2.25 comment lines per code line, per example (same formula as By
   Example)
3. **Self-containment**: copy-paste-runnable within the primer's scope
4. **Scope discipline** (CRITICAL, Primer-specific): `overview.md` states the "just enough to be
   productive" scope and dependent topics; every example serves that stated scope
5. **Diagrams**: accessible color-blind palette
6. **Format**: five-part structure identical to By Example
7. **Capstone type**: light consolidation exercise, not a full runnable project
8. **Frontmatter**: complete and correct

**Outputs**:

- Audit report: `generated-reports/ayokoding-web-primer__{uuid-chain}__{timestamp}__audit.md`
- Executive summary with overall status
- Detailed findings with confidence levels
- Specific line numbers for issues
- Actionable recommendations

**UUID Chain Tracking**: Checker generates 6-char UUID and writes to
`generated-reports/.execution-chain-{scope}` (where scope is derived from tutorial path, e.g.,
"just-enough-go"). See
[Temporary Files Convention](../../../development/infra/temporary-files.md#uuid-chain-generation) for
details.

**Depends on**: Step 1 completion

**Next step**: Proceed to step 3
