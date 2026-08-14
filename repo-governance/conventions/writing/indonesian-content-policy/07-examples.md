---
title: "Indonesian Content Policy — Examples"
description: Three worked examples — creating a technical tutorial under the English-first policy, creating unique Indonesian content, and handling an explicit translation request.
when_to_use: Use as a concrete template when creating a new technical tutorial, a unique Indonesian essay, or fulfilling an explicit translation request.
category: explanation
subcategory: conventions
tags:
  - ayokoding-www
  - indonesian
  - bilingual
  - content-policy
  - translation
created: 2026-02-07
---

# Examples

## Example 1: Creating Technical Tutorial (English-First Policy)

**Scenario**: AI agent creates new TypeScript tutorial

**PASS: Good (follows policy)**:

```bash
# Agent creates English tutorial only
# apps/ayokoding-www/content/en/learn/swe/programming-languages/typescript/tutorials/by-example/advanced.md

# No automatic Indonesian creation
# /id/belajar/swe/programming-languages/typescript/ does NOT exist
```

**FAIL: Bad (automatic mirroring)**:

```bash
# Agent creates English tutorial
# apps/ayokoding-www/content/en/learn/swe/programming-languages/typescript/tutorials/by-example/advanced.md

# Agent ALSO creates Indonesian mirror (WRONG!)
# apps/ayokoding-www/content/id/belajar/swe/programming-languages/typescript/tutorials/by-example/advanced.md
# This violates English-first policy unless explicitly requested
```

## Example 2: Creating Indonesian Unique Content

**Scenario**: Creating personal reflection on learning journey

**PASS: Good (unique Indonesian content)**:

```bash
# Create Indonesian personal essay (encouraged)
# apps/ayokoding-www/content/id/celoteh/2024/02/refleksi-belajar-golang.md
```

**Content Focus**:

- Personal learning journey
- Cultural challenges specific to Indonesian developers
- Local community experiences
- Career insights for Indonesian market

**No English Version Needed**: This content is inherently Indonesian-specific and valuable in original language.

## Example 3: Explicit Translation Request

**Scenario**: User specifically requests Indonesian translation of high-value tutorial

**User Request**:

```markdown
User: "Please translate the Golang Initial Setup tutorial to Indonesian. This is critical for beginners who struggle with English."
```

**PASS: Good (explicit request with justification)**:

```bash
# Create Indonesian translation
# apps/ayokoding-www/content/id/belajar/swe/programming-languages/golang/tutorials/initial-setup.md

# Add cross-reference in English version
echo "**Similar article:** [Pengaturan Awal Golang](/id/belajar/swe/programming-languages/golang/tutorials/initial-setup)" >> apps/ayokoding-www/content/en/learn/swe/programming-languages/golang/tutorials/initial-setup.md

# Add cross-reference in Indonesian version with machine translation disclaimer
echo "> _Artikel ini adalah hasil terjemahan dengan bantuan mesin..._" >> apps/ayokoding-www/content/id/belajar/swe/programming-languages/golang/tutorials/initial-setup.md
```

**Key Points**:

- Explicit user request
- Clear justification (accessibility for beginners)
- Cross-reference links in both versions
- Machine translation disclaimer in Indonesian version
- Maintenance commitment understood
