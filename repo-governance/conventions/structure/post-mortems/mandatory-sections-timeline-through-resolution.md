---
title: "Post-Mortem Convention: Mandatory Sections — Timeline Through Resolution"
description: The required Timeline, Root Cause, Trigger, Contributing Factors, and Resolution & Mitigations sections of a post-mortem document, in reading order
when_to_use: Read this when authoring the middle mandatory sections of a post-mortem, from the incident timeline through how service was restored.
category: explanation
subcategory: conventions
tags:
  - post-mortem
  - incidents
  - blameless
  - reliability
  - structure
created: 2026-06-05
---

# Mandatory Sections: Timeline Through Resolution

## 6. Timeline

Absolute timestamps with stated timezone. Never use relative offsets ("T+5min") as the primary
form — they cannot be interpreted without an anchor and degrade over time.

```markdown
| Time (WIB UTC+7) | Event                                                          |
| ---------------- | -------------------------------------------------------------- |
| 2026-06-04 14:00 | Dependency bump PR merged to main                              |
| 2026-06-04 14:05 | GitHub Actions CI failure triggered on affected apps           |
| 2026-06-04 14:30 | Developer noticed coverage-threshold regression in CI output   |
| 2026-06-04 15:10 | Root cause identified (missing test file from code generation) |
| 2026-06-04 16:00 | Fix merged; CI green                                           |
```

Use the repository's standard [Timestamp Format](../../formatting/timestamp.md) (UTC+7 WIB).

## 7. Root Cause

The deepest systemic condition that made the incident possible. A root cause explains **why**
the trigger was able to cause harm, not just what happened.

Distinguish from Trigger (below). Do not name a person as a root cause.

## 8. Trigger

The proximate event that started the incident chain — the "what pulled the thread." The trigger
is distinct from the root cause, which is the condition that made the trigger consequential.

Example distinction: Trigger = "Prettier reformatted a generated `.amazonq/` binding file after
an `Edit` operation"; Root Cause = "Generated output files were not listed in `.prettierignore`,
so the post-tool hook treated them as hand-authored content."

## 9. Contributing Factors

Systemic conditions that made the incident worse or made recovery harder. Use a bullet list.
These are **conditions**, not causes to blame.

Avoid single-cause fixation: most non-trivial incidents involve several compounding conditions.
Naming them all produces richer action items.

## 10. Resolution & Mitigations

Describe what restored service. Explicitly distinguish:

- **Applied fix**: what was done to resolve this incident
- **Open root-cause fix**: what still needs to happen to prevent recurrence (tracked in Action
  Items)
