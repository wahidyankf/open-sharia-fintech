---
title: "Manual Behavioral Verification Convention"
description: Practice requiring manual verification of UI features and API endpoints using Playwright MCP tools and curl after implementing changes
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
---

# Manual Behavioral Verification Convention

After implementing UI or API changes, manual behavioral verification is **mandatory** -- not optional. Automated tests validate correctness at the code level; manual verification validates that the feature actually works as a user or consumer would experience it. Both are required. They complement each other.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Manual verification forces the implementer to observe the actual behavior of the system, not just trust that tests passed. This deliberate observation step catches integration issues, visual regressions, and behavioral mismatches that automated tests may not cover.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Bugs that reach production often stem from skipping manual verification. The root cause is not inadequate tests -- it is the absence of a human or agent observing the actual behavior before declaring the work complete. This convention addresses that root cause directly.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: The verification step is an explicit, required action in the implementation workflow. It is not assumed to have happened because tests passed. The evidence of verification (screenshots, console output, API responses) makes the check visible and auditable.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Three-Level Testing Standard](./three-level-testing-standard.md)**: Manual verification supplements the three automated testing levels (unit, integration, E2E). It does not replace any of them. All three levels plus manual verification form the complete quality assurance picture.

- **[Code Quality Convention](./code.md)**: Automated quality gates (typecheck, lint, test:quick) catch code-level issues. Manual verification catches behavioral issues that survive those gates. Together they form a complete quality boundary.

- **[Evidence Capture Convention](./evidence-capture.md)**: Manual verification must leave a committed record — screenshots in the plan's `evidence/` subfolder, curl outputs inline in `delivery.md`. "Verified manually" without a record is incomplete.

## The Rule

**Manual behavioral verification is MANDATORY after implementing UI or API changes.**

This applies to:

- New UI features (pages, components, interactions)
- UI bug fixes
- New API endpoints
- API behavior changes (request/response shape, validation rules, error handling)
- Integration changes (connecting UI to API, connecting API to data source)

## UI Verification

Use Playwright MCP tools to verify UI features and bugs in a real browser environment.

### Required Tools

| Tool                       | Purpose                                                |
| -------------------------- | ------------------------------------------------------ |
| `browser_navigate`         | Open the relevant page                                 |
| `browser_snapshot`         | Capture the current DOM state for inspection           |
| `browser_click`            | Interact with buttons, links, and interactive elements |
| `browser_fill_form`        | Fill form fields to test input handling                |
| `browser_console_messages` | Check for JavaScript errors, warnings, and logs        |
| `browser_take_screenshot`  | Capture visual evidence of the rendered state          |
| `browser_network_requests` | Verify API calls, response codes, and payload shapes   |

### UI Verification Checklist

After implementing a UI change, verify:

1. **Page renders**: Navigate to the page and take a snapshot. Confirm the expected elements are present.
2. **Interactions work**: Click buttons, fill forms, and navigate between pages. Confirm the expected behavior occurs.
3. **No console errors**: Check `browser_console_messages` for JavaScript errors or unexpected warnings.
4. **Network requests succeed**: Check `browser_network_requests` for failed API calls, unexpected 4xx/5xx responses, or missing requests.
5. **Visual correctness**: Take a screenshot and confirm the layout, typography, and content match expectations.
6. **All locales verified**: For multi-locale apps, repeat steps 1–5 for EVERY supported locale — navigate to each locale-prefixed URL (e.g., `/en/`, `/id/`). A UI change verified only in the default locale is incomplete. Confirm the `html[lang]` attribute matches each locale and that no strings are untranslated.
7. **All breakpoints verified**: Repeat at mobile (375 px), tablet (768 px), and desktop (1280 px). Responsive behavior at one viewport does not imply correct behavior at others.
   - **Presence is not legibility**: confirming an element is present at a breakpoint (via `browser_snapshot` or a DOM query) does not confirm it is legible. Read a computed style (e.g., font-size) or a bounding box for representative text elements at each breakpoint — an element can exist in the DOM while rendering too small to read, and a screenshot scaled into a review pane can hide a factor-of-two type-size error.
8. **Evidence captured**: Save one screenshot per breakpoint per locale to the plan's `evidence/` subfolder; reference each from the `delivery.md` implementation notes. See [Evidence Capture Convention](./evidence-capture.md).

### Example: UI Feature Verification (multi-locale app)

```
For each locale in ["en", "id"]:
  For each breakpoint in [375, 768, 1280]:
    1. browser_resize(breakpoint, 900)
    2. browser_navigate("http://localhost:3200/{locale}/products")
    3. browser_snapshot() -- confirm product list renders with correct language
    4. browser_take_screenshot() -- save to evidence/phase-N-products-{locale}-{breakpoint}px.png
    5. browser_console_messages() -- confirm no errors
    6. browser_network_requests() -- confirm API calls succeed

After all locales/breakpoints:
  7. browser_click("Add Product button")
  8. browser_fill_form("Product Name", "Test Product")
  9. browser_click("Submit button")
  10. browser_snapshot() -- confirm product appears in list
  11. browser_network_requests() -- confirm POST /api/products returned 201

Record inline in delivery.md: screenshot paths, console status, network status per locale.
```

## API Verification

Use `curl` via Bash to verify API endpoints respond correctly.

### API Verification Checklist

After implementing an API change, verify:

1. **Health check**: Confirm the server is running and responding.
2. **Happy path**: Send a valid request and confirm the expected response shape, status code, and data.
3. **Error cases**: Send invalid requests and confirm proper error responses (4xx status codes, error messages).
4. **Edge cases**: Test boundary conditions (empty payloads, missing fields, maximum lengths).

### Example: API Endpoint Verification

```bash
# Health check
curl -s http://localhost:8202/health | jq .

# Happy path -- create a resource
curl -s -X POST http://localhost:8202/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 9.99}' | jq .

# Verify the response status code
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8202/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 9.99}'

# Error case -- missing required field
curl -s -X POST http://localhost:8202/api/products \
  -H "Content-Type: application/json" \
  -d '{"price": 9.99}' | jq .

# Error case -- invalid data type
curl -s -X POST http://localhost:8202/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "price": "not-a-number"}' | jq .
```

Record the command, response body, and HTTP status code inline in `delivery.md` under the
implementation notes for the step. If the response is long (> 20 lines), save it to
`evidence/phase-N-<endpoint-slug>.txt` and reference it by path.

### Locale-Aware API Verification

For APIs that serve locale-specific responses (e.g., localized error messages, locale-dependent
formatting), verify each supported locale explicitly:

```bash
# Verify locale-specific response (Accept-Language header or query param)
curl -s -H "Accept-Language: en" http://localhost:8202/api/products | jq .name
curl -s -H "Accept-Language: id" http://localhost:8202/api/products | jq .name
```

## When Verification Is Required

| Change Type                                 | UI Verification              | API Verification                       |
| ------------------------------------------- | ---------------------------- | -------------------------------------- |
| New UI page or component                    | Yes                          | No (unless it calls an API)            |
| UI bug fix                                  | Yes                          | No (unless the bug involved API calls) |
| New API endpoint                            | No (unless a UI consumes it) | Yes                                    |
| API behavior change                         | No (unless a UI consumes it) | Yes                                    |
| Full-stack feature (UI + API)               | Yes                          | Yes                                    |
| Styling-only change                         | Yes (visual check)           | No                                     |
| Internal refactor with no behavioral change | No                           | No                                     |
| Documentation-only change                   | No                           | No                                     |

## Relationship to Automated Tests

Manual verification does **not** replace automated tests. The relationship is complementary:

| Layer                   | What It Catches                                                            | When It Runs                                |
| ----------------------- | -------------------------------------------------------------------------- | ------------------------------------------- |
| **Unit tests**          | Logic errors, edge cases, contract violations                              | On every commit (test:quick)                |
| **Integration tests**   | Cross-component failures, database issues                                  | On demand or CI                             |
| **E2E tests**           | Full-stack flow failures, regression                                       | On demand or CI                             |
| **Manual verification** | Visual regressions, UX issues, integration mismatches, real-world behavior | After implementation, before declaring done |

A feature is not complete until **both** automated tests pass **and** manual verification confirms the expected behavior.

## Examples

### PASS: Complete verification workflow

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

### FAIL: Skipping manual verification

```
1. Implement the feature
2. Write automated tests
3. Run test:quick -- all pass
4. Declare the feature complete
   [No manual verification -- visual regression ships to production]
```

### FAIL: Manual verification without automated tests

```
1. Implement the feature
2. Manually check it works in the browser
3. Declare the feature complete
   [No automated tests -- regression introduced in next commit]
```

## Scope

This convention applies to:

- All AI agents implementing UI or API changes
- All human developers implementing UI or API changes
- All apps in `apps/` that have a UI or API surface

It does not apply to:

- Library-only changes (`libs/`) with no UI or API surface
- Documentation changes (`docs/`, `repo-governance/`, `plans/`)
- Configuration changes that do not affect runtime behavior
- Internal refactors with no observable behavioral change

## Tools and Automation

- **Playwright MCP tools**: Available to all agents for browser-based verification
- **curl**: Available via Bash for API verification
- **jq**: Available via Bash for JSON response inspection

## Related Documentation

- [Three-Level Testing Standard](./three-level-testing-standard.md) -- Automated testing architecture that manual verification complements
- [Code Quality Convention](./code.md) -- Automated quality gates (typecheck, lint, test:quick)
- [Implementation Workflow Convention](../workflow/implementation.md) -- Three-stage workflow where manual verification fits in the "make it work" stage
- [Specs-Application Sync Convention](./specs-application-sync.md) -- Spec updates required alongside code changes
- [User-Facing Delivery Hardening Convention](./user-facing-delivery-hardening.md) -- Extends this convention to a per-breakpoint, per-locale visual sign-off against the design mockups **before archival**, plus fifteen sibling rules for user-facing delivery
- [Evidence Capture Convention](./evidence-capture.md) -- Where and how to store verification evidence: screenshots in `evidence/`, curl outputs inline in `delivery.md`, locale and breakpoint coverage requirements
