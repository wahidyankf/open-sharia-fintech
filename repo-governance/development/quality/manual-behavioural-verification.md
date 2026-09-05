---
title: "Manual Behavioural Verification Convention"
description: Practice requiring manual verification of UI features and API endpoints using Playwright MCP tools and curl after implementing changes
category: explanation
subcategory: development
tags:
  - verification
  - testing
  - playwright
  - api
  - quality
  - manual-testing
created: 2026-04-04
when_to_use: "Use after implementing a UI or API change, before declaring it done."
---

# Manual Behavioural Verification Convention

This convention requires manually verifying UI features and API endpoints -- via Playwright MCP tools and curl -- after implementing a change, in addition to any automated tests.

## Documents

- [Principles and Conventions Implemented/Respected](./manual-behavioural-verification/principles-and-conventions-implemented-respected.md) — Principles/conventions this convention implements. Use when tracing this convention's rationale.
- [The Rule](./manual-behavioural-verification/the-rule.md) — The manual-verification rule for UI/API changes. Use for the exact wording of the rule.
- [UI Verification](./manual-behavioural-verification/ui-verification.md) — Required tools for manual UI verification. Use when preparing to manually verify a UI change.
- [UI Verification Checklist](./manual-behavioural-verification/ui-verification-checklist.md) — The checklist to run through when verifying a UI change. Use when manually verifying a UI change.
- [Example: UI Feature Verification (multi-locale app)](./manual-behavioural-verification/example-ui-feature-verification-multi-locale-app.md) — A worked example of manually verifying a UI feature across locales. Use for a concrete example of multi-locale UI verification.
- [API Verification](./manual-behavioural-verification/api-verification.md) — How to manually verify an API endpoint with curl. Use when preparing to manually verify an API change.
- [When Verification Is Required](./manual-behavioural-verification/when-verification-is-required.md) — The triggers that require manual behavioural verification. Use when deciding whether a change needs manual verification.
- [Relationship to Automated Tests](./manual-behavioural-verification/relationship-to-automated-tests.md) — How manual verification relates to automated test coverage. Use when deciding whether automated tests already cover manual verification.
- [Examples](./manual-behavioural-verification/examples.md) — Worked examples of manual behavioural verification. Use for a concrete example of this convention applied.
- [Scope](./manual-behavioural-verification/scope.md) — What this convention applies to and its boundaries. Use when checking whether this convention applies to a change.
- [Tools and Automation](./manual-behavioural-verification/tools-and-automation.md) — Tools used for manual behavioural verification. Use when locating a manual-verification tool.
- [Related Documentation](./manual-behavioural-verification/related-documentation.md) — Related testing and evidence conventions. Use for a related convention on testing or evidence.
