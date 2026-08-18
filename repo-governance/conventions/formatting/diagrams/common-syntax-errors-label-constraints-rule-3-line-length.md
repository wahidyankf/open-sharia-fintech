---
title: "Common Mermaid Syntax Errors: Label Constraints — Rule 3, Maximum Line Length"
description: "Documents Rule 3: the 20-character maximum line length constraint for Mermaid labels, with examples."
when_to_use: "Use when a Mermaid label is too long and you need the exact line-length limit and how to shorten it."
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

# Common Mermaid Syntax Errors: Label Constraints — Rule 3, Maximum Line Length

Both node label lines (each segment between `<br/>` tags) and edge label strings must not exceed **20 characters**. Most Mermaid renderers clip text beyond approximately 20–22 characters with no error or warning.

Count every character including spaces, colons, slashes, and Unicode.

**Note**: `rhino-cli md mermaid validate` enforces ≤ **30** raw characters per `<br/>`-split line (Mermaid's `wrappingWidth` baseline). Use `--max-label-len 20` for stricter validation to guard against rendering clipping in some environments.

**Safe examples (≤20 chars):**

| Text                 | Length |
| -------------------- | ------ |
| `"Auth and profile"` | 16     |
| `"health check"`     | 12     |
| `"JWKS public key"`  | 15     |
| `"issues JWT"`       | 10     |

**Unsafe examples (>20 chars — will be clipped):**

| Text                                  | Length | Clipped rendering          |
| ------------------------------------- | ------ | -------------------------- |
| `"Single deployable backend process"` | 34     | `"Single deployable back"` |
| `"HTTPS: fetch JWKS public key"`      | 28     | `"HTTPS: fetch JWKS publ"` |
| `"GET /.well-known/jwks.json"`        | 26     | cut at `.well-known`       |

**DO:**

```mermaid
graph TD
    A["Backend process<br/>single deployable"]:::blue
    B[Client]-->|"JWKS public key"| A
    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF
```

**DO NOT:**

```mermaid
graph TD
    A["Single deployable<br/>backend process"]:::blue
    %% BROKEN: "Single deployable backend process" is 34 chars — clipped
    B[Client]-->|"HTTPS: fetch JWKS public key"| A
    %% BROKEN: "HTTPS: fetch JWKS public key" is 28 chars — clipped
    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF
```

**Technique**: Split long phrases across two `<br/>` segments, each ≤20 chars.

```mermaid
graph TD
    A["Backend process<br/>single deployable"]:::blue
    classDef blue fill:#0173B2,stroke:#000000,color:#FFFFFF
```
