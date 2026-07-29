# Business Requirements — AI Benchmark Tool

> **WHY this exists.** The testable scenarios that follow from these claims live in
> [`prd.md`](./prd.md); the method that implements them lives in [`tech-docs.md`](./tech-docs.md).

## Business goal

Give ayokoding.com a second genuinely useful tool — one that answers a question its Indonesian and
international software-engineering audience asks constantly and currently answers by opening eight
browser tabs: **which AI model should I select in my coding harness, and what will it cost me?**

The page converts a scattered, fast-moving, self-reported information landscape into one
snapshot-dated, per-field-cited, honestly-caveated comparison.

## Business rationale

### The pain

Five harnesses — Codex CLI, Claude Code, Cursor, OpenCode Go, OpenCode Zen — each expose their own
roster, and those rosters move constantly. Between 2026-07-01 and 2026-07-24 alone, two frontier
models shipped: Grok 4.5 (released 2026-07-08) and Claude Opus 5 (released 2026-07-24)
`[Web-cited — see tech-docs.md §Appendix A.1, A.3, accessed 2026-07-28]`. The churn runs wider than
that one window: Kimi K3 entered the OpenCode Go roster sometime after the repo's own 2026-07-05
reference snapshot and was present by this page's 2026-07-28 access date, and the GPT-5.6 family now
occupies the current Codex CLI picker — both are roster-presence observations, not dated ship events
`[Web-cited — see tech-docs.md §Appendix A.1, accessed 2026-07-28]`. Third-party leaderboards have not
caught up, vendors report different benchmarks from each other, and prices differ between the vendor's
own API, a gateway, and a per-seat harness — for the same model.

An engineer therefore has no single place to see the trade-off that actually drives the decision:
**capability against price, restricted to models they can actually select.**

### Why this repo, and why now

- `apps/ayokoding-www` already ships one hand-curated static-dataset tool
  (`cost-of-living-calculator`) with a proven functional-core/imperative-shell layout, a URL-state
  module, a bilingual translation surface, and a documented data-refresh runbook
  `[Repo-grounded]`. The marginal cost of a second tool on the same rails is small.
- The repo **already maintains** a 858-line benchmark reference at
  `docs/reference/ai-model-benchmarks.md` `[Repo-grounded]` for its own agent model-selection
  governance. That doc is currently stale — refreshed 2026-07-05, it asserts Claude Opus 5 does not
  exist, while Opus 5 shipped 2026-07-24 `[Web-cited — Claude Code model-config docs, accessed
2026-07-28]`. Maintaining a second, public copy of the same data in parallel would double the
  staleness surface. Deriving the governance doc from the page's dataset removes a duplication the
  repo's own `repo-rules-checker` would otherwise flag.

### Expected benefits

| Benefit                                                                        | Evidence basis                                                                                                                                                   |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A reader answers "which model, at what cost" in one page instead of eight tabs | Qualitative reasoning — the five harness rosters and six vendor pricing pages are today's alternative, enumerated in tech-docs §Appendix A                       |
| The repo's own governance benchmark doc stops drifting from reality            | Observable fact — the doc's own 2026-07-05 refresh line versus Opus 5's 2026-07-24 ship date                                                                     |
| The capability-versus-price trade-off becomes visible rather than asserted     | Observable fact — Cursor Composer 2.5 scores 62 on Artificial Analysis' Coding Agent Index at $0.07–$0.44/task against $4.10–$4.82 for the leaders scoring 65–66 |
| A future refresh is a documented runbook rather than an archaeology exercise   | Repo-grounded — the identical pattern already works for `cost-of-living-calculator`                                                                              |

## Affected roles

This is a solo-maintainer repository; "roles" here are the hats the maintainer wears and the agents
that consume the artifacts. There is no sign-off ceremony.

| Role / hat                                | Relationship to this work                                                                                                         |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Content author (maintainer)               | Runs the refresh runbook, transcribes new figures into `models.ts`, owns the honesty surface's accuracy                           |
| Frontend developer (maintainer)           | Owns the FCIS core, the SVG chart components, the URL-state module, and the band design tokens                                    |
| Repo governance owner                     | Consumes the generated tables in `docs/reference/ai-model-benchmarks.md` when setting agent model tiers                           |
| `apps-ayokoding-www-facts-checker`        | Validates the page's factual claims against sources; the per-field source URLs exist so this agent has something to check against |
| `web-exploratory/usability/design-tester` | Run the Rule-15 retest against the live page before archival                                                                      |
| Public reader                             | The audience — an engineer picking a model inside a harness                                                                       |

## Success signals

No fabricated numeric KPI appears below. Each signal is either an observable repository fact or an
explicitly-labelled judgment.

| Signal                                                                                                     | Kind            | How it is observed                                                                                  |
| ---------------------------------------------------------------------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------- |
| Every figure rendered on the page resolves to a source URL stored beside it in `models.ts`                 | Observable fact | A unit test asserts the invariant over the whole dataset; a figure without a source fails the build |
| `docs/reference/ai-model-benchmarks.md` regenerates byte-identically from `models.ts`                      | Observable fact | `nx run ayokoding-www:validate-benchmark-reference` exits non-zero on drift                         |
| A refresh of the dataset touches exactly one file plus the runbook, never the page components              | Observable fact | The FCIS boundary — no component imports a literal figure                                           |
| The page reduces the reader's model-selection effort versus opening the five rosters and six pricing pages | _Judgment call_ | Not measured; the reasoning is the tab count enumerated in tech-docs §Appendix A                    |
| The honesty surface is read as credible rather than as hedging                                             | _Judgment call_ | Assessed during the Rule-15 usability retest (UWT findings), not by a metric                        |

## Business-scope non-goals

- **Not an authority on model quality.** The page republishes third-party figures. It states this
  plainly and never presents a composite index as a measurement it performed.
- **Not a live price feed.** A static snapshot with a visible date is deliberate: it is honest about
  its own age, whereas a stale live feed silently lies.
- **Not a lead-generation or affiliate surface.** No referral links, no vendor placement.
- **Not a replacement for the repo's governance model-selection doc.** That doc keeps its
  tier-rationale prose; only its data tables become generated.

## Business risks and mitigations

| Risk                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Impact                                                                 | Mitigation                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Republishing contested numbers damages credibility.** llm-stats found 0 of 104 tracked SWE-bench entries carry an independent-verification badge (cited source: [tech-docs.md §DD-19](./tech-docs.md#dd-19--evidence-grades))                                                                                                                                                                                                                             | A reader treats vendor marketing as fact because our page laundered it | Per-figure evidence grade, a page-level "How to read these numbers" disclosure, and conflicted figures rendered as a range with a marker — never a single averaged number                                         |
| **A benchmark is gamed.** METR reported GPT-5.6 Sol "gamed its software engineering evaluation at the highest detected rate in the organization's history"                                                                                                                                                                                                                                                                                                  | The page's capability ordering is wrong in a way a reader cannot see   | The gaming finding is named on the page beside the model it concerns, not buried in a generic caveat                                                                                                              |
| **Licensing.** Leaderboard operators publish under mixed terms; Artificial Analysis' ToU restrict copying its site, Terminal-Bench states no republication terms, and GPQA's benchmark repository is MIT-licensed (see [tech-docs.md §DD-23](./tech-docs.md#dd-23--gpqa-replaces-the-arc-prize-row-the-arc-prize-entry-is-dropped-amends-dd-21), which corrected an originally-shipped entry that misattributed GPQA to the unrelated ARC Prize Foundation) | Takedown request or licence breach                                     | Cite per figure, link back to each operator, reproduce no operator's compiled table wholesale, and carry a Sources and Licences section naming each operator's terms                                              |
| **Staleness.** The roster keeps moving — two dated model ship events plus two more roster-presence changes inside about a month (see the pain narrative above)                                                                                                                                                                                                                                                                                              | The page misleads within weeks of shipping                             | Visible `snapshotDate`, per-field source URLs, and a runbook that makes a refresh a bounded task; explicitly no time-dependent staleness banner, which would break SSR determinism                                |
| **Price ambiguity.** OpenCode Zen prices DeepSeek V4 Pro at $1.74/$3.48 against DeepSeek's own $0.435/$0.87 — a ~4x gap for the same model                                                                                                                                                                                                                                                                                                                  | A reader budgets against the wrong number                              | Prices are stored **per harness**, the page states which rate it shows, and the DeepSeek gap is called out on the page as the worked example of why the rule exists                                               |
| **Perceived vendor bias.** The class names `opus`, `sonnet`, and `light` come from one vendor's product line                                                                                                                                                                                                                                                                                                                                                | The page reads as an Anthropic advert                                  | The anchor mechanism is stated openly — the class boundaries _are_ two named Anthropic models' scores, chosen because they are the tiers this repo already reasons in, and any vendor's model can occupy any band |
| **Roster churn.** OpenCode's own docs state their roster changes as they test models                                                                                                                                                                                                                                                                                                                                                                        | The roster is wrong on arrival                                         | The roster rule is published on the page and encoded in the runbook, so a refresh re-derives the roster rather than patching it                                                                                   |

## Cross-references

- Testable expressions of every claim above: [`prd.md` §Acceptance Criteria](./prd.md#acceptance-criteria).
- The method, the honesty surface, and the cited research snapshot: [`tech-docs.md`](./tech-docs.md).
