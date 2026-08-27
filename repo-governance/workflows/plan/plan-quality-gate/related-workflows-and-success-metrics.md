---
title: "Related Workflows and Success Metrics"
description: Lists the workflows plan-quality-gate composes with and the success metrics tracked across executions.
when_to_use: Use when navigating from plan-quality-gate to a composing workflow, or when reviewing its success-metric tracking.
---

# Related Workflows and Success Metrics

## Related Workflows

This workflow can be composed with:

- Content creation workflows (validate plans before creating content)
- Execution workflows (validate before starting implementation)
- Release workflows (validate plan completeness before release planning)
- [PR Leak Review](../../pr/pr-leak-review.md) — the mandatory current-head focused gate for
  `*-to-pr` delivery; broad semantic review remains explicit-only; see
  [Relationship to Delivery-Mode Done-Definition](./termination-criteria-and-delivery-mode-relationship.md#relationship-to-delivery-mode-done-definition)
  above

## Success Metrics

Track across executions:

- **Average iterations to completion**: How many cycles typically needed
- **Success rate**: Percentage reaching zero findings
- **Common finding categories**: What issues appear most often in plans
- **Fix success rate**: Percentage of fixes applied without errors
