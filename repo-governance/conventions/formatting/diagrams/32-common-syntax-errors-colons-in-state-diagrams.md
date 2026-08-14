---
title: "Common Mermaid Syntax Errors: Colons in State Diagram Edge Labels"
description: "Documents Error 6: how colons in Mermaid state diagram edge labels cause parse errors, with the fix."
when_to_use: "Use when a Mermaid state diagram edge label containing a colon fails to parse."
category: explanation
subcategory: conventions
tags:
  - diagrams
  - mermaid
  - ascii-art
  - visualization
  - conventions
  - accessibility
  - color-blindness
created: 2025-11-24
---

# Common Mermaid Syntax Errors: Colons in State Diagram Edge Labels

**CRITICAL**: In `stateDiagram-v2`, edge labels cannot contain colon characters (`:`).

**Syntax**: State diagram edge labels use the format `state1 --> state2: label text here`, where the colon after `state2` separates the transition from the label text.

**Problem**: If the label text itself contains colons (like Clojure keywords `:count` or `:users`, or other code snippets with colons), Mermaid's parser fails because the colon is a reserved separator character.

**Problem Example (FAIL: BROKEN)**:

```mermaid
stateDiagram-v2
    complex --> updated: swap! update :count inc
    updated --> final: swap! update :users conj
```

**Why it fails**: The parser sees `:count` and `:users` as additional syntax elements, not part of the label text. The first colon in the label text (`:` in `:count`) is interpreted as a new separator, breaking the parsing.

**Solution (PASS: WORKING)**:

Remove colons from edge label text. Use plain text descriptions instead of literal code syntax when colons are present:

```mermaid
stateDiagram-v2
    complex --> updated: swap! update count inc
    updated --> final: swap! update users conj
```

**Alternative - Descriptive Text**:

If the code syntax is critical to show, use descriptive text that avoids colons:

```mermaid
stateDiagram-v2
    complex --> updated: update count with increment
    updated --> final: add user to collection
```

**Rule**: Avoid colons in state diagram edge labels. Remove colons from code snippets in labels (e.g., use `count` instead of `:count` for Clojure keywords, use `key value` instead of `key: value` for object notation).

**Affected syntax**: `stateDiagram-v2` only. This does NOT affect:

- Flowchart edge labels (`graph TD` / `flowchart TD`) - colons work fine in flowchart edge labels
- Sequence diagram messages - different syntax, no issue with colons
- Node text in any diagram type - only affects state diagram edge labels

**Rationale**: In state diagrams, the colon is a structural syntax element that separates the transition from its label. Any additional colons in the label text create parsing ambiguity.

**Real-World Context**: This error was discovered when documenting Clojure state transitions using keywords like `:count` and `:users` in edge labels.
