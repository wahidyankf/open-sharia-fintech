# How to Drive the Browser

Before browser-facing verification, discover the real-browser integrations installed on the machine
and confirm which are healthy and callable in the current harness. Prefer Playwright MCP; if it is
unavailable, use Chrome DevTools MCP; if neither is available, use an equivalent installed
browser-driving tool. Record the selected tool, any fallback, browser/version when available, and
capability gaps in the verification evidence. Static source, fetched HTML, WebFetch, and curl
inspection are useful baselines, but do not count as live-browser verification when a working browser
integration exists.

1. **Baseline** — `WebFetch` the target(s) for rendered text, headings, nav labels, and link
   discovery; `Bash curl -sS -D - -o /dev/null` to read the redirect/locale-prefix/trailing-slash
   structure that feeds the URL-naturalness pass.
2. **Interactive walkthrough & responsive passes** — write a Playwright script to `local-tmp/` and
   run it via `npx playwright` to navigate each task step, click, fill benign data, resize to each
   breakpoint, capture screenshots, read console/network for surprising behaviour, and time perceived
   latency on key interactions (flag > ~400 ms without a progress indicator). Iterate the walkthrough
   over EVERY supported locale × EVERY breakpoint, and save cited screenshots to the backlog plan's
   `evidence/` subfolder (per the
   [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md)),
   not `local-tmp/`. Treat tooling absence gracefully — fall back to the baseline and record the
   limitation under "areas not covered".
3. **External-consistency research** — when judging whether a widget matches the universal
   convention, `WebSearch` or delegate to `web-researcher`; cite the convention, not this product's
   intent.
4. **Never read the answer key** — do not open `specs/**`, source, or mockups to decide whether
   something is "correct". The question is comprehension, and the only valid judge is principle +
   convention + internal consistency.
