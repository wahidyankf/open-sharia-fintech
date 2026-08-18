---
title: "Examples-by-Level Section: Slug Algorithm and Example Numbering"
description: "Details the github-slugger algorithm for anchor generation, why the Examples by Level section is required, a worked snippet, and the example numbering scheme."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when you need to compute a github-slugger anchor by hand, justify why the Examples by Level section exists, or determine sequential example numbering across levels."
---

# Examples-by-Level Section: Slug Algorithm and Example Numbering

## Slug algorithm reference

Use `github-slugger` (or its identical algorithm) — do not re-derive the rules from scratch.
Key slug behaviors relevant to example headings:

- Colons (`:`) are stripped (no replacement character).
- En-dashes (`–`) are preserved as `-`.
- Em-dashes (`—`) produce `--` (double hyphen).
- Words separated by a single space become a single `-`.
- Parentheses are stripped.

Examples:

| Heading text                                                      | Slug                                                        |
| ----------------------------------------------------------------- | ----------------------------------------------------------- |
| `### Example 1: States as a Sealed Type`                          | `example-1-states-as-a-sealed-type`                         |
| `### Example 15: Java Record + Enum Transition`                   | `example-15-java-record--enum-transition`                   |
| `### Example 37: PO Lifecycle Coverage — PartiallyReceived State` | `example-37-po-lifecycle-coverage--partiallyreceived-state` |

When in doubt, run `node -e "const s=require('github-slugger');console.log(s.slug('…'))"` with the
exact heading text to generate the correct anchor.

## Why this section is required

The `## Examples by Level` section lets readers scan the full curriculum — all 75-85 examples
across every level — from a single page without clicking into each level file. It also gives every
example a permanent, predictable URL that external documents, search engines, and cross-references
can link to reliably. Without it, discovering "which examples cover concurrency" requires opening
three separate level pages.

## Worked snippet (fictional `procurement-platform-be` tutorial)

```markdown
## Examples by Level

### Beginner (Examples 1–25)

- [Example 1: States as a Sealed Type](/en/learn/software-engineering/software-architecture/procurement-platform-be/by-example/beginner#example-1-states-as-a-sealed-type)
- [Example 2: The Minimal FSM Record](/en/learn/software-engineering/software-architecture/procurement-platform-be/by-example/beginner#example-2-the-minimal-fsm-record)

### Intermediate (Examples 26–50)

- [Example 26: Invoice States and the Three-Way Match](/en/learn/software-engineering/software-architecture/procurement-platform-be/by-example/intermediate#example-26-invoice-states-and-the-three-way-match)
- [Example 27: The Three-Way Match Guard](/en/learn/software-engineering/software-architecture/procurement-platform-be/by-example/intermediate#example-27-the-three-way-match-guard)
```

The live FSM by-example tutorial at
`apps/ayokoding-www/content/en/learn/software-engineering/software-architecture/finite-state-machine-fsm/by-example/overview.md`
follows this exact pattern and can be used as a reference implementation.

> **NOTE**: This section is automatically regenerable. If a heading on any level page changes,
> regenerate every affected bullet in the overview list (slug AND link text both change). Stale
> anchors silently 404 in browsers — treat this the same as a broken link.

## Example Numbering

**Sequential numbering across all levels**: Examples 1-75 to 1-85

**Typical distribution**:

- **Beginner**: Examples 1-30 (0-40% coverage)
- **Intermediate**: Examples 31-60 (40-75% coverage)
- **Advanced**: Examples 61-85 (75-95% coverage)

**Actual distributions in production** (ayokoding-www):

- Golang: 1-30 (beginner), 31-60 (intermediate), 61-85 (advanced)
- Python: 1-27 (beginner), 28-54 (intermediate), 55-80 (advanced)
- Rust: 1-28 (beginner), 29-57 (intermediate), 58-85 (advanced)

**Rationale**: Sequential numbering creates a unified reference system across the entire tutorial series, making it easy to reference specific examples ("see Example 42") without ambiguity.
