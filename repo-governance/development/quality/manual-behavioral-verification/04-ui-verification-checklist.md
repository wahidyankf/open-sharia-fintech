---
title: "UI Verification Checklist"
description: "The checklist to run through when verifying a UI change."
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
when_to_use: "Use when manually verifying a UI change."
---

# UI Verification Checklist

After implementing a UI change, verify:

1. **Page renders**: Navigate to the page and take a snapshot. Confirm the expected elements are present.
2. **Interactions work**: Click buttons, fill forms, and navigate between pages. Confirm the expected behavior occurs.
3. **No console errors**: Check `browser_console_messages` for JavaScript errors or unexpected warnings.
4. **Network requests succeed**: Check `browser_network_requests` for failed API calls, unexpected 4xx/5xx responses, or missing requests.
5. **Visual correctness**: Take a screenshot and confirm the layout, typography, and content match expectations.
6. **All locales verified**: For multi-locale apps, repeat steps 1–5 for EVERY supported locale — navigate to each locale-prefixed URL (e.g., `/en/`, `/id/`). A UI change verified only in the default locale is incomplete. Confirm the `html[lang]` attribute matches each locale and that no strings are untranslated.
7. **All breakpoints verified**: Repeat at mobile (375 px), tablet (768 px), and desktop (1280 px). Responsive behavior at one viewport does not imply correct behavior at others.
   - **Presence is not legibility**: confirming an element is present at a breakpoint (via `browser_snapshot` or a DOM query) does not confirm it is legible. Read a computed style (e.g., font-size) or a bounding box for representative text elements at each breakpoint — an element can exist in the DOM while rendering too small to read, and a screenshot scaled into a review pane can hide a factor-of-two type-size error.
8. **Evidence captured**: Save one screenshot per breakpoint per locale to the plan's `evidence/` subfolder; reference each from the `delivery.md` implementation notes. See [Evidence Capture Convention](.././evidence-capture.md).
