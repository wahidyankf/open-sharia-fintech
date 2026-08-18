---
title: "Examples"
description: "Worked PASS/FAIL examples for this mandate."
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
when_to_use: "Use when you need a concrete pass/fail example."
---

# Examples

## PASS: Behavioral bug with Gherkin scenario

A developer discovers that the savings tab ignores the geographic filter and shows global
averages instead of city-specific figures.

They fix the filtering logic AND add:

1. A Gherkin scenario in `specs/apps/organiclever/behavior/.../calculator.feature`:

   ```gherkin
   Scenario: Savings tab respects the selected city filter
     Given I have selected "Kuala Lumpur" as my city
     When I navigate to the Savings tab
     Then all figures reflect Kuala Lumpur cost data
     And no global-average figures are shown
   ```

2. A unit test that calls the filter function with a city and asserts the output
   excludes global-average data.

The fix and the scenario land in the same commit. The mandate is satisfied.

## PASS: Visual regression with DOM assertion

A developer discovers that the currency input accepts non-numeric characters in production.
They fix the input validation AND add an E2E test:

```typescript
test("currency input rejects non-numeric characters", async ({ page }) => {
  await page.fill('[data-testid="currency-input"]', "abc");
  await expect(page.locator('[data-testid="currency-input"]')).toHaveValue("");
});
```

Fix + test land in the same commit. The mandate is satisfied.

## FAIL: Fix without a reproducing test

A developer discovers the hidden toggle controls visible output but has no visible affordance.
They add a label to make it discoverable but do not add a test asserting the label exists and
the toggle is accessible. The fix is incomplete -- the label can be removed in a future cleanup
without any automated gate objecting.

## FAIL: Fix in one commit, test in a later PR

A developer fixes a jargon label in commit A and says "I'll add the test in a follow-up PR."
The mandate requires both in the same commit or PR. The fix is incomplete until the test lands.
