---
title: "The Offload Decision Tree"
description: "The decision tree for choosing an offload option."
category: explanation
subcategory: development
tags:
  - content-preservation
  - condensation
  - offload
  - zero-loss
  - documentation
created: 2025-12-14
when_to_use: "Use when deciding which of the four offload options to apply."
---

# The Offload Decision Tree

When condensing content, ask these questions:

```
Is this content unique and valuable?
 │
 ├─ YES → Offload to convention OR development doc
 │   │
 │   ├─ Is this about HOW we write/format?
 │   │   └─> repo-governance/conventions/
 │   │
 │   ├─ Is this about HOW we work/process?
 │   │   └─> repo-governance/development/
 │   │
 │   ├─ Does convention/development doc exist?
 │   │   ├─ YES → Option B: Merge into existing doc
 │   │   └─ NO → Option A: Create new doc
 │   │
 │   └─ Is this pattern shared across multiple files?
 │       ├─ YES → Option C: Extract common pattern to shared doc
 │       └─ NO → Option D: Add to appropriate folder (conventions/ or development/)
 │
 ├─ NO (duplicated from conventions/development) → Link instead of duplicate
 │
 └─ UNSURE (agent-specific implementation) → Keep in agent file
```
