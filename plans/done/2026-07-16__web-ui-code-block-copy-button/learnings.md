# Learnings — web-ui Code-Block Copy Button

> Transient running log the executor appends to during delivery: one entry per generalizable learning,
> sanitized per the secret/sensitivity gate BEFORE it is ever written. Triaged to a durable home (or an
> explicit discard) in the Knowledge Capture phase before archival. If nothing generalizable surfaced,
> record the explicit `No generalizable learnings — <reason>` escape rather than leaving this empty.

## Entry template

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — see the secret/sensitivity gate)
- **Why it might generalize**: the litmus reasoning
- **Routing (filled at Knowledge Capture)**: <durable home | backlog plan slug | discarded: reason>
```

## Candidate watch-items — triaged at Knowledge Capture (2026-07-16)

- **`getTextContent` newline verbatim**: did not materialise as a generalizable learning. Copy is
  driven from the source `code` string (not re-extracted from highlighted HTML), and verbatim fidelity
  is proven by the e2e byte-equal assertion. **Discarded** — settled by the shipped design + tests;
  `tech-docs.md` already records it. No durable surface would be improved.
- **Promote the `role=status aria-live=polite` sr-only pattern to a shared web-ui helper**:
  **Discarded** — single consumer (`CopyButton`); a shared live-region helper would be a premature
  abstraction (YAGNI). Re-open when a second consumer needs the same pattern.
- **jsdom `navigator.clipboard` stubbing friction**: **Discarded** — no material friction materialised;
  the existing stub approach worked across all unit + retest passes. Nothing to codify.

## Entries

### Learning: rhino `speccoverage` scenario-title scan is per-physical-line

- **Context**: Rule-15 fix pass; `specs:behavior:coverage` reported a spurious "scenario gap" for a
  fully-bound vitest-cucumber scenario.
- **Observation**: `extract_ts_scenario_titles` scans `for line in content.lines()` and matches
  `Scenario\s*\(\s*"..."\s*,` per line. Prettier (`printWidth: 120`) wraps a long
  `Scenario("long title", (cb) => {` onto two lines, so the title is no longer on the `Scenario(` line
  and is never extracted. Worked around here with `// prettier-ignore` + a single-line `Scenario("title",`.
- **Why it might generalize**: any author writing a long scenario title hits this; the `// prettier-ignore`
  workaround is fragile (depends on every author remembering it). A multi-line-aware scanner is a durable
  surface that catches it automatically.
- **Secret/sensitivity gate**: no secrets — file paths + a regex only.
- **Repo-relevance gate**: `apps/rhino-cli` is public; routable in-repo.
- **Routing**: **Filed as backlog plan** `plans/backlog/2026-07-16__rhino-speccoverage-multiline-scenario-scan/`
  (code home → backlog per the code-routing rule; NEVER inline in this PR).

### Learning: `tailwind-merge` collapses stacked `transition-*` utilities

- **Context**: DWT-002 — the copy button's colour transition silently stopped animating.
- **Observation**: `tailwind-merge` treats all `transition-*` utilities as one property group (last wins),
  so `transition-opacity` from the wrapper className overrode `transition-colors` on the button, dropping
  the colour animation. Fixed by passing the single `transition` utility (animates colour + bg + opacity).
- **Secret/sensitivity gate**: no secrets.
- **Repo-relevance gate**: public web-ui concern.
- **Routing**: **Discarded** — now fixed in code and guarded by the regenerated visual baseline; the
  behaviour is documented upstream by `tailwind-merge`. No repo doc/lint surface would auto-catch it
  short of a custom rule not worth a plan. Recorded here for the audit trail only.

### Learning: rehype-pretty-code `keepBackground` inline var shadows the CSS fallback

- **Context**: DWT-001 — live light-theme code background rendered `#fff` instead of `#f6f8fa`.
- **Observation**: `keepBackground: true` with the github-light theme writes an inline
  `--shiki-light-bg:#fff` on `pre`, which shadows the CSS `var(--shiki-light-bg, #f6f8fa)` fallback.
  Fixed by hard-setting `background-color: #f6f8fa !important` (light only) in both apps' `globals.css`.
- **Secret/sensitivity gate**: no secrets.
- **Repo-relevance gate**: public app concern.
- **Routing**: **Discarded** — app-specific, now fixed in both `globals.css` and guarded by the DWT-001
  fix. Localised; no cross-repo generalization. Recorded for the audit trail only.

### Learning: Nx TS coverage projects flake under parallel load / dev-server contention

- **Context**: pre-push affected gates + `run-many` showed transient `test:coverage` failures.
- **Observation**: heavy TS coverage projects (ayokoding-www, wahidyankf-www) starve and flake when many
  projects run concurrently OR a background dev server competes for resources; they pass 0-fail in
  isolation. Mitigate by warming caches / killing the dev server, then re-running isolated.
- **Secret/sensitivity gate**: no secrets.
- **Repo-relevance gate**: CI-runner / local-ops behaviour, not public-governance content — no in-repo
  propagation.
- **Routing**: **Already captured in operator memory** (`feedback_nx_flaky_warm_cache_commit`); terminal,
  no new home needed.
