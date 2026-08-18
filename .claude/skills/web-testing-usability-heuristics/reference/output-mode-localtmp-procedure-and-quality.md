# Output Mode `local-tmp`, Procedure Summary, and Quality Guidelines

## Mode `local-tmp` — a throwaway findings file for direct fixing

Write a single `local-tmp/<YYYY-MM-DD>__<slug>/findings.md` carrying the full finding catalog plus
an `evidence/` subfolder beside it. Emit **no**
`README`/`brd`/`prd`/`walkthrough`/`spec-suggestions`/`tech-docs`/`delivery`, and make **no** entry
in `plans/backlog/README.md`. The folder is gitignored and ephemeral. Return the same severity-count
summary plus the `local-tmp/` path to the orchestrator.

## Procedure Summary

1. Confirm URL(s) + usability goal; resolve persona, tasks, depth, breakpoints, locales. Do not
   request specs/mockups.
2. Establish the baseline (WebFetch + curl): rendered content, nav labels, link graph, URL/locale
   structure.
3. Run the heuristic-evaluation sweep against all 10 heuristics across the page and sibling
   surfaces.
4. Run cognitive walkthroughs for each task at each breakpoint/locale, answering the four questions
   per step; capture transcripts.
5. Run the first-click / information-scent and URL-naturalness passes.
6. Judge responsive usability at mobile/tablet/desktop across EVERY supported locale; screenshot
   each. Probe the edge & boundary UX states — surface at least one or record that none were found.
7. Run the four **Mandatory Systematic Probes** (enumerate, never sample); record each in the
   coverage map.
8. For external-consistency calls, check the convention via `web-researcher`/`WebSearch` — never the
   product's specs.
9. Triage findings with Nielsen 0-4 severity + proposed priority, each citing its violated
   principle; de-duplicate. Draft any `USS-###` spec suggestions.
10. Write the backlog plan (README, brd, prd, findings, walkthrough, and spec-suggestions when any
    surfaced) with steps-to-reproduce and Gherkin ACs for the clarified behaviour.
11. Return a concise summary to the orchestrator: counts by severity, the spec-suggestion count, the
    top friction, the plan path, and what was _not_ covered.

## Quality Guidelines

- **Cite the principle, never a vibe** — every finding names the heuristic / walkthrough question /
  UX law / ISO / WCAG criterion it violates. No principle, no finding.
- **Stay blind** — if you catch yourself wanting to open a spec or the source to decide whether
  something is "right", stop.
- **Reproduce before you report** — a friction claim without deterministic steps (and the
  breakpoint/locale) is an opinion, not a finding.
- **See past the polish** — the Aesthetic-Usability Effect makes pretty pages feel usable; walk the
  task anyway.
- **Record non-coverage honestly** — list dimensions, breakpoints, locales, or tasks not exercised
  and why; silent gaps read as "all clear" when they are not.
- **Stay non-destructive** — when unsure an action is safe, don't; record it as a flow not exercised.
