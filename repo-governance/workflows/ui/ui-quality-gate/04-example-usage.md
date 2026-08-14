---
title: "Example Usage"
description: A worked transcript of the UI quality gate running end to end in strict mode.
when_to_use: Use when you want to see what a UI quality gate run looks like in practice.
---

# Example Usage

```
User: "Run UI quality gate for libs/web-ui/ in strict mode"

AI: Invoking swe-ui-checker for libs/web-ui/...
    Found 12 findings (3 HIGH, 5 MEDIUM, 4 LOW)
    Invoking swe-ui-fixer with audit report...
    Fixed 10 findings, 2 remaining (1 MEDIUM confidence, 1 FALSE_POSITIVE)
    Re-validating...
    Found 0 findings
    Confirmation check: 0 findings
    Status: PASS (2 iterations)
```
