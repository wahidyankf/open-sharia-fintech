---
title: "Steps 1-2: Maker and Checker"
description: Documents the maker step (manual/AI-assisted example creation) and the checker step (validation against by-example standards, including the mandatory Examples-by-Level section).
when_to_use: Use when creating or updating by-example tutorial content, or when running/interpreting the apps-ayokoding-www-by-example-checker agent.
---

# Steps 1-2: Maker and Checker

## 0. Lifecycle Filter

Apply [Lifecycle Validation Ownership](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md);
pass its IDs and evidence to checker/fixer prompts.

## 1. Maker - Create/Update Examples (Manual/AI-Assisted)

**Objective**: Create or update by-example tutorial content

**Approaches**:

**Option A: Manual creation** (human author)

- Write examples following [By-Example Tutorial Convention](../../../conventions/tutorials/swe-by-example.md)
- Focus on educational value and code quality
- Don't worry about perfect compliance (checker will catch issues)

**Option B: AI-assisted creation** (docs-tutorial-maker or future by-example-maker)

- Use docs-tutorial-maker with by-example specifications
- Generate initial examples based on language/framework
- Human review and refinement

**Outputs**:

- Tutorial files: overview.md, beginner.md, intermediate.md, advanced.md
- 75-85 examples across three levels
- Mermaid diagrams where appropriate
- Educational annotations and comments

**Next step**: Proceed to step 2

## 2. Checker - Validate Quality (Sequential)

**Objective**: Identify gaps and issues against by-example standards

**Agent**: `apps-ayokoding-www-by-example-checker`

**Execution**:

```bash
# Invoke via Task tool
subagent_type: apps-ayokoding-www-by-example-checker
prompt: "Validate {input.scope}; delegated-gate-ids: {step0.outputs.delegated-gate-ids}; lifecycle-evidence: {step0.outputs.lifecycle-evidence}"
```

**Validation areas**:

1. **Coverage and count**: 95% coverage, 75-85 examples
2. **Annotation density**: 1.0-2.25 comment lines per code line (target: 1.0-2.25, upper bound: 2.5)
   - **Calculation**: `density = comments ÷ code` (e.g., 10 comments ÷ 5 code = 2.0)
3. **Self-containment**: Copy-paste-runnable within chapter scope
4. **Annotations**: `// =>` notation for outputs and states
5. **Diagrams**: 30-50 total diagrams (approximately 35-60% of 75-85 examples), color-blind palette
6. **Format**: Five-part structure: (1) Brief Explanation (2-3 sentences), (2) Mermaid Diagram (when appropriate), (3) Heavily Annotated Code, (4) Key Takeaway (1-2 sentences), (5) Why It Matters (50-100 words)
7. **Frontmatter**: Complete and correct
8. **Examples-by-Level section** (CRITICAL — see
   [By-Example Convention §Examples-by-Level Section](../../../conventions/tutorials/swe-by-example.md#examples-by-level-section-mandatory)):
   - `overview.md` MUST contain a `## Examples by Level` heading (exact text, exact level).
   - Every `### Example N: Title` heading on every level page (`beginner.md`,
     `intermediate.md`, `advanced.md`, and `production.md` if present) MUST appear as a
     bullet in the matching per-level subheading block.
   - Each bullet MUST be a markdown link whose text is the verbatim example
     heading and whose href is `<level-page-url>#<slug>` — where `<slug>` is
     produced by `github-slugger` against the verbatim heading text (same
     algorithm as `rehype-slug`). See the
     [Examples-by-Level Section rule](../../../conventions/tutorials/swe-by-example.md#examples-by-level-section-mandatory)
     for the literal pattern and a worked snippet.
   - No bullet may point to an anchor that does not exist on the target level page (the
     link checker validates this).
   - If any level-page heading changes, the corresponding overview bullet (link text AND
     slug) MUST be regenerated.

**Outputs**:

- Audit report: `generated-reports/ayokoding-web-by-example__{uuid-chain}__{timestamp}__audit.md`
- Overall status and actionable findings with confidence and line numbers

**UUID Chain Tracking**: Checker generates 6-char UUID and writes to `generated-reports/.execution-chain-{scope}` (where scope is derived from tutorial path, e.g., "golang"). See [Temporary Files Convention](../../../development/infra/temporary-files.md#uuid-chain-generation) for details.

**Depends on**: Step 1 completion

**Next step**: Proceed to step 3
