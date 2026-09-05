# Rule 9: Manual Behavioural Assertion Validation (Step 5c — MANDATORY)

After Step 5b, verify manual behavioural assertion steps when applicable.

**What to validate**:

1. **Playwright MCP steps for web UI plans** — any web-frontend change (Next.js, Flutter Web, any UI
   project) needs `browser_navigate`, `browser_snapshot`, `browser_click`/`browser_fill_form`,
   `browser_console_messages`, `browser_take_screenshot` steps naming which pages/flows. Missing
   entirely: **CRITICAL**.
2. **curl steps for API plans** — any endpoint change (REST, tRPC, backend service) needs curl steps
   naming endpoint URLs, expected response shapes, error-case testing, health check, and affected
   endpoints. Missing entirely: **CRITICAL**.
3. **End-to-end flow assertion for full-stack plans** — UI-plus-API plans need full-flow assertion
   (UI → API → response → UI update). Missing entirely: **HIGH**.
4. **Locale coverage for multi-locale UI plans** — a frontend serving more than one locale (detect via
   `apps/<app>/src/features/i18n/` or locale-prefixed routes) needs verification across ALL supported
   locales (explicit "for each locale" or named locale URLs `/en/...`, `/id/...`). Single-locale-only:
   **HIGH**. Per
   [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md)
   and
   [Manual Behavioural Verification](../../../../repo-governance/development/quality/manual-behavioural-verification.md).
5. **Evidence Capture Steps** — every manual-verification section needs evidence-capture steps:
   screenshots to `evidence/` (named `phase-N-<description>-<locale>-<breakpoint>px.png`) referenced
   in `delivery.md`; curl responses inlined as fenced code blocks or saved to `evidence/`. Section
   present but no evidence-capture step: **HIGH**.
6. **Not-applicable exemption** — plans touching only docs/governance/non-code files don't need
   manual assertions; verify the exemption is legitimate (genuinely no UI/API changes).

**Finding severity**: missing Playwright steps for UI plan: **CRITICAL**. Missing curl steps for API
plan: **CRITICAL**. Missing end-to-end flow for full-stack plan: **HIGH**. Single-locale-only on
multi-locale app: **HIGH**. Missing evidence-capture steps: **HIGH**. Steps present but vague (no
specific pages/endpoints): **MEDIUM**.
