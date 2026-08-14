# How to Drive the Browser and Suggesting New Behaviour for the Specs

## How to Drive the Browser

Before browser-facing verification, discover the real-browser integrations installed on the machine
and confirm which are healthy and callable in the current harness. Prefer Chrome/Chromium through
Chrome DevTools MCP or Playwright MCP; if neither is available, use an equivalent installed
browser-driving tool. Record the selected tool, any fallback, browser/version when available, and
capability gaps in the verification evidence. Static source, fetched HTML, WebFetch, and curl
inspection are useful baselines, but do not count as live-browser verification when a working browser
integration exists.

1. **Baseline** — `WebFetch` the target(s) for rendered text, headings, nav labels, and link
   discovery; `Bash curl -sS -D - -o /dev/null` to read the redirect/locale-prefix/trailing-slash
   structure that feeds the URL-naturalness pass.
2. **Interactive walkthrough & responsive passes** — write a Playwright script to `local-temp/` and
   run it via `npx playwright` to navigate each task step, click, fill benign data, resize to each
   breakpoint, capture screenshots, read console/network for surprising behaviour, and time perceived
   latency on key interactions (flag > ~400 ms without a progress indicator). Iterate the walkthrough
   over EVERY supported locale × EVERY breakpoint, and save cited screenshots to the backlog plan's
   `evidence/` subfolder (per the
   [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md)),
   not `local-temp/`. Treat tooling absence gracefully — fall back to the baseline and record the
   limitation under "areas not covered".
3. **External-consistency research** — when judging whether a widget matches the universal
   convention, `WebSearch` or delegate to `web-researcher`; cite the convention, not this product's
   intent.
4. **Never read the answer key** — do not open `specs/**`, source, or mockups to decide whether
   something is "correct". The question is comprehension, and the only valid judge is principle +
   convention + internal consistency.

## Suggesting New Behaviour for the Specs (spec-blind)

The agent does **not** read `specs/**`, so it cannot tell what the specs already cover. It can still
contribute spec value from the usability side: whenever the cognitive walkthrough or heuristic sweep
shows that a first-time user would reasonably **expect a behaviour the page does not provide**, the
agent captures that desired behaviour as a Gherkin scenario — a _suggestion_, not a gap verdict.

Propose a suggestion only when the missing behaviour is:

- **Grounded in a usability principle** — tie it to the same heuristic / walkthrough question / UX
  law / WCAG 3.x criterion the related finding cites (e.g. Heuristic 1 → a visible loading state or
  an explicit empty/zero-result message; Heuristics 5 & 9 → a confirmation before a destructive
  action).
- **Expressible as Given/When/Then** — concrete enough to become a scenario.
- **In the target's responsibility** — owned by this app/lib, not a third-party widget or the
  browser.

Each suggestion carries an ID (`USS-001`, …), the desired behaviour, the violated principle and the
`UWT-###` finding it pairs with, the proposed Gherkin scenario (use the
`plan-writing-gherkin-criteria` Skill), and a **spec-blind caveat**: "this agent did not read
`specs/**`; a spec-aware reviewer must confirm this behaviour is not already covered before adding
it." These land in `spec-suggestions.md`.

They are **desired-behaviour proposals from usability principles**, deliberately distinct from
`web-exploratory-tester`'s `spec-gaps.md`, which proposes scenarios for **already-observed correct
behaviour** after de-duplicating against the existing specs. The two never overlap by construction:
one suggests what _ought_ to exist for clarity (blind), the other documents what _does_ exist but is
unprotected (spec-aware). If the run surfaced no suggestions, omit the file and say so in
`README.md`.
