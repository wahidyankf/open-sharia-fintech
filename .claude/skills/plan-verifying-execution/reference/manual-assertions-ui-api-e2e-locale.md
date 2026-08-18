# Manual Behavioral Assertion Verification (Step 5c): UI, API, End-to-End, Locale

## 2. Verify Manual Behavioral Assertions (Step 5c — MANDATORY)

After verifying operational readiness (Step 5b), verify that manual behavioral assertions were
performed.

### What to Validate

1. **Playwright MCP Assertions for Web UI Changes**
   - If the plan touched any web frontend, check delivery.md for "Manual UI Verification" notes
   - Start the dev server and use Playwright MCP to independently verify key UI flows:
     `browser_navigate` to affected pages, `browser_snapshot` to inspect DOM state,
     `browser_console_messages` to check for JS errors, `browser_network_requests` to verify API
     integration
   - If UI is broken or has JS console errors: CRITICAL finding
   - If no manual UI verification was documented but plan touched UI: HIGH finding

2. **curl Assertions for API Changes**
   - If the plan touched any API endpoint, check delivery.md for "Manual API Verification" notes
   - Start the backend server and use curl to independently verify key endpoints
     (`curl -s http://localhost:[port]/api/health | jq .`, then the affected endpoint)
   - If API returns errors or unexpected responses: CRITICAL finding
   - If no manual API verification was documented but plan touched API: HIGH finding

3. **End-to-End Flow Verification**
   - If the plan touches both UI and API, verify the full flow: use Playwright MCP to interact with
     the UI, verify that UI actions trigger correct API calls (`browser_network_requests`), verify API
     responses are correctly rendered in the UI
   - If end-to-end flow is broken: CRITICAL finding

4. **Locale Coverage (multi-locale apps)**
   - If the plan touched a web frontend serving more than one locale (detect via
     `apps/<app>/src/features/i18n/` or locale-prefixed routes `/en/`, `/id/`), verify the delivery
     notes show UI verification was performed for ALL supported locales, not just the default.
     Independently spot-check: `browser_navigate` to a non-default locale URL and confirm `html[lang]`
     matches and content is translated.
   - Verification documented for only the default locale on a multi-locale app: **HIGH** finding
   - Per the
     [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
