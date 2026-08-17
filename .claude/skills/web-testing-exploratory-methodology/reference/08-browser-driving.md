# How to Drive the Browser

Before browser-facing verification, discover the real-browser integrations installed on the machine
and confirm which are healthy and callable in the current harness. Prefer Chrome/Chromium through
Chrome DevTools MCP or Playwright MCP; if neither is available, use an equivalent installed
browser-driving tool. Record the selected tool, any fallback, browser/version when available, and
capability gaps in the verification evidence. Static source, fetched HTML, WebFetch, and curl
inspection are useful baselines, but do not count as live-browser verification when a working browser
integration exists.

1. **Baseline (always available)** — `WebFetch` the target(s) for rendered HTML, meta, and link
   discovery; `Bash curl -sS -D - -o /dev/null` for headers/redirects/TLS/status; `curl` each
   discovered link for status codes; fetch `robots.txt`/`sitemap.xml`.
2. **Interactive / visual / responsive (when the goal needs it)** — write a Playwright script to
   `local-tmp/` and run it via `npx playwright` to navigate, click, fill, resize to each breakpoint,
   capture screenshots (compare to mockups), read console errors, and capture network failures.
   Iterate the navigate/screenshot pass over EVERY supported locale × EVERY breakpoint. Save
   screenshots that a finding cites to the backlog plan's `evidence/` subfolder (named
   `phase-N-<description>-<locale>-<breakpoint>px.png` per the
   [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md)),
   not `local-tmp/` — they become committed proof a developer can inspect. Run
   `npx lighthouse <url> --output=json` for Core Web Vitals where available (save reports to
   `evidence/`). Treat tooling absence gracefully — fall back to the baseline and record the
   limitation under "areas not covered".
3. **Ground-truth comparison** — `Read`/`Glob`/`Grep` the plan `assets/`, `specs/**`, source, and
   i18n files to decide whether observed behaviour is a defect (diverges from intent) or expected.
4. **Value correctness** — for any computed output, independently recompute or cross-check against
   the spec; assert the _value_, not just its presence (Rule 5/12 of User-Facing Delivery Hardening).
