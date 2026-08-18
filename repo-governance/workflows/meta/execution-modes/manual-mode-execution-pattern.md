---
title: "Manual Mode Execution Pattern"
description: The six-step procedure (initialize, check, terminate?, fix, iterate, finalize) for running a workflow manually without agent delegation.
category: explanation
subcategory: workflows
tags:
  - workflows
  - execution-mode
  - orchestration
created: 2026-01-05
when_to_use: Use when actually executing a workflow in Manual Orchestration mode and needing the concrete step sequence.
---

# Manual Mode Execution Pattern

## Step-by-Step Guide

**Step 1: Initialize Workflow Context**

- Generate UUID for execution tracking
- Determine workflow scope (files to process)
- Set iteration counter to 0

**Step 2: Execute Checker Logic**

```markdown
1. Read all files in scope
2. Apply validation rules
3. Categorize findings by criticality
4. Generate UUID chain for report
5. Write audit report to generated-reports/
   Pattern: {agent-family}**{uuid}**{timestamp}\_\_audit.md
6. Report findings summary to user
```

**Step 3: Check Termination Criteria**

```markdown
If findings = 0 AND iterations >= min-iterations (if set):
→ Go to Step 6 (Success)
If findings = 0 AND iterations < min-iterations:
→ Go to Step 4 (continue iterating)
If findings > 0 AND iterations >= max-iterations (if set):
→ Go to Step 6 (Partial success)
If findings > 0 AND (no max-iterations OR iterations < max-iterations):
→ Go to Step 4 (apply fixes)
```

**Step 4: Execute Fixer Logic**

```markdown
1. Read audit report from Step 2
2. Re-validate each finding:
   - Confirms issue exists → assess confidence
   - Issue resolved → skip (stale finding)
   - Issue never existed → FALSE_POSITIVE
3. Apply HIGH confidence fixes using Edit tool
4. Skip MEDIUM confidence (manual review needed)
5. Write fix report to generated-reports/
   Pattern: {agent-family}**{uuid}**{timestamp}\_\_fix.md
6. Report fixes applied to user
```

**Step 5: Iterate**

```markdown
1. Increment iteration counter
2. Go back to Step 2 (Execute Checker Logic)
```

**Step 6: Finalize**

```markdown
1. Report final status:
   - Success (zero findings)
   - Partial (findings remain after max-iterations)
   - Failure (errors during execution)
2. Show git status (modified files)
3. Wait for user commit approval
```
