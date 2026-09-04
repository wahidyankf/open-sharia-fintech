---
title: "Steps 1-2: Maker and Checker"
description: Documents the maker step (manual/AI-assisted worked-example creation) and the checker step (mode detection plus the eight quality validation areas) of the Annotated-concept quality gate.
when_to_use: Use when creating or updating Annotated-concept tutorial content, or when running/interpreting the apps-ayokoding-www-annotated-concept-checker agent.
---

# Steps 1-2: Maker and Checker

## 0. Lifecycle Validation Filter

Apply [Lifecycle Validation Ownership](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md)
before composing checker prompts. Pass Step 0's `delegated-gate-ids` and `lifecycle-evidence` to
checker and fixer prompts; exact delegated predicates cannot become findings or enter the fix loop.

## 1. Maker - Create/Update Worked Examples (Manual/AI-Assisted)

**Objective**: Create or update Annotated-concept tutorial content, in the correct mode (standard
concept-centric with code, or the leadership no-code sub-mode)

**Approaches**:

**Option A: Manual creation** (human author)

- Write worked examples following the anatomy documented in
  `apps-ayokoding-www-annotated-concept-maker`
- Focus on educational value and concept clarity
- Don't worry about perfect compliance (checker will catch issues)

**Option B: AI-assisted creation** (`apps-ayokoding-www-annotated-concept-maker`)

- Determine mode first (standard vs. no-code sub-mode) from the topic's format designation
- Generate initial worked examples/scenarios based on the topic's concept inventory
- Human review and refinement

**Outputs**:

- Tutorial files: `overview.md`, worked-example page(s) grouped by per-theme clusters, `capstone/`
- `code/` directory with colocated runnable files (standard mode only — absent in the no-code
  sub-mode)
- 45-60 worked examples (standard mode) or 20-30 worked scenarios (no-code sub-mode)
- Accessible Mermaid diagrams where a visual materially aids understanding

**Next step**: Proceed to step 2

## 2. Checker - Detect Mode and Validate Quality (Sequential)

**Objective**: Detect the topic's anatomy mode, then identify gaps and issues against
Annotated-concept standards

**Agent**: `apps-ayokoding-www-annotated-concept-checker`

**Execution**:

```bash
# Invoke via Task tool
subagent_type: apps-ayokoding-www-annotated-concept-checker
prompt: "Validate apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/computer-science-foundations/learning/ for Annotated-concept standards; delegated-gate-ids: {step0.outputs.delegated-gate-ids}; lifecycle-evidence: {step0.outputs.lifecycle-evidence}"
```

**Validation areas**:

1. **Mode detection**: standard (code-bearing) vs. leadership no-code sub-mode, decided before any
   other check
2. **Worked-example/scenario count**: 45-60 (standard) or 20-30 (no-code sub-mode) — floor, not a
   cap
3. **Annotation density** (standard mode only): 1.0-2.25 comment lines per code line, same formula
   direction as By Example
4. **Self-containment**: code-bearing worked examples copy-paste-runnable within topic scope
5. **Mode integrity** (CRITICAL): zero code blocks and no `code/` directory in a no-code sub-mode
   topic
6. **Diagrams**: accessible WCAG palette, used only where a visual materially aids understanding
7. **Structure**: Context, medium-fits-concept, Key Takeaway, Why It Matters (50-100 words)
8. **Frontmatter**: complete and correct

**Outputs**:

- Audit report:
  `local-tmp/ayokoding-web-annotated-concept/ayokoding-web-annotated-concept__{uuid-chain}__{timestamp}__audit.md`
- Executive summary with overall status and detected mode
- Detailed findings with confidence levels
- Specific line numbers for issues
- Actionable recommendations

**UUID Chain Tracking**: Checker generates 6-char UUID and writes to
`local-tmp/.execution-chain-{scope}` (where scope is derived from tutorial path, e.g.,
"computer-science-foundations"). See
[Temporary Files Convention](../../../development/infra/temporary-files.md#uuid-chain-generation) for
details.

**Depends on**: Step 1 completion

**Next step**: Proceed to step 3
