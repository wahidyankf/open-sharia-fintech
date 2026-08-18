---
title: "Completeness Checklist"
description: "Checklist before declaring a bug fix complete."
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
when_to_use: "Use as a final check before declaring a bug fix done."
---

# Completeness Checklist

Before declaring a bug fix complete, verify:

- [ ] A test exists that targets the specific defect condition (not a general "happy path" test
      that happened to pass even when broken).
- [ ] The test is committed in the same PR or commit as the fix (not in a follow-up).
- [ ] The test slots into the correct level per the [Three-Level Testing Standard](.././three-level-testing-standard.md).
- [ ] For behavioral/functional defects: a Gherkin scenario in `specs/**` captures the correct
      expectation and the test that consumes it is updated.
- [ ] `test:quick` passes (including `specs:coverage`) after the fix + test are in place.
