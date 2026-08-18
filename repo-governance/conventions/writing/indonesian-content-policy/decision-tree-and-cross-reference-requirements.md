---
title: "Indonesian Content Policy — Decision Tree and Cross-Reference Requirements"
description: The decision tree for whether to create Indonesian content, a content-type example table, and the mandatory cross-reference links when translations exist.
when_to_use: Use when unsure whether a specific piece of content should be Indonesian or English, or when a translation exists and needs cross-reference links.
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

# Decision Tree and Cross-Reference Requirements

## Decision Tree: Should I Create Indonesian Content?

Use this decision tree when considering Indonesian content creation:

```
START: Should I create Indonesian content?
│
├─ Is this a programming tutorial or technical reference?
│  ├─ Yes → Has user EXPLICITLY requested Indonesian translation?
│  │  ├─ Yes → Create Indonesian translation with maintenance commitment
│  │  └─ No → Create in ENGLISH only
│  │
│  └─ No → Is this personal essay, opinion, or culturally-specific?
│     ├─ Yes → Create in INDONESIAN (encouraged)
│     └─ No → Consider value proposition
│        ├─ High unique value → Create in INDONESIAN
│        └─ Low unique value → Create in ENGLISH
```

**Examples by Content Type**:

| Content Type                      | Default Language | Indonesian Version?              | Rationale                                   |
| --------------------------------- | ---------------- | -------------------------------- | ------------------------------------------- |
| Golang By-Example Tutorial        | English          | No (unless explicitly requested) | Technical tutorial, English-first policy    |
| Personal Reflection on Learning   | Indonesian       | Yes (encouraged)                 | Culturally-specific, unique value           |
| TypeScript Intermediate Tutorial  | English          | No (unless explicitly requested) | Technical tutorial, English-first policy    |
| Indonesian Tech Community Guide   | Indonesian       | Yes (encouraged)                 | Local ecosystem content                     |
| Java Quick Start                  | English          | No (unless explicitly requested) | Technical tutorial, English-first policy    |
| Git Cheat Sheet (Bahasa)          | Indonesian       | Yes (encouraged)                 | Quick reference, accessibility value        |
| React Hooks Explanation           | English          | No (unless explicitly requested) | Technical explanation, English-first policy |
| Career Advice for Indonesian Devs | Indonesian       | Yes (encouraged)                 | Culturally-specific career guidance         |

## Cross-Reference Requirements

**CRITICAL**: When Indonesian translations DO exist (by explicit request), both English and Indonesian versions MUST include cross-reference links.

**English Original → Indonesian Translation**:

```markdown
**Similar article:** [Judul Artikel Indonesia](/id/belajar/path/to/article)
```

**Indonesian Translation → English Original**:

```markdown
> _Artikel ini adalah hasil terjemahan dengan bantuan mesin. Karenanya akan ada pergeseran nuansa dari artikel aslinya. Untuk mendapatkan pesan dan nuansa asli dari artikel ini, silakan kunjungi artikel yang asli di: [English Article Title](/en/learn/path/to/article)_
```

**See**: [Programming Language Content Standard](../../tutorials/programming-language-content.md) for complete content standards.
