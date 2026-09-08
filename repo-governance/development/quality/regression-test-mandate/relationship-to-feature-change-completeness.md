---
description: "How this mandate and Feature Change Completeness divide obligations."
when_to_use: "Use when deciding which rule(s) a change needs."
---

# Relationship to Feature Change Completeness

[Feature Change Completeness](.././feature-change-completeness.md) asks: _does this feature change
land with all its companion artifacts?_ This mandate asks: _does this bug fix land with a
reproducing test?_

They are complementary, not overlapping:

| Work type                     | Governing rule              | Artifact required                                   |
| ----------------------------- | --------------------------- | --------------------------------------------------- |
| New or modified feature       | Feature Change Completeness | Gherkin specs + contracts + tests + documentation   |
| Bug fix (spec was correct)    | **This mandate**            | Reproducing test only (spec was already right)      |
| Bug fix (spec was also wrong) | Both rules                  | Updated spec + reproducing test + related artifacts |

The table in Feature Change Completeness that reads _"Bug fix that matches existing spec → Tests
only (add regression test)"_ is the same obligation stated at a higher level of abstraction.
This document makes that obligation explicit, names it, and declares it BLOCKING.
