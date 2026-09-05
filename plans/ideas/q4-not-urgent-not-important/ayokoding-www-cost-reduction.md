# Cut ayokoding-www's four accreted cost lines: bundle, image, build, and dependency debt

One-line summary: `apps/ayokoding-www` ships a 3 MB FlexSearch index and ~700 KB of client Mermaid
to every reader, copies 97 MB of `content/` into its runtime image behind a trace glob its own
framework docs warn against, and carries a not-XSS-safe HTML parser plus a stale TypeScript pin — a
single coordinated pass can retire all four.

> Demoted 2026-08-05 from a full `backlog/` plan to this two-pager. The plan was **never executed**
> — its delivery checklist held 188 items, none checked. The full folder had carried a README, BRD,
> PRD (personas, user stories, F-1…F-16 product scope, AC-1…AC-28 Gherkin), tech-docs (DD tables,
> per-phase file-impact analysis, a dependency Path A/B/C classification table, and a ten-entry
> research appendix), a ten-phase delivery checklist with a delivery DAG and boundaries table, and
> an empty learnings log.

## Problem / context

The app has accreted real cost along four measured lines, every number read off the current tree:

- **Client bundle weight** — `flexsearch@0.7.43` (the stale 0.7 major) bakes a **3.0 MB** per-locale
  index (`generated/search-data.json`) into the client bundle; `mermaid@11` ships **~700 KB** of JS
  to render diagrams client-side after hydration, producing a visible diagram flash; the
  `cost-of-living-calculator` route bakes **155 KB** of hand-curated data (`cities.ts` 79 KB +
  `roles.ts` 76 KB) into its initial bundle.
- **Image size and cold start** — the Dockerfile copies the **97 MB `content/`** directory into the
  runner image for runtime `fs.readFile`, and `next.config.ts` declares
  `outputFileTracingIncludes: { "/**": [...] }` — precisely the broad root glob the Next.js docs
  tell you to avoid. Together these inflate the standalone image by roughly 100 MB over what the
  tracer would pick up on its own. All three Docker stages sit on `node:24-alpine` (musl) rather
  than the glibc `node:24-slim` the upstream `with-docker` example uses.
- **Build minutes** — every build regenerates the 3 MB search index and walks all **2,008 markdown
  files** to refresh `_index.md` files; `project.json` and `vercel.json` each declare the same two
  prebuild generators (config drift); and lint runs through `npx oxlint@latest`, a non-reproducible,
  network-dependent invocation. The `validate-indexes` target exists but was never wired into
  `test:quick`, so index drift ships silently.
- **Security and maintenance debt** — `html-react-parser` renders content HTML at runtime and its
  own README states plainly that it is not XSS-safe; `typescript@5.8.3` is pinned while TS 7.0
  (Go-native `tsc`, 8–12× faster on Microsoft's published benchmark) is GA; three `@trpc/*` entries
  sit on caret pins; the app README's source-layout table omits the calculator feature; and
  `vitest.config.ts` (`lines: 80`) disagrees with `project.json`
  (`--coverage.thresholds.lines=82`).

## Why now

The app is mid-programme: the course-authoring line is shipping steadily, and every course added
multiplies the search-index size, the route count, and the build-minute cost — deferring means each
future course ships against a larger, costlier, more brittle runtime. The stabilization window for
the four biggest levers opened together and is open now: TypeScript 7.0 went GA on 2026-07-08,
Next.js 16.3 added `experimental.useTypeScriptCli` as its floor, Pagefind 1.4+ is a mature line, and
`rehype-mermaid` v3 is published. Paying the modernization cost once inside a deliberate pass beats
rediscovering it under a CVE-driven rush after another year of caret-pin drift.

## Prior art / precedents

- [Dependency Bump Stability & Safety Policy](../../../repo-governance/development/workflow/dependency-bump-policy.md)
  — the Path A (LTS latest patch) / Path B (60-day soak + CVE-clean) / Path C (security waiver)
  decision tree every bump in this work must classify against, with exact pins throughout.
- [`ayokoding-www-tools-ai-benchmark`](../../done/2026-07-30__ayokoding-www-tools-ai-benchmark/README.md)
  — a completed sibling that shipped the same calculator-style static-data surface; its file-impact
  footprint overlapped only on the shared token CSS, which is the precedent that this work can
  proceed without colliding with content programmes.
- [`ayokoding-learning-path-04-course-authoring`](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md)
  — the completed content-programme baseline whose successors keep growing the route and index
  counts this work is trying to bound.
- [`post-cutoff-dependency-migrations`](../q2-not-urgent-important/post-cutoff-dependency-migrations.md) — the standing brief
  for tracking deferred dependency bumps as their soak windows clear; the modernization stream here
  should be reconciled against it rather than duplicating it.
- [`apps/ayokoding-www/README.md`](../../../apps/ayokoding-www/README.md) — the app's own source-layout
  and feature documentation, one of the artifacts the quick-win stream corrects.

## Proposed direction (sketch)

Six work streams, most of them serialized by shared config files (`package.json`, `next.config.ts`,
`project.json`, `vercel.json`) rather than by logic:

- **Quick wins** — pin `oxlint` as an exact devDependency, reconcile the two coverage thresholds,
  fix the README feature table, de-duplicate the prebuild generators to a single Nx-driven source,
  and gate `validate-indexes` in `test:quick`.
- **Dependency modernization** — adopt TypeScript 7 side-by-side (a TS 6 alias keeps the JS API that
  Next's build needs; the Go-native compiler drives `typecheck`), bump Next to the 16.3 floor, and
  exact-pin the remaining patch-level and caret-pinned entries with a written Path classification.
- **Pagefind migration** — drop `flexsearch` and its `serverExternalPackages` carve-out, index the
  built HTML with Pagefind after `next build`, and delete the `generate-search-data` target and the
  3 MB artifact it produces.
- **Build-time Mermaid** — replace the client renderer with `rehype-mermaid` at `inline-svg` in the
  existing rehype pipeline, one shared browser per build, and drop `mermaid` entirely.
- **`html-react-parser` removal** — move every runtime HTML-to-React transform into a build-time
  rehype step so the SSG output ships pre-rendered, then drop the dependency.
- **Calculator lazy-load** — split the two static data modules behind dynamic `import()` so the
  route's lookup logic stays bundled but its 155 KB of data loads on demand.
- **Docker base and trace narrowing** — move to `node:24-slim` and replace the root `"/**"` trace
  glob with per-route globs derived from the actual `fs.readFile` call sites.

## Rough scope & non-goals

In scope: the six streams above, plus companion Gherkin under the app's specs tree for the three
behaviour-changing streams (search, diagram rendering, calculator lazy-load), bound by Unit and E2E
step definitions, and a live-site retest before archival since the changes are UI-affecting at
runtime without adding screens.

Explicitly out of scope, carried forward from the plan's named list:

- **Bilingual parity** — the `id` locale's 124-file stub against `en`'s 1,884 is recorded as known
  debt; fixing or honestly downgrading the bilingual claim needs its own plan.
- **ISR migration** — the work keeps full SSG for every compatible route, preserving 0 ms
  first-visit and zero ISR metering; build-minute headroom is ample today, so ISR tiering waits for
  a plan with real build-pressure data.
- **Build-time content internalization** — runtime `fs.readFile` of `content/` stays; only the trace
  patterns narrow. Eliminating it is a content-pipeline re-architecture.
- **Dockerfile workspace hoisting** — the manual `cp -r` of the shared UI library is brittle, but a
  proper workspace link needs a standalone-output layout fix rivaling the trace work.
- **The calculator's two `jsx-a11y` suppressions** — a click handler on a `div` and an
  unassociated label; known A11y debt for a focused A11y plan.
- **The misfiled `next-config-security.unit.test.ts`** — small unrelated debt.
- **The two `react-hooks/exhaustive-deps` suppressions** in the calculator — intentional, untouched.
- Also declined: lazy-loading the calculator's lookup _logic_ (only its data moves), replacing
  `oxlint` with another linter, adding runtime APM or a build-time budget step, and a
  `flexsearch 0.7 → 0.8` migration (breaking, and it would not retire the client-index lever at all).

## Risks & open questions

- **TypeScript 7's Go-native compiler will surface pre-existing strict-mode errors** across the
  production sources, reading the same `tsconfig.json` the JS-API compiler tolerated silently. How
  many, and whether they are cheap to fix, is unmeasured. (open)
- **The exact TS 7 typecheck invocation is undecided** — whether the aliased package or a standalone
  Go-native CLI is the clean entry point was left to be settled at execution time. (open)
- **`html-react-parser`'s removal must carry every `replace()` branch across** — the renderer has
  eight distinct transform branches, and each needs a verified build-time equivalent or content
  silently regresses. Snapshot coverage is the intended gate. (open)
- **Narrowing the trace can drop a file something actually reads at runtime**, manifesting as a 500
  on a live route rather than a build failure. The mitigation is deriving globs from audited
  `fs.readFile` call sites, but the audit's completeness against concurrently-landing code is
  unproven. (open)
- **Pagefind's search UX may not match the existing dialog** closely enough to avoid a reader-facing
  regression; the intent is to keep the existing dialog wrapper and swap only the engine. (open)
- `rehype-mermaid` adds a build-time browser launch — expected to be small since it is one shared
  browser per build, but it does trade a client cost for a build cost.
- Build-minute savings were never quantified; the plan itself flagged this as a judgment call rather
  than a metric, so the build-minute stream rests on reasoning, not measurement. (open)

Research behind the version, sizing, and migration claims above was gathered by `web-researcher` on
2026-07-28 against Vercel and Next.js documentation, Pagefind, flexsearch, rehype-pretty-code, shiki,
`rehype-mermaid`, oxlint, the Microsoft TypeScript 7.0 announcement, webpack SplitChunks, and the
`html-react-parser` README.

## What success looks like + promotion signal

Success is falsifiable per stream and does not need a synthetic KPI: no `flexsearch` import or
`search-data.json` artifact remains; no client `mermaid` or `html-react-parser` import remains; the
trace declares per-route globs instead of the root `"/**"`; the Docker base is `node:24-slim`; lint
runs a pinned local binary; the two coverage thresholds agree; and the calculator route's initial
chunk no longer carries its two data modules — with search, diagrams, and the calculator verified
working across both locales at mobile, tablet, and desktop.

**Promotion signal**: re-promote to a full plan when either (a) a measured build or bundle pressure
signal appears — a build approaching its cap, a Lighthouse or bundle-report regression on the search
or calculator routes, or a CVE landing on `html-react-parser`, `flexsearch`, or `mermaid` — or (b)
the streams can be re-scoped as independently shippable units. The single most useful de-risking
step before promotion is a throwaway spike answering the TypeScript 7 question: run the Go-native
compiler against the existing config and count the errors. If that count is small, the modernization
stream unblocks the rest; if it is large, that stream should be split off and the bundle-weight
streams promoted on their own.
