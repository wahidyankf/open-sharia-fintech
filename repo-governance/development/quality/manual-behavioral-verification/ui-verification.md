---
title: "UI Verification"
description: "Required tools for manual UI verification."
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
when_to_use: "Use when preparing to manually verify a UI change."
---

# UI Verification

Before browser-facing verification, discover the real-browser integrations installed on the machine
and confirm which are healthy and callable in the current harness. Prefer Playwright MCP first, then
Chrome DevTools MCP; if neither is available, use an equivalent installed browser-driving
integration. Record the selected tool, any fallback, browser/version when available, and capability
gaps in the verification evidence. Static source, fetched HTML, WebFetch, and curl inspection are
useful baselines, but do not count as live-browser verification when a working browser integration
exists.

## Required Tools

| Tool                       | Purpose                                                |
| -------------------------- | ------------------------------------------------------ |
| `browser_navigate`         | Open the relevant page                                 |
| `browser_snapshot`         | Capture the current DOM state for inspection           |
| `browser_click`            | Interact with buttons, links, and interactive elements |
| `browser_fill_form`        | Fill form fields to test input handling                |
| `browser_console_messages` | Check for JavaScript errors, warnings, and logs        |
| `browser_take_screenshot`  | Capture visual evidence of the rendered state          |
| `browser_network_requests` | Verify API calls, response codes, and payload shapes   |
