---
title: "Common Workflows"
description: "The three common maker-checker-fixer workflows."
category: explanation
subcategory: development
tags:
  - maker-checker-fixer
  - workflow
  - content-quality
  - agent-patterns
  - validation
  - automation
created: 2025-12-14
when_to_use: "Use when choosing a workflow for a task."
---

# Common Workflows

## Basic Workflow: Create → Validate → Fix

**Scenario**: Creating new content from scratch

```
1. User Request: "Create new tutorial about X"
   ↓
2. Maker: Creates content + all dependencies
   ↓
3. User: Reviews content, looks good
   ↓
4. Checker: Validates content, finds minor issues
   ↓
5. User: Reviews audit report, approves fixes
   ↓
6. Fixer: Applies validated fixes
   ↓
7. Done: Content is production-ready
```

**Example**:

```bash
# Step 1: Create content
User: "Create TypeScript generics tutorial for ayokoding-www"
Agent: apps-ayokoding-www-general-maker (creates tutorial + navigation updates)

# Step 2: Validate
User: "Check the new tutorial"
Agent: apps-ayokoding-www-general-checker (generates audit report)

# Step 3: Fix
User: "Apply the fixes"
Agent: apps-ayokoding-www-general-fixer (applies validated fixes from audit)
```

## Iterative Workflow: Maker → Checker → Fixer → Checker

**Scenario**: Major content update requiring validation of fixes

```
1. User Request: "Update existing content X"
   ↓
2. Maker: Updates content + dependencies
   ↓
3. Checker: Validates, finds issues
   ↓
4. User: Reviews audit, approves fixes
   ↓
5. Fixer: Applies fixes
   ↓
6. Checker: Re-validates to confirm fixes worked
   ↓
7. Done: Content verified clean
```

**When to use**: Critical content, major refactoring, or when fixer confidence is uncertain

## Update Workflow: Maker (update mode) → Checker

**Scenario**: Updating existing content that's already high quality

```
1. User Request: "Add section Y to existing content X"
   ↓
2. Maker: Updates content (already validated during creation)
   ↓
3. Checker: Quick validation (optional, for confirmation)
   ↓
4. Done: High-quality content remains high-quality
```

**When to use**: Minor updates to well-maintained content
