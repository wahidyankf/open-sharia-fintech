# How to Drive the Browser, and Specs as Ground Truth & Spec-Gap Detection

## How to Drive the Browser

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
   `local-temp/` and run it via `npx playwright` to navigate, click, fill, resize to each breakpoint,
   capture screenshots (compare to mockups), read console errors, and capture network failures.
   Iterate the navigate/screenshot pass over EVERY supported locale × EVERY breakpoint. Save
   screenshots that a finding cites to the backlog plan's `evidence/` subfolder (named
   `phase-N-<description>-<locale>-<breakpoint>px.png` per the
   [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md)),
   not `local-temp/` — they become committed proof a developer can inspect. Run
   `npx lighthouse <url> --output=json` for Core Web Vitals where available (save reports to
   `evidence/`). Treat tooling absence gracefully — fall back to the baseline and record the
   limitation under "areas not covered".
3. **Ground-truth comparison** — `Read`/`Glob`/`Grep` the plan `assets/`, `specs/**`, source, and
   i18n files to decide whether observed behaviour is a defect (diverges from intent) or expected.
4. **Value correctness** — for any computed output, independently recompute or cross-check against
   the spec; assert the _value_, not just its presence (Rule 5/12 of User-Facing Delivery Hardening).

## Specs as Ground Truth & Spec-Gap Detection

The repo's `specs/**` tree is the executable record of intended behaviour (`specs/apps/**` for apps,
`specs/libs/**` for libraries). Treat it as a first-class ground truth alongside the design mockups —
and treat the live site as evidence about what the specs _should_ say.

### Compare live behaviour against existing specs

1. **Locate the relevant features** — `Glob`/`Grep` `specs/apps/<target>/**` (and `specs/libs/**`
   when the target consumes a shared lib) for `.feature` files whose scenarios map to the URL(s) and
   flows under test.
2. **Exercise each mapped scenario on the live target** — walk its Given/When/Then against the
   running site and sort every scenario into one of three buckets:
   - **Covered + passing** — live behaviour matches the scenario; record it in the `README.md`
     coverage map.
   - **Covered + diverging** — live behaviour contradicts the scenario; this is a **defect**. File it
     in `findings.md` with the **Expected Result citing the scenario** by
     `path/to.feature › Scenario name`.
   - **Uncovered** — feeds gap detection below.
3. **Cite the spec, not an assumption** — when a Gherkin scenario exists, the finding's "expected"
   MUST quote it; the spec outranks the agent's guess about correct behaviour.

### Detect behaviours that should be added to the specs

While touring the URL(s) / location, the agent continually observes behaviours that the existing
`specs/**` do **not** describe. Each is a candidate **spec gap** — a scenario the specs ought to
carry so the behaviour is protected by the
[Specs & Gherkin Completeness rule](../../../../repo-governance/development/quality/feature-change-completeness.md).
**Edge-case behaviours are the richest source of gaps**: boundary handling, empty/zero-result states,
error recovery, and input-validation rules are frequently correct in the running app yet absent from
the spec. When an edge behaviour observed under the dimensions checklist is correct and intended,
propose it as a Gherkin scenario here rather than letting it stay unprotected.

Propose a gap only when the observed behaviour is:

- **Intended / correct** — not itself a defect. Defects go to `findings.md`, never `spec-gaps.md`. If
  unsure whether it is intended, record it as an open question rather than a confident proposal.
- **Reproducible** — deterministic enough to express as Given/When/Then.
- **In the target's responsibility** — owned by this app/lib, not a third-party widget or the
  browser.

For each gap, draft a Gherkin scenario (use the `plan-writing-gherkin-criteria` Skill) and name the
target `specs/**` file — an existing `.feature` to extend or a new one to add. Every gap is a
**proposal for maintainer confirmation**: the agent asserts "this behaviour exists and is
unprotected", not "the spec is wrong". These land in `spec-gaps.md`.
