---
title: "Manual Behavioural Assertions — Web UI and API Verification"
description: Defines the mandatory post-CI manual verification of web UI changes via Playwright MCP and API changes via curl.
when_to_use: Use when a phase touches web UI or API code and its behaviour must be manually verified before proceeding.
---

# Manual Behavioural Assertions — Web UI and API Verification

After CI is green, manually verify actual application behaviour using Playwright MCP and curl.
Evidence MUST be captured: screenshots committed to the plan's `evidence/` subfolder and
referenced in `delivery.md`; curl responses inlined as fenced code blocks. "Verified manually"
without evidence is incomplete. See [Evidence Capture Convention](../../../development/quality/evidence-capture.md).

**Orchestrator action**:

1. **For Web UI changes** — use Playwright MCP tools across ALL supported locales and breakpoints:
   - Discover supported locales: read `apps/<app>/src/features/i18n/` or `apps/<app>/next.config.ts`
   - Start dev server: `nx dev [project-name]`
   - For EACH locale (e.g., `en`, `id`) × EACH breakpoint (375 px, 768 px, 1280 px):
     - `browser_resize(width, 900)`
     - `browser_navigate` to the locale-prefixed URL (e.g., `/en/page`, `/id/page`)
     - `browser_snapshot` to inspect rendered DOM; verify `html[lang]` matches the locale
     - `browser_console_messages` to check for JS errors
     - `browser_network_requests` to verify API calls
     - `browser_take_screenshot` — save to `evidence/phase-{N}-{description}-{locale}-{breakpoint}px.png`
   - `browser_click`, `browser_fill_form` to test interactive flows (any locale sufficient for flow)
   - Record screenshot paths in `delivery.md` under the relevant checkbox per the Evidence Capture Convention
2. **For API changes** — use curl via Bash:
   - Start backend server: `nx dev [project-name]`
   - Hit affected endpoints with curl and verify response status, shape, and data
   - Test error cases with invalid payloads
