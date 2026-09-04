---
title: "Steps 1-2: Maker and Checker"
description: Documents the maker step (manual/AI-assisted guide creation) and the checker step (validation against in-the-field standards) of the in-the-field quality gate.
when_to_use: Use when creating or updating in-the-field production guides, or when running/interpreting the apps-ayokoding-www-in-the-field-checker agent.
---

# Steps 1-2: Maker and Checker

## 0. Lifecycle Validation Filter

Apply [Lifecycle Validation Ownership](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md)
before composing checker prompts. Pass Step 0's `delegated-gate-ids` and `lifecycle-evidence` to
checker and fixer prompts; exact delegated predicates cannot become findings or enter the fix loop.

## 1. Maker - Create/Update Guides (Manual/AI-Assisted)

**Objective**: Create or update in-the-field production guides

**Approaches**:

**Option A: Manual creation** (human author)

- Write guides following [In-the-Field Tutorial Convention](../../../conventions/tutorials/in-the-field.md)
- Focus on standard library first, then frameworks
- Don't worry about perfect compliance (checker will catch issues)

**Option B: AI-assisted creation** (apps-ayokoding-www-in-the-field-maker)

- Use in-the-field-maker with production specifications
- Generate initial guides based on language/framework
- Human review and refinement

**Outputs**:

- Guide files: overview.md, [topic].md (20-40 guides)
- Standard library → framework progressions
- Production-ready code with error handling
- Mermaid diagrams where appropriate

**Next step**: Proceed to step 2

## 2. Checker - Validate Quality (Sequential)

**Objective**: Identify gaps and issues against in-the-field standards

**Agent**: `apps-ayokoding-www-in-the-field-checker`

**Execution**:

```bash
# Invoke via Task tool
subagent_type: apps-ayokoding-www-in-the-field-checker
prompt: "Validate apps/ayokoding-www/content/en/learn/software-engineering/programming-language/java/in-the-field/ for in-the-field standards; delegated-gate-ids: {step0.outputs.delegated-gate-ids}; lifecycle-evidence: {step0.outputs.lifecycle-evidence}"
```

**Validation areas**:

1. **Guide count**: 20-40 guides
2. **Standard library first**: Standard library BEFORE framework (CRITICAL)
3. **Annotation density**: 1.0-2.25 comment lines per code line
4. **Production code quality**: Error handling, logging, security, configuration
5. **Framework justification**: Why not standard library explained
6. **Diagram count**: 10-20 diagrams (progression diagrams prioritized)
7. **Frontmatter**: Complete and correct

**Outputs**:

- Audit report: `local-tmp/ayokoding-web-in-the-field/ayokoding-in-the-field__{uuid-chain}__{timestamp}__audit.md`
- Executive summary with overall status
- Detailed findings with confidence levels
- Specific line numbers for issues
- Actionable recommendations

**UUID Chain Tracking**: Checker generates 6-char UUID and writes to `local-tmp/.execution-chain-{scope}` (where scope is derived from tutorial path, e.g., "java").

**Depends on**: Step 1 completion

**Next step**: Proceed to step 3
