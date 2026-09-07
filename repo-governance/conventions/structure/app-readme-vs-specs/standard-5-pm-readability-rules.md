---
description: The six authoring rules that make specs/apps/ files readable by a SWE-background TPM — header block, intent-before-mechanism, scoped glossing, tables, introduced code blocks, and links forward.
when_to_use: Use when authoring or reviewing a specs/apps/ file against the six PM-readability rules.
---

# Standard 5 — PM-Readability Contract for specs/ (Rules 1-6)

## Rule 1 — Required header block

Every spec file starts with this block (first 10 lines after H1):

```markdown
# <Title>

> **Audience**: Engineers, Technical Product/Project Managers
>
> **Plain-language summary**: <one paragraph free of jargon for the niche
> stack choices and DDD-applied vocabulary; mainstream SWE vocabulary is fine.
> A SWE-background TPM should be able to form a working mental model on first read.>

## <First section heading>
```

## Rule 2 — Intent before mechanism

Every section leads with what the feature or component enables for the user (1-2 sentences) before describing how the code is shaped. A SWE-background TPM should be able to read the first paragraph of any section and walk away knowing the user-facing point.

```markdown
<!-- FAIL: opens with mechanism -->

## Journal Context

The journal context owns the `JournalEvent` aggregate and exposes `appendEvent` use-cases via PGlite store.

<!-- PASS: opens with intent, mechanism follows -->

## Journal Context

The journal records every life-event the user logs. It is the system of record — every other feature reads from or writes to here.

Under the hood the context owns the `JournalEvent` aggregate (Domain-Driven Design — a cluster of domain objects treated as one consistent unit by writes) and exposes three use-cases backed by a PGlite (Postgres-WASM — Postgres compiled to WebAssembly running directly in the browser) store.
```

## Rule 3 — Glossary on first use, scoped narrowly

The first occurrence of each niche project-specific term in a file carries a parenthetical gloss. Subsequent uses in the same file are gloss-free. Only the terms listed in the [glossary table](./standard-5-pm-readability-glossary.md) need glossing — anything not on that list is mainstream and must NOT be glossed.

## Rule 4 — Tables over prose where possible

Routes, screens, endpoints, environment variables, and feature lists are presented as tables. SWE-background TPMs scan tables faster than prose.

## Rule 5 — Code blocks are introduced

Every code or Mermaid block is preceded by a one-sentence "what this shows" introduction. The intro lets readers decide whether to read the block.

## Rule 6 — Link forward to engineering depth

When a section requires hands-on engineering depth (e.g., DDD layer rules with ESLint boundary enforcement, Effect Layer composition), the section opens with a one-line TPM-skim cue and links to a deeper subsection or external doc.
