---
description: The required template and worked PASS/FAIL examples for the prerequisite-knowledge statement every language style guide README must include
when_to_use: Read this when writing or reviewing the Prerequisite Knowledge section of a docs/explanation/ programming-language README.
---

# Rule 3: Explicit Prerequisite Knowledge Statements

**REQUIRED**: Every `docs/explanation/software-engineering/programming-languages/{language}/README.md` MUST include explicit prerequisite knowledge statement linking to ayokoding-www.

**Template**:

```markdown
## Prerequisite Knowledge

**This documentation assumes you have completed the ayokoding-www {LANGUAGE} learning path**:

- [ayokoding-www {LANGUAGE} Overview](https://ayokoding.com/en/learn/software-engineering/programming-languages/{language}/)
- [By Example Tutorial](https://ayokoding.com/en/learn/software-engineering/programming-languages/{language}/by-example/) (0-95% coverage, 75-85 examples)
- [In Practice Guides](https://ayokoding.com/en/learn/software-engineering/programming-languages/{language}/in-practice/)

If you're new to {LANGUAGE}, **start with ayokoding-www first**. This documentation focuses exclusively on OSE Platform-specific style guides and conventions, not language fundamentals.

## What This Documentation Covers

This documentation is the **authoritative reference for {LANGUAGE} coding standards in the OSE Platform**. It covers:

- Repository-specific naming conventions
- Framework choices and rationale (why we chose X)
- Architecture patterns specific to OSE Platform
- Anti-patterns to avoid in OSE Platform context
- Alignment with [Software Engineering Principles](../../principles/software-engineering/README.md)

**This is NOT a {LANGUAGE} tutorial** - see ayokoding-www for comprehensive language education.
```

**Examples**:

**PASS: Clear prerequisite statement**:

```markdown
## Prerequisite Knowledge

**This documentation assumes you have completed the ayokoding-www Rust learning path**:

- [ayokoding-www Rust Overview](https://ayokoding.com/en/learn/software-engineering/programming-languages/rust/)
- [By Example Tutorial](https://ayokoding.com/en/learn/software-engineering/programming-languages/rust/by-example/)

If you're new to Rust, **start with ayokoding-www first**.
```

**FAIL: No prerequisite statement**:

```markdown
# Rust

Rust is used for high-performance services...

## Best Practices

Use channels for concurrency...
```

**Why it fails**: Doesn't tell developers where to learn Rust fundamentals. Assumes knowledge.
