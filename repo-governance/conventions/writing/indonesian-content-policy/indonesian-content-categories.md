---
title: "Indonesian Content Policy — Indonesian Content Categories"
description: The three content categories — encouraged unique Indonesian content, strategic translations allowed on explicit request, and discouraged mirror translations.
when_to_use: Use when classifying a piece of proposed Indonesian content into the encouraged, allowed, or discouraged category before creating it.
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

# Indonesian Content Categories

## Category 1: Unique Indonesian Content (ENCOURAGED)

**Purpose**: Content specifically valuable to Indonesian audience that doesn't exist in English.

**Content Types**:

- **Personal Essays** (`/id/celoteh/`) - Indonesian-language reflections, opinions, cultural perspectives
- **Key Lessons** - Learning insights specifically for Indonesian developers
- **Cheat Sheets** - Quick reference cards in Indonesian
- **Video Content** (`/id/konten-video/`) - Indonesian-language video tutorials or explanations
- **Blog Posts** - Indonesian-language articles on tech culture, career advice, local ecosystem
- **Local Ecosystem Guides** - Indonesian tech community resources, events, job market insights

**Characteristics**:

- Content originates in Indonesian (not translated from English)
- Provides culturally-specific value
- Addresses Indonesian developer community needs
- Not duplicating English technical tutorials

**Example Structure**:

```
content/id/
├── celoteh/                           # Personal essays
│   └── 2024/
│       └── 01/
│           └── refleksi-belajar-golang.md
├── konten-video/                      # Video content
│   └── intro-programming.md
└── cheat-sheets/                      # Quick references
    └── git-commands-bahasa.md
```

## Category 2: Strategic Translations (ALLOWED WITH EXPLICIT REQUEST)

**Purpose**: Specific English content that provides exceptional value when translated to Indonesian.

**When to Translate**:

- User explicitly requests translation of specific content
- Content has demonstrated high value in English
- Translation provides significant accessibility benefit
- Resources available for ongoing maintenance

**Process**:

1. **Explicit Request**: Translation must be explicitly requested (never automatic)
2. **Value Assessment**: Evaluate if translation provides sufficient value
3. **Maintenance Commitment**: Confirm resources to keep translation updated
4. **Create Deliberately**: Translate as separate, intentional task

**Example Request Flow**:

```markdown
User: "Please translate the Golang Initial Setup tutorial to Indonesian"
Agent: Creates /id/belajar/swe/programming-languages/golang/tutorials/initial-setup.md
Agent: Adds cross-reference links in both English and Indonesian versions
```

## Category 3: Mirror Translations (DISCOURAGED)

**Purpose**: None - mirror translations are explicitly discouraged.

**Definition**: Automatically creating Indonesian versions of all English technical tutorials.

**Why Discouraged**:

- **Maintenance Burden**: Doubles update effort when English content changes
- **Outdated Content**: Indonesian versions lag behind English updates
- **Resource Waste**: Translation effort could create unique Indonesian content
- **False Value**: Provides illusion of bilingual support without quality guarantee

**Policy**: DO NOT create mirror translations unless explicitly requested and justified.
