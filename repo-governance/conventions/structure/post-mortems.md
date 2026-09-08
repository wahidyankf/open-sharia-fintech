---
description: Standards for writing and organizing blameless incident post-mortems in this repository, including location, naming, mandatory sections, severity scale, and action-item tracking
when_to_use: Read this when you need to write, name, or review a blameless incident post-mortem, or to look up the mandatory sections and severity scale it must use.
---

# Post-Mortem Convention

This convention defines how to write, name, and organize blameless incident post-mortems for
this repository. Post-mortems are permanent retrospective documents that examine what happened
during a software incident, why it made sense at the time, and what systemic changes prevent
recurrence.

The practical writer-facing template and index live in
[`docs/explanation/post-mortems/README.md`](../../../docs/explanation/post-mortems/README.md).
This document is the **authoritative governance rule**; that directory is the working surface.
When the two disagree, the convention wins.

## In This Convention

- [Principles, Purpose, and Scope](./post-mortems/principles-purpose-and-scope.md) — why this convention exists, the principles it implements, and what it covers versus excludes
- [Location, Naming, Blameless Principle, and Timing](./post-mortems/naming-blameless-principle-and-timing.md) — filename rules, the blameless-culture standard, and when to write
- [Mandatory Sections: Frontmatter Through Detection](./post-mortems/mandatory-sections-frontmatter-through-detection.md) — required sections 1–5
- [Mandatory Sections: Timeline Through Resolution](./post-mortems/mandatory-sections-timeline-through-resolution.md) — required sections 6–10
- [Mandatory Sections: Action Items Through References](./post-mortems/mandatory-sections-action-items-through-references.md) — required sections 11–14
- [Optional Sections and Severity Scale](./post-mortems/optional-sections-and-severity-scale.md) — Background/Supporting Data, and the authoritative Sev-1 through Sev-4 tiers
- [No Secrets Rule, Diagrams, and Examples](./post-mortems/no-secrets-rule-diagrams-and-examples.md) — redaction requirements, diagram guidance, and worked PASS/FAIL examples
- [Validation and References](./post-mortems/validation-and-references.md) — the completion checklist and source references
