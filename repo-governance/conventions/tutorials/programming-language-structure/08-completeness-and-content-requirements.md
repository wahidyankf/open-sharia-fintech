---
title: "Full Set Completeness and Content Requirements"
description: The five mandatory-component completeness checklist plus frontmatter, link, overview-file, and index-file content requirements.
when_to_use: Use when verifying a language's Full Set Tutorial Package is complete or when writing tutorial file content and frontmatter.
category: explanation
subcategory: conventions
tags:
  - programming-languages
  - tutorials
  - ayokoding-www
  - education
  - structure
created: 2025-12-27
---

# Full Set Completeness and Content Requirements

## Full Set Completeness Requirements

**All 5 components are mandatory** for complete Full Set Tutorial Package:

✅ **Component 1**: initial-setup.md (0-5% coverage)
✅ **Component 2**: quick-start.md (5-30% coverage)
✅ **Component 3**: by-example/ folder (95% coverage, code-first) - **PRIORITY**
✅ **Component 4**: by-concept/ folder (95% coverage, narrative-driven)
✅ **Component 5**: cookbook/ folder (practical recipes)

**Creation Order** (recommended for fast learning):

1. Initial Setup (minimal viable content)
2. Quick Start (core concepts)
3. By-Example (75-85 annotated examples for fast pickup) - **CREATE FIRST for speed**
4. Cookbook (30+ recipes alongside by-example development)
5. By-Concept (complete beginner → intermediate → advanced for deep learning)

**Quality Gate**: A language is NOT complete until all 5 components exist and pass validation. Languages can be production-ready with a subset of components.

## Content Requirements

### Frontmatter

All tutorial files follow this frontmatter format:

```yaml
---
title: "Tutorial Title"
date: 2025-12-27T10:00:00+07:00
draft: false
description: "Brief description for SEO"
weight: [level-based weight]
tags: ["language-name", "tutorial-type", "skill-level"]
---
```

**Rules:**

- **No categories field**: Not used in ayokoding-www content
- **No author field**: Not used in ayokoding-www content
- **Date format**: UTC+7 with ISO 8601 format
- **Weight field**: MANDATORY - uses level-based system
- **Tags**: JSON array format `["tag1", "tag2"]` (NOT dash-based YAML)

### Internal Links

**CRITICAL**: All internal links MUST use absolute paths with language prefix.

**Format:**

```markdown
[Display Text](/[language]/learn/software-engineering/programming-language/[language]/tutorials/[path])
```

**Examples:**

```markdown
- [By Concept](/en/learn/software-engineering/programming-language/java/tutorials/by-concept)
- [By Example](/en/learn/software-engineering/programming-language/java/tutorials/by-example)
- [Initial Setup](/en/learn/software-engineering/programming-language/java/tutorials/initial-setup)
- [Beginner Tutorial](/en/learn/software-engineering/programming-language/java/tutorials/by-concept/beginner)
```

**Why absolute paths?**

- Relative paths break when content is rendered in different contexts (sidebar, mobile menu, homepage)
- Absolute paths work from ANY page context
- Language prefix ensures correct bilingual routing

### Overview Files

Both by-concept/ and by-example/ MUST have overview.md files:

**by-concept/overview.md:**

- Explains narrative-driven learning approach
- Describes comprehensive coverage philosophy
- Links to Programming Language Content Standard
- Sets expectations for deep explanations

**by-example/overview.md:**

- Explains code-first learning approach
- Describes 75-90 annotated examples
- Links to By Example Tutorial Convention
- Sets expectations for experienced developers
- Clarifies NOT a replacement for by-concept

### Index Files

All directories MUST have `_index.md` navigation hubs:

```
tutorials/_index.md         # Lists by-concept/, by-example/, initial-setup, quick-start
by-concept/_index.md        # Lists overview, beginner, intermediate, advanced
by-example/_index.md        # Lists overview, beginner, intermediate, advanced
```

**Navigation Pattern**: 2-layer depth with complete coverage (show all immediate children).
