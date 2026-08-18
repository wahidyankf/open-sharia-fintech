---
title: "Common Anti-Patterns"
description: "Common anti-patterns when condensing or offloading content."
category: explanation
subcategory: development
tags:
  - content-preservation
  - condensation
  - offload
  - zero-loss
  - documentation
created: 2025-12-14
when_to_use: "Use when reviewing a condensation for a common anti-pattern."
---

# Common Anti-Patterns

## FAIL: Anti-Pattern 1: Deleting Content Without Offload

```markdown
Before: AGENTS.md has 500 lines on file naming
Action: Delete section to reduce size
After: File naming knowledge lost

Problem: Need to recreate later, knowledge erosion
```

**PASS: Correct Approach:** Offload to `repo-governance/conventions/structure/file-naming.md`, link from AGENTS.md

## FAIL: Anti-Pattern 2: Incomplete Offload

```markdown
Before: Agent has 300 lines on testing
Action: Move 100 lines to convention, delete 200 lines
After: Partial knowledge preserved

Problem: Lost unique details, incomplete documentation
```

**PASS: Correct Approach:** Move ALL 300 lines to convention, comprehensive documentation

## FAIL: Anti-Pattern 3: Wrong Folder Choice

```markdown
Before: Testing strategy duplicated across agents
Action: Create `conventions/writing/testing-strategy.md`
After: Wrong location (testing is process, not content format)

Problem: Violates convention/development separation
```

**PASS: Correct Approach:** Create `repo-governance/development/quality/testing-strategy.md`

## FAIL: Anti-Pattern 4: Offloading Agent-Specific Logic

```markdown
Before: Agent has workflow for applying file naming convention
Action: Move workflow to `conventions/structure/file-naming.md`
After: Convention doc contains agent-specific logic

Problem: Convention polluted with implementation details
```

**PASS: Correct Approach:** Keep agent-specific workflow in agent, reference convention for rules
