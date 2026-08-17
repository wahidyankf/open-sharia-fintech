---
title: "Agents"
description: The maker, checker, and fixer agents that create and validate content under this programming-language documentation separation convention
when_to_use: Read this when you need to find which agent creates, validates, or fixes docs/explanation/ or ayokoding-www programming-language content.
category: explanation
subcategory: conventions
tags:
  - documentation
  - programming-languages
  - style-guides
  - content-separation
  - dry-principle
created: 2026-02-04
---

# Agents

**Makers**:

- `docs-maker` - Creates style guide content in docs/explanation/ following this convention
- `apps-ayokoding-www-general-maker` - Creates educational content in ayokoding-www following this convention
- `apps-ayokoding-www-by-example-maker` - Creates by-example tutorials following separation rules

**Checkers**:

- `docs-checker` - Validates style guides follow this convention (prerequisite statements, no duplication)
- `apps-ayokoding-www-general-checker` - Validates educational content scope (no OSE Platform-specific content)
- `apps-ayokoding-www-facts-checker` - Validates factual correctness of educational content

**Fixers**:

- `docs-fixer` - Fixes style guide violations (adds missing prerequisite statements, removes duplicated content)
- `apps-ayokoding-www-general-fixer` - Fixes educational content violations (removes OSE Platform-specific content)

---

**Scope**: Every language with a style guide under `docs/explanation/software-engineering/programming-languages/` (today TypeScript, Rust, F#) and every language AyoKoding teaches. Read those two indexes rather than a fixed list here.
**Maintainers**: Repository Governance Team
