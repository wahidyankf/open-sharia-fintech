---
title: "Test Form by Defect Type"
description: "Required test form per defect type: behavioural, visual, content, integration."
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
when_to_use: "Use when deciding what kind of test a defect type requires."
---

# Test Form by Defect Type

The obligation is uniform; the form adapts:

| Defect type                         | Required test form                                                                                                                                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Behavioural / functional**        | A Gherkin scenario in `specs/**` (preferred) expressing the correct behaviour -- plus the unit, integration, or E2E test that consumes it per the [Behaviour-Driven Development](../../behaviour-driven-development.md). |
| **Visual / design / UI regression** | A DOM assertion, a computed-style assertion, a Playwright snapshot assertion, or a Gherkin scenario capturing the on-design expectation -- whichever level can assert the specific visual property that was wrong.       |
| **Content / copy / i18n**           | A test asserting the corrected string, translation key, or rendered text -- at the unit level if the string is in logic, at E2E level if it is rendered.                                                                 |
| **Integration / API regression**    | An integration or E2E test asserting the correct response shape, status code, or state transition.                                                                                                                       |

The common thread: the test must make the specific defect _impossible to silently reintroduce_.
A test that passes even on the broken version does not satisfy this mandate.
