# Business Requirements — ayokoding-www Cost Reduction

> **WHY this exists.** Testable scenarios that follow from these claims live in
> [`prd.md`](./prd.md); the method that implements them lives in [`tech-docs.md`](./tech-docs.md).
> Web citations in this file are dated **2026-07-28** — see `tech-docs.md §Appendix A` for the full
> verified digest.

## Business goal

Cut the runtime, hosting, and maintenance cost of `apps/ayokoding-www` (the AyoKoding educational
content platform at [ayokoding.com](https://ayokoding.com)) across four cost lines — **build minutes,
image size / cold start, client bundle weight, and security/maintenance debt** — without retreating
from full SSG, without altering the bilingual surface, and without breaking any existing Gherkin
scenario under `specs/apps/ayokoding/`. The plan pairs the cut with a dependency modernization sweep
that binds every bump to the repo's
[Dependency Bump Stability & Safety Policy](../../../repo-governance/development/workflow/dependency-bump-policy.md)
(Path A LTS / Path B 60-day soak / Path C security waiver).

## Business rationale

### The pain (concrete, not abstract)

The app has accreted real cost across four lines, every one measured against the current tree:

- **Build minutes** — every `dev`, `build`, and CI run regenerates
  `generated/search-data.json` (a **3.0 MB** FlexSearch index file,
  `apps/ayokoding-www/generated/search-data.json`) plus walks all **2,008 markdown files** in
  `content/` to regenerate `_index.md` files; `project.json:42-50` `dependsOn` lists both generators
  and `vercel.json:4` duplicates them inline (`project.json`-vs-`vercel.json` config drift). On top
  of that, `project.json:68` lints via `npx oxlint@latest` — a **non-reproducible** lint that pays a
  network round-trip per CI run (research measured the `npx` overhead alone at **3× a cached binary**
  of the same invocation — see [tech-docs.md §Appendix A.7](./tech-docs.md#a7--oxlint-reproducibility)).
- **Image size / cold start** — the Dockerfile (`apps/ayokoding-www/Dockerfile:47`) copies the
  **97 MB `content/`** directory into the runner image and `next.config.ts:25-27` declares
  `outputFileTracingIncludes: { "/**": ["./content/**/*", "./generated/**/*"] }`, a glob pattern
  the Next.js docs explicitly warn against ("Keep patterns as narrow as possible to avoid oversized
  traces (avoid `**/*` at the repo root)" — cited at
  [tech-docs.md §Appendix A.2](./tech-docs.md#a2--output-standalone--outputfiletracingincludes)).
  The result: a ~100 MB inflation of the standalone function image versus what Next's tracer would
  pick up by itself.
- **Client bundle weight** — `flexsearch@0.7.43` (the **stale 0.7 major**; `0.8.212` is published)
  ships a **3 MB per-locale search index baked into the client bundle**
  (`apps/ayokoding-www/generated/search-data.json`); `mermaid@11` ships ~**700 KB of client JS** to
  render diagrams client-side after hydration
  ([Appendix A.6](./tech-docs.md#a6--mermaid-build-time-vs-runtime)); and the
  `cost-of-living-calculator` route bakes **155 KB of hand-curated data** (`cities.ts` 79 KB +
  `roles.ts` 76 KB) into its initial bundle.
- **Security/maintenance debt** — `html-react-parser` is used at runtime to render content HTML and
  is **explicitly not XSS-safe** per its own README ("No, this library is not XSS-safe (see [#94])."
  cited at [Appendix A.10](./tech-docs.md#a10--html-react-parser-security-surface)); the app pins
  `typescript@5.8.3` while TS 7.0 (Go-native, **8–12× faster `tsc`**) is GA and the documented
  side-by-side alias (`npm:@typescript/typescript6` + `npm:typescript@^7`) is the supported path
  ([Appendix A.8](./tech-docs.md#a8--typescript-7--nextjs-16-compatibility)); the `README.md:71-79`
  source-layout table omits the `cost-of-living-calculator` feature entirely and mis-states
  `app-shell` as shell-only; `vitest.config.ts:58` declares `lines: 80` while
  `project.json:84` requires `--coverage.thresholds.lines=82` — silent config drift.

### Why this repo, and why now

- The repo is mid-programme on `apps/ayokoding-www`: [`ayokoding-learning-path-04`](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md)
  is shipping roughly one course per week, and the now-completed
  [`ayokoding-www-tools-ai-benchmark`](../../done/2026-07-30__ayokoding-www-tools-ai-benchmark/README.md) copied
  the `cost-of-living-calculator`'s FCIS layout. Every additional course the programme ships **multiplies
  the build-minute and `generate-search-data` cost** — the 3 MB FlexSearch index scales with the
  recent course-shipping velocity. Deferring the cost pass means every weekly course ships against a
  larger, costlier, more brittle runtime.
- The stabilizing window for the four biggest changes the plan needs (TS 7, Next 16.3+, Pagefind,
  rehype-mermaid) is **already open in 2026-07**: TS 7.0 GA'd 2026-07-08; Next 16.3 added
  `experimental.useTypeScriptCli`; Pagefind 1.4+ is mature; `rehype-mermaid` v3 is published and
  in use. Catching the window now means the modernization cost is paid once rather than re-discovered
  against larger content next quarter.
- The repo's own governance binds dep bumps to a classifying decision tree, so a modernization pass
  done _right_ is auditable; one done under pressure (a CVE-driven rush after a year of caret-pin
  drift) costs more for a worse outcome.

### Expected benefits

| Benefit                                                                                                                         | Evidence basis                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Search routes ship ~**3 MB → ~300 KB lazy** of client JS, an order-of-magnitude initial-bundle cut                              | Observable — Pagefind's own published threshold is "under 300 kB, including the library itself" for a 10k-page site (cited at [Appendix A.4](./tech-docs.md#a4--pagefind-vs-flexsearch)) |
| Mermaid routes ship **~700 KB → 0** client JS; diagrams render as static inline SVG at build time                               | Observable — artka.dev measurement plus `rehype-mermaid` README (cited at [Appendix A.6](./tech-docs.md#a6--mermaid-build-time-vs-runtime))                                              |
| The runtime content-HTML XSS surface is **removed**, not papered over                                                           | Observable fact — the `html-react-parser` README itself states the library is not XSS-safe; removal is the root-cause fix (Appendix A.10)                                                |
| `nx typecheck` runs **8–12× faster** through the Go-native `tsc`, freeing CI minutes proportional to current type-check latency | Cited measurement — Microsoft TS 7.0 announcement, Slack 7.5 min → 1.25 min on a large repo (Appendix A.8)                                                                               |
| The Docker image loses ~100 MB from a narrowed trace and a `node:24-slim` base, and oxlint runs without a network round-trip    | Observable — `next.config.ts:25-27` and `project.json:68` are the levers                                                                                                                 |

## Affected roles

Solo-maintainer repository; "roles" here are the hats the maintainer wears and the agents that
consume the artifacts. There is no sign-off ceremony.

| Role / hat                                | Relationship to this work                                                                                                                                               |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Frontend developer (maintainer)           | Owns the rehype pipeline, the search feature module, the calculator lazy-load split, and the `next.config.ts` trace narrowing                                           |
| Build / DevOps (maintainer)               | Owns the `Dockerfile` base swap, oxlint pinning, generator dedup, the validate-indexes wiring, and the TS 7 side-by-side `tsc` invocation                               |
| Repo governance owner                     | Consumes the deps-policy binding record in `tech-docs.md` when auditing the bump decisions; binds the same Path A/B/C classifications                                   |
| `apps-ayokoding-www-facts-checker`        | Validates every cited cost number in this file against `tech-docs.md §Appendix A` and against the live file at the cited path                                           |
| `swe-code-checker` / `swe-ui-checker`     | Validates the static code surface and token/a11y compliance for Phase 6 (calculator) and Phase 3 (search UI) per the Surface-Conditional Tester Gates                   |
| `web-exploratory/usability/design-tester` | Rule-15 retest against the live site after the reveal — verifies search behaviour, diagram rendering, calculator lazy-load UX across both locales and three breakpoints |
| Public reader (the audience)              | Sees the same educational content at faster cold start and a smaller bundle; the mermaid diagrams arrive without a hydration flash                                      |

## Success signals

No fabricated numeric KPI appears below. Each signal is either an observable repository fact or an
explicitly-labelled judgment. Every numeric claim cites an Appendix A entry.

| Signal                                                                                                                                       | Kind            | How it is observed                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `apps/ayokoding-www/generated/search-data.json` no longer exists; no `flexsearch` import remains in `src/`                                   | Observable fact | After Phase 3: `test -f apps/ayokoding-www/generated/search-data.json` exits non-zero and `grep -rn "flexsearch" apps/ayokoding-www/src` prints nothing                                                           |
| No `mermaid` runtime import remains in any client component                                                                                  | Observable fact | After Phase 4: `grep -rn "from \"mermaid\"" apps/ayokoding-www/src` prints nothing                                                                                                                                |
| No `html-react-parser` runtime import remains in any client component                                                                        | Observable fact | After Phase 5: `grep -rn "from \"html-react-parser\"" apps/ayokoding-www/src` prints nothing                                                                                                                      |
| `apps/ayokoding-www/package.json` carries `"typescript": "npm:@typescript/typescript6@^6.0.2"` and `"typescript-7": "npm:typescript@^7.0.2"` | Observable fact | After Phase 2: `node -e "const p=require('./apps/ayokoding-www/package.json').devDependencies; console.log(p.typescript, p['typescript-7'])"` prints the two aliases                                              |
| `nx typecheck` invokes the Go-native `tsc` (or `tsgo`) binary, not the JS API path                                                           | Observable fact | After Phase 2: the `typecheck` target in `project.json` invokes `tsc-7` (or `tsgo`) per the alias wiring                                                                                                          |
| `vitest.config.ts` coverage `lines` and `project.json` `--coverage.thresholds.lines` agree                                                   | Observable fact | After Phase 1: both declare the same number (`grep -E "lines:                                                                                                                                                     | thresholds.lines=" apps/ayokoding-www/vitest.config.ts apps/ayokoding-www/project.json`) |
| `npx oxlint` no longer appears in any `app/ayokoding-www` target; `oxlint` is an exact-pinned `devDependencies` entry                        | Observable fact | After Phase 1: `grep "oxlint" apps/ayokoding-www/project.json apps/ayokoding-www/package.json` names the pinned version, not `@latest`                                                                            |
| The Docker image uses `node:24-slim`, not `node:24-alpine`, and the `outputFileTracingIncludes` carries per-route globs, not `"/**"`         | Observable fact | After Phase 7: `grep "FROM node:" apps/ayokoding-www/Dockerfile` prints `node:24-slim`; `next.config.ts` declares narrowed globs                                                                                  |
| The calculator route's initial bundle loses `cities.ts` (79 KB) + `roles.ts` (76 KB) — they load on demand                                   | Observable fact | After Phase 6: the calculator-route bundle report (Next build output) no longer lists these files in the initial chunk                                                                                            |
| Search, mermaid rendering, and calculator behave correctly under the live-site triad                                                         | _Judgment call_ | Assessed during the Phase 8 Rule-15 retest (EWT/UWT/DWT findings + spec gaps triaged), not by a metric                                                                                                            |
| Build-minute cost drops                                                                                                                      | _Judgment call_ | Not measured by a metric in this plan; the reasoning is the four build-minute levers above (oxlint pin, generator dedup, TS 7 typecheck, SSR-without-trace-inflation). A future plan may add a build-time budget. |

## Business-scope non-goals

- **No bilingual parity work.** The `id` locale's 124-file stub is out of scope; the asymmetry is
  recorded as known debt, not addressed here.
- **No ISR migration.** The plan keeps **full SSG for every route whose render is compatible** —
  every statically enumerable content page stays baked at build time; the catch-all
  `generateStaticParams` keeps enumerating all 1,884 content slugs. `dynamicParams = true` already
  covers only the manifest-driven `learn/paths/**` namespace that genuinely cannot be statically
  baked. This preserves 0 ms first-visit and 0 ISR-metering. The Vercel plan is **Pro ($20/mo)**,
  which buys 12-way build parallelism (the lever that matters for the weekly course-ship programme)
  but the same 45-min single-build cap as Hobby; build-minute headroom is ample today. ISR tiering
  is deferred to a future plan with real build-pressure data.
- **No build-time content ingestion.** The runtime `fs.readFile` of `content/` stays; the plan
  narrows the trace patterns only. Eliminating `fs.readFile` is a content-pipeline re-architecture
  that exceeds the agreed scope tier.
- **No A11y overhaul.** The two `jsx-a11y` suppressions in the calculator route are noted as known
  debt and deferred to a focused A11y plan.
- **No new screens.** This plan adds no user-facing routes; search, content, and calculator keep
  their existing URLs and are not UI-bearing for the design-funnel convention.

## Business risks and mitigations

| Risk                                                                                                                                   | Impact                                                              | Mitigation                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TS 7 side-by-side breaks `next build`.** TS 7's `tsc` loses `lib/typescript.js`; the fallback is the `@typescript/typescript6` alias | Build halts                                                         | The Phase 2 plan follows the documented side-by-side recipe; bumps Next to 16.3+ as the floor for `experimental.useTypeScriptCli`; the existing `tsc` (under the TS6 alias) remains the JS-API path for Next     |
| **Pagefind's UI differs from the existing FlexSearch dialog** enough to regress the search UX                                          | Reader experience worsens                                           | Phase 3 ships the new search behind the existing dialog wrapper; the Rule-15 retest (Phase 8) verifies the search flow across both locales and three breakpoints before archival                                 |
| **`rehype-mermaid` adds Playwright/Chromium to the build image**, inflating the build minute budget it is supposed to reduce           | Build minutes per build rise by ~5 s cold-warm                      | The Playwright browser is one shared per build (not per diagram); the cost is small (research measured 32 diagrams in 11.6 s cold / 6.3 s warm, Appendix A.6)                                                    |
| **`html-react-parser` runs against carefully-curated content**, so the XSS surface is theoretical rather than real                     | Reader sees a regression on content that no longer renders          | A build-time rehype replacement parses the same Markdown to the same AST; surface output is identical or a clean-enrichment (e.g., class additions), verified by snapshot tests in Phase 5                       |
| **A Path A / Path B bump lands a known issue** — the classic caret-pinned update footgun                                               | Build or test regression                                            | Every bump in Phase 2 carries a written Path classification in `tech-docs.md §Design Decisions`; `repo-rules-checker` and `apps-ayokoding-www-facts-checker` validate the classifications                        |
| **Concurrent sessions write into the same `apps/ayokoding-www` files**                                                                 | Merge conflict on shared config (`package.json`, `next.config.ts`)  | One-worktree-one-PR-per-unit HARD RULE; the Plan-Execution workflow Step 0 gate syncs against `origin/main` before each phase; PRs open at delivery boundaries, not on every commit                              |
| **`outputFileTracingIncludes` narrowing drops a file that's actually needed at runtime**                                               | A content page renders a 500                                        | Phase 7 narrows conservatively from `/**` to per-route globs derived from the actual `fs.readFile` call sites; a unit assertion confirms the narrowed glob set still covers every `fs.readFile` target in `src/` |
| **TS 7 strict-mode errors** lock the repo into a stricter constraint than caret deps were silently tolerating                          | Type errors cascade across the existing 253 production source files | Phase 2 keeps the existing `tsconfig.json` strictness; the TS-7 invocation runs the native `tsc` against the SAME config, surfacing pre-existing issues rather than introducing new ones                         |

## Cross-references

- Testable expressions of every claim above: [`prd.md` §Acceptance Criteria](./prd.md#acceptance-criteria).
- The method, the deps-policy binding, and the cited research snapshot: [`tech-docs.md`](./tech-docs.md).
- Phase-by-phase execution: [`delivery.md`](./delivery.md).
