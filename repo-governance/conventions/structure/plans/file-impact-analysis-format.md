---
title: "File-Impact Analysis Format (HARD RULE)"
description: Specifies the required annotated file-tree format for a plan's File-Impact Analysis section and the optional More Detail elaboration.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing or reviewing a plan's tech-docs.md File-Impact Analysis section.
---

# File-Impact Analysis Format (HARD RULE)

Every substantive plan's selected technical form MUST contain a `## File-Impact Analysis` whose
primary view is one root-relative, annotated file tree. In the directory form,
`tech-docs/README.md` either owns the section or maps the companion that owns it. The tree is the
scan-first source of truth for scope: a reviewer must identify every planned path, repository
location, and intended action without assembling information from prose bullets.

Use a fenced `text` block rooted at `.`. Annotate each leaf or bounded path family with its action:
**[E]** edit, **[N]** new file/pattern, **[D]** delete, or **[G]** generated/regenerated. A `*`
pattern is allowed only for a bounded, named family; state how its exact members will be discovered
before editing. Do not use an unbounded directory or a vague phrase such as “update related files”
in place of a path. Keep a short purpose beside each entry when the filename alone is insufficient.

When the tree cannot carry non-obvious execution context without becoming unreadable, place a
`### More Detail` section immediately after it. This section may explain cross-cutting mechanics,
ordering, discovery criteria, or archival follow-up, but it MUST map back to the tree and MUST NOT
replace it, repeat every path, or contain delivery checkboxes. Execution steps remain in
`delivery.md`.

```text
.
├── apps/example/
│   ├── project.json [E] — register the new target
│   ├── src/Feature.ts [N] — feature boundary
│   └── src/Legacy.ts [D] — superseded implementation
└── specs/apps/example/feature.feature [E] — companion behavior
```

## More Detail

`src/Feature.ts` is introduced only after the existing boundary is characterized. The exact test
files under the affected project are discovered from its project configuration and recorded in the
execution ledger before they are edited.
