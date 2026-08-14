# Operational Readiness and Manual Behavioral Assertion Verification

## 1. Verify Operational Readiness Execution (Step 5b — MANDATORY)

After assessing code quality (Step 5), verify that the executor followed ALL operational readiness
protocols. These are CRITICAL findings if missing.

### What to Validate

1. **Local Quality Gates Were Executed**
   - Check git log for evidence that quality gates were run before each push
   - Verify no lint, typecheck, or test failures remain in the affected projects
   - Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push` (the same registry-declared
     gate set `.husky/pre-push` invokes; includes `nx affected -t test:quick`) and confirm zero
     failures
   - If ANY failure exists, report as CRITICAL finding

2. **Post-Push CI Passed**
   - Check if every GitHub Actions workflow triggered by the latest commits passed on the plan's
     delivery target — the PR branch under `*-to-pr` modes, `main` under the direct-push modes
     (resolve the mode first; do not assume `main`)
   - If CI status is not all-green, report as CRITICAL finding
   - This includes workflows that may have been failing before the plan execution

3. **Preexisting Issues Were Fixed**
   - Review git log for fix commits addressing preexisting issues (e.g., `fix(lint): resolve
preexisting ...`)
   - Run quality gates to confirm no preexisting failures remain
   - If preexisting failures still exist in affected projects, report as HIGH finding
   - The root cause orientation principle requires proactive fixing of encountered issues

4. **Delivery.md Was Updated Progressively**
   - Verify ALL delivery checklist items are ticked (`- [x]`)
   - Verify each ticked item has implementation notes (Date, Status, Files Changed)
   - Verify items were ticked in sequential order (not batch-ticked at the end)
   - Check git history: delivery.md should have been committed progressively, not in one final
     commit
   - Missing implementation notes: MEDIUM finding per item
   - Unticked items: CRITICAL finding per item

5. **Thematic Commits Were Made**
   - Review git log for the plan execution period
   - Verify commits follow Conventional Commits format
   - Verify different concerns are in separate commits (not one giant commit)
   - Giant monolithic commits: HIGH finding
   - Missing conventional commit format: MEDIUM finding

6. **Environment Setup Was Performed**
   - Verify the plan included environment setup steps and they were completed
   - Check that `npm install` and `npm run doctor` were run (or equivalent)
   - Missing setup evidence: MEDIUM finding

### Finding Severity

- Quality gates not run / still failing: **CRITICAL**
- CI not passing: **CRITICAL**
- Delivery items not ticked: **CRITICAL**
- Preexisting issues not fixed: **HIGH**
- Monolithic commits: **HIGH**
- Missing implementation notes: **MEDIUM**
- Missing setup evidence: **MEDIUM**

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

5. **Evidence Capture**
   - Verify each ticked manual-verification checkbox carries committed evidence: **Screenshots** —
     the plan's `evidence/` subfolder contains at least one screenshot per locale per breakpoint
     tested, and `delivery.md` references them; **curl** — API-verification notes contain the
     command, HTTP status, and response body.
   - A bare "verified manually" note with NO screenshot and NO curl response: **HIGH** finding
   - UI-verification checkbox ticked but `evidence/` has zero screenshots for it: **HIGH** finding

6. **Rule-15 Three-Tester Retest (web-UI feature-change plans)**
   - If the plan was a web-UI **feature-change** plan, verify it carried a near-end "Rule-15
     three-tester retest" round — the
     [`web-ux-test-fixing-planning`](../../../../repo-governance/workflows/web/web-ux-test-fixing-planning.md)
     triad (`web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) — that ran across
     ALL supported locales, and that every resulting `EWT-###`/`UWT-###`/`DWT-###` defect checkbox in
     `delivery.md` is `- [x]` (fixed) before archival. Deferral of EWT/UWT/DWT defect findings is NOT
     permitted — an unfixed defect checkbox at archival time is a **HIGH** finding. (`SG-###`/`USS-###`
     are proposals, not defects, and may be triaged or deferred with written rationale.)
   - A web-UI feature-change plan archived with no three-tester retest round, single-locale-only
     scope, or any unfixed rule-15 defect checkbox: **HIGH** finding. CLI/text output and pure
     governance/agent-definition plans are exempt. Per
     [User-Facing Delivery Hardening](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
     Rule 15.

7. **Rule-16 API Exploratory Retest (API feature-change plans)**
   - If the plan was an API **feature-change** plan (REST or GraphQL endpoints in a backend or tRPC
     app), verify it carried a near-end "Rule-16 API exploratory retest" round —
     `api-exploratory-tester` run with `output-mode: delivery` against the running endpoint(s) with
     the contract (OpenAPI 3.x / GraphQL SDL) as ground truth — and that every resulting `AET-###`
     defect checkbox in `delivery.md` is `- [x]` (fixed) before archival. Deferral is NOT permitted —
     an unfixed defect checkbox at archival time is a **HIGH** finding.
   - An API feature-change plan archived with no API exploratory retest round, or any unfixed rule-16
     `AET-###` defect checkbox: **HIGH** finding. Frontend-only, CLI/text output, and pure
     governance/agent-definition plans are exempt. Per
     [User-Facing Delivery Hardening](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
     Rule 16.

### Finding Severity

- Broken UI (JS errors, rendering failures): **CRITICAL**
- Broken API (error responses, wrong data): **CRITICAL**
- Missing manual UI verification for UI changes: **HIGH**
- Missing manual API verification for API changes: **HIGH**
- End-to-end flow broken: **CRITICAL**
- Verification covered only the default locale on a multi-locale app: **HIGH**
- "Verified manually" with no committed evidence (no screenshot, no curl output): **HIGH**
- UI-verification checkbox ticked but no screenshot in `evidence/`: **HIGH**
