# Manual Behavioral Assertions — UI (Playwright) and API (curl)

When the plan touches web UI or API code, delivery plans MUST include manual assertion sections.
**Two hard requirements bind every manual-assertion section:**

1. **Locale coverage** — for a **multi-locale** app, every UI-verification step runs across ALL
   supported locales (e.g. `en` AND `id`), never just the default. Discover the locale set from
   `apps/<app>/src/features/i18n/` or `next.config.ts`. Single-locale verification on a bilingual app
   is INCOMPLETE.
2. **Evidence capture** — every manual-verification step produces a committed artifact: screenshots
   in the plan's `evidence/` subfolder (named `phase-N-<description>-<locale>-<breakpoint>px.png`),
   curl responses inlined in `delivery.md`. See the
   [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).

## For Web UI Plans — Playwright MCP

```markdown
### Manual UI Verification (Playwright MCP) — all locales × all breakpoints

- [ ] [AI] Discover supported locales: read `apps/[app]/src/features/i18n/` or `next.config.ts`
- [ ] [AI] Start dev server: `nx dev [project-name]`
- [ ] [AI] For EACH locale × EACH breakpoint (375 / 768 / 1280 px): navigate to the locale-prefixed
      URL (`/en/...`, `/id/...`) via `browser_navigate` + `browser_resize`
- [ ] [AI] Inspect DOM via `browser_snapshot` — verify `html[lang]` matches the locale, no untranslated strings
- [ ] [AI] Test interactive flows via `browser_click` / `browser_fill_form`
- [ ] [AI] Check for JS errors via `browser_console_messages` — must be zero errors per locale
- [ ] [AI] Verify API integration via `browser_network_requests`
- [ ] [AI] Capture one screenshot per locale per breakpoint via `browser_take_screenshot`, saved to
      `evidence/phase-N-[feature]-[locale]-[breakpoint]px.png`
- [ ] [AI] Document evidence in this checklist: reference each screenshot (`![alt](./evidence/...)`)
```

## For API Plans — curl

```markdown
### Manual API Verification (curl)

- [ ] [AI] Start backend server: `nx dev [project-name]`
- [ ] [AI] Verify health endpoint: `curl -s http://localhost:[port]/api/health | jq .` — paste response inline
- [ ] [AI] Verify affected endpoints return expected responses — paste command + status + body inline
- [ ] [AI] Test error cases with invalid payloads — verify proper error responses
- [ ] [AI] For locale-sensitive responses, verify each locale via `Accept-Language` header
- [ ] [AI] Document evidence: inline curl command + status + body (or save responses > 20 lines to `evidence/`)
```

## For Full-Stack Plans — Both + End-to-End

Include both sections above plus an end-to-end flow verification step (per locale).

See [20-manual-verification-retest-rules.md](manual-verification-retest-rules.md) for the mandatory rule-15/rule-16 pre-archival retests.
