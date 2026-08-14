---
title: "Steps 3-4: Apply Content and Facts Fixes"
description: Documents the content-fixer and facts-fixer steps of the general quality gate, including their conditions and success criteria.
when_to_use: Use when running or interpreting the fix-application steps of the general quality gate.
---

# Steps 3-4: Apply Content and Facts Fixes

## 3. Apply Content Fixes (Sequential, Conditional)

Fix convention violations, frontmatter issues, and content quality problems.

**Agent**: `apps-ayokoding-www-general-fixer`

- **Args**: `report: {step1.outputs.content-report-N}, approved: all`
- **Output**: `{content-fixes-applied}`
- **Condition**: Content findings exist from step 2
- **Depends on**: Step 2 completion

**Success criteria**: Fixer successfully applies content fixes without errors.

**On failure**: Log errors, continue to next fixer.

## 4. Apply Facts Fixes (Sequential, Conditional)

Fix factual errors, outdated information, and incorrect code examples.

**Agent**: `apps-ayokoding-www-facts-fixer`

- **Args**: `report: {step1.outputs.facts-report-N}, approved: all`
- **Output**: `{facts-fixes-applied}`
- **Condition**: Facts findings exist from step 2
- **Depends on**: Step 3 completion

**Success criteria**: Fixer successfully applies factual fixes without errors.

**On failure**: Log errors, continue to next fixer.

**Notes**:

- Uses web verification to ensure accuracy
- Re-validates findings before applying
- Preserves educational content intent
