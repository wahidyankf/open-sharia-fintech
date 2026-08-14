---
title: "Programming Language Docs Separation: No Duplication and Cross-Referencing"
description: Rule 4 and Rule 5 of content separation — the decision tree for avoiding duplication between platforms, and the required cross-referencing link patterns
when_to_use: Read this when checking whether content duplicates ayokoding-www, or when adding the required cross-reference links between docs/explanation/ and ayokoding-www.
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

# Content Separation Rules: No Duplication and Cross-Referencing

## Rule 4: No Duplication Between Platforms

**CRITICAL**: Content covered in ayokoding-www MUST NOT be duplicated in docs/explanation/.

**Decision tree**:

```
Is this content about {LANGUAGE} fundamentals or generic patterns?
├─ Yes → ayokoding-www (educational content)
│   Examples: syntax, by-example code, generic error patterns, DDD in Go
│
└─ No → Is this content OSE Platform-specific?
    ├─ Yes → docs/explanation/ (style guide)
    │   Examples: "We use Gin for HTTP", "Name variables like this in OSE Platform"
    │
    └─ No → Still ayokoding-www (generic programming knowledge)
```

**Example - Error Handling**:

**ayokoding-www** (`apps/ayokoding-www/content/en/learn/.../golang/in-practice/error-handling.md`):

````markdown
# Error Handling in Go

This guide covers generic Go error patterns.

## Error Interface

Go's error interface is simple:

```go
type error interface {
    Error() string
}
```
````

Use `errors.New()` to create errors, `fmt.Errorf()` to wrap them...

````

**docs/explanation/** (`docs/explanation/.../golang/error-handling.md`):

```markdown
# Go Error Handling - OSE Platform Standards

**Prerequisite**: Complete [ayokoding-www Error Handling](https://ayokoding.com/en/learn/.../golang/in-practice/error-handling/) first.

## OSE Platform Error Standards

In OSE Platform, all errors MUST:

1. Use structured logging with `slog` package
2. Include request IDs for tracing
3. Follow error code taxonomy: `ERRZAKAT001`, `ERRWAQF001`

Example:

```go
// OSE Platform pattern
if err != nil {
    logger.Error("zakat calculation failed",
        "request_id", reqID,
        "error_code", "ERRZAKAT001",
        "error", err)
    return nil, fmt.Errorf("ERRZAKAT001: %w", err)
}
````

**Why**: Enables distributed tracing, compliance auditing, Shariah audit trails.

````

**Key differences**:

- **ayokoding-www**: Generic Go error patterns (what `error` interface is, how to use `errors.New()`)
- **docs/explanation/**: OSE Platform-specific error conventions (structured logging, error codes, audit requirements)

## Rule 5: Cross-Referencing Pattern

**Required linking between platforms**:

**From docs/explanation/ → ayokoding-www**:

```markdown
## Prerequisite Knowledge

**This documentation assumes you have completed the ayokoding-www {LANGUAGE} learning path**:

- [ayokoding-www {LANGUAGE} Overview](https://ayokoding.com/en/learn/.../programming-languages/{language}/)
- [By Example Tutorial](https://ayokoding.com/en/learn/.../programming-languages/{language}/by-example/)

If you're new to {LANGUAGE}, **start with ayokoding-www first**.
````

**From ayokoding-www → docs/explanation/** (optional, when relevant):

```markdown
## Repository-Specific Guides

For OSE Platform-specific {LANGUAGE} conventions, see:

- OSE Platform {LANGUAGE} Style Guide: `docs/explanation/software-engineering/programming-languages/{language}/`
```

**Linking rules**:

- docs/explanation/ README.md MUST link to ayokoding-www (prerequisite)
- ayokoding-www MAY link to docs/explanation/ (optional, for contributors)
- Use absolute URLs for ayokoding-www (Next.js site)
- Use relative paths for docs/explanation/ (GitHub markdown)
