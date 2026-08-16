# How to Drive the Browser, and Locale + Evidence Awareness

## How to Drive the Browser

Before browser-facing verification, discover the real-browser integrations installed on the machine
and confirm which are healthy and callable in the current harness. Prefer Chrome/Chromium through
Chrome DevTools MCP or Playwright MCP; if neither is available, use an equivalent installed
browser-driving tool. Record the selected tool, any fallback, browser/version when available, and
capability gaps in the verification evidence. Static source, fetched HTML, WebFetch, and curl
inspection are useful baselines, but do not count as live-browser verification when a working browser
integration exists.

1. **Baseline** — `WebFetch` the target(s) for rendered HTML/CSS and link discovery; identify the
   routes and the locale-prefix structure.
2. **Render, measure, screenshot (per breakpoint × per locale)** — write a Playwright script to
   `local-tmp/` and run it via `npx playwright` to navigate each route, resize to each breakpoint,
   read **computed styles** for the elements under test (colour, spacing, font, radius, shadow), and
   capture screenshots. Iterate the render/measure/screenshot pass over EVERY supported locale × EVERY
   breakpoint (375 / 768 / 1280, plus 320/1440 when `thorough`). Save cited screenshots to the backlog
   plan's `evidence/` subfolder (named `phase-N-<description>-<locale>-<breakpoint>px.png` per the
   [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md)),
   not `local-tmp/` — they become committed proof. Treat tooling absence gracefully — fall back to
   `WebFetch` static inspection and record the limitation under "areas not covered".
3. **Ground-truth comparison** — `Read`/`Glob`/`Grep` the plan `assets/` mockups, the design tokens/
   theme, and the `libs/web-ui` primitive library to decide whether an observation diverges from the
   design (a finding) or matches it. `WebFetch` the external design source when one was provided.
4. **Design-practice grounding** — for any principle whose exact statement is in doubt, delegate to
   `web-researcher`; cite the principle in the finding rather than asserting a preference.

## Locale + Evidence Awareness (Mandatory)

- Test **ALL supported locales** (discover from the app's i18n config —
  `apps/<target>/src/features/i18n/` or `next.config.ts`), per breakpoint **375 / 768 / 1280 px**
  (plus 320/1440 when `thorough`). Verify `html[lang]` matches the locale under test.
- Capture cited screenshots into the plan's committed `evidence/` subfolder, named
  `phase-N-<description>-<locale>-<breakpoint>px.png`, per the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
- Use **Playwright MCP** for rendering/screenshots; **`web-researcher`** for design-practice grounding.
