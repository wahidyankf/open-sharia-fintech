---
title: "Example Usage"
description: A worked transcript of the UI quality gate running end to end in strict mode.
when_to_use: Use when you want to see what a UI quality gate run looks like in practice.
---

# Example Usage

```text
User: "Run UI quality gate for libs/web-ui/ in strict mode"

AI: Invoking swe-ui-checker for libs/web-ui/...
    Found 12 findings (3 HIGH, 5 MEDIUM, 4 LOW)
    Invoking swe-ui-fixer with audit report...
    Fixed 7 validated findings; recorded 1 FALSE_POSITIVE and 4 below-threshold findings
    Verifying the original findings and smoke-testing affected components...
    Original findings resolved; regression smoke passed
    Final status: PASS
    Lifecycle status: VERIFIED
```
