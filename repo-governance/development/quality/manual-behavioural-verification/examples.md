---
title: "Examples"
description: "Worked examples of manual behavioural verification."
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
when_to_use: "Use for a concrete example of this convention applied."
---

# Examples

## PASS: Complete verification workflow

```
1. Implement the feature (code changes)
2. Write/update automated tests (unit, integration, E2E as appropriate)
3. Run test:quick -- all pass
4. Start dev server
5. Manually verify UI renders correctly in ALL locales at ALL breakpoints
   (browser_navigate, browser_snapshot, browser_take_screenshot → evidence/)
6. Manually verify API responds correctly (curl → inline in delivery.md)
7. Check for console errors (browser_console_messages)
8. Record evidence: screenshot paths in delivery.md, curl output inline
9. Declare the feature complete
```

## FAIL: Skipping manual verification

```
1. Implement the feature
2. Write automated tests
3. Run test:quick -- all pass
4. Declare the feature complete
   [No manual verification -- visual regression ships to production]
```

## FAIL: Manual verification without automated tests

```
1. Implement the feature
2. Manually check it works in the browser
3. Declare the feature complete
   [No automated tests -- regression introduced in next commit]
```
