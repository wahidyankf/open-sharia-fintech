---
title: "Related Documentation"
description: "Cross-references to related testing and sync conventions."
category: explanation
subcategory: development
tags:
  - regression
  - testing
  - bug-fix
  - quality
  - gherkin
  - specs
created: 2026-06-22
when_to_use: "Use when you need a related convention on testing or specs sync."
---

# Related Documentation

- [Feature Change Completeness Convention](.././feature-change-completeness.md) -- The feature-change
  dual of this mandate; together they cover all behavior-altering work
- [Three-Level Testing Standard](.././three-level-testing-standard.md) -- Which test level applies
  to which defect type
- [Code Quality Convention](.././code.md) -- Automated quality gates that run the regression suite
- [Test-Driven Development Convention](../../workflow/test-driven-development.md) -- Red→Green→Refactor
  cycle; a reproducing test is the natural RED step for a bug fix
- [Specs-Application Sync Convention](.././specs-application-sync.md) -- Bidirectional sync between
  specs/ and application code; behavioral regression tests belong in specs/
- [Live-Tester Systematic Coverage](.././live-tester-systematic-coverage.md) -- How the three live-site
  testers find defects that become inputs to this mandate
