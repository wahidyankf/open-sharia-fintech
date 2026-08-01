# Baseline — per-project measurement

**Captured**: 2026-08-01 15:30 WIB (UTC+7)
**Method**: Vercel MCP (`plugin:vercel:vercel`), `get_runtime_logs` with `group_by`, plus `curl -D -`
against live production. No dashboard access was needed.
**Satisfies**: delivery step 0.1 (DD-7 — per-project attribution must be measured, not inferred)

## What this file replaces

DD-7 stated that aggregate billing figures cannot be split per project from repo evidence, and that
the "middleware-count ≈ function-count" equality only _implies_ `ayokoding-www` dominates. That
inference is now a measurement.

## Method and its limits

`get_runtime_logs` returns **log-event counts**, not billed units. Read this file as an
**attribution and volume** baseline, not as a dollar baseline:

- It answers "which project burns the functions, and on which routes" — exactly what DD-7 needed.
- It does **not** report GB-Hrs, Active CPU, Provisioned Memory, or any currency figure. The Vercel
  MCP exposes no billing, usage, or invoice tool (see
  [tech-docs.md §Vercel MCP capability boundary](../tech-docs.md#vercel-mcp-capability-boundary)),
  so the dollar side of Phase 0.1 remains `[HUMAN]`, as does the whole of the successor plan
  [`vercel-cost-steady-state-verification`](../../../backlog/vercel-cost-steady-state-verification/README.md).
- Window limits observed empirically: `since: "24h"` and `since: "72h"` both return; `since: "7d"`
  fails with `Aggregate query failed: timed out`. **72h is the widest usable window.**
- Retention depends on Observability, which delivery step 0.5 disables. This snapshot was therefore
  taken **before** 0.5, per DD-7's ordering requirement.

## Per-project invocation baseline — production, last 24h

| Project                | function | middleware | redirect | cache | Verdict                          |
| ---------------------- | -------- | ---------- | -------- | ----- | -------------------------------- |
| `ayokoding-www`        | 43,105   | 43,422     | 5,290    | —     | **Dominant. 99.9% of functions** |
| `wahidyankf-www`       | 45       | —          | 6        | —     | Negligible volume                |
| `ose-www`              | 0        | —          | 14       | 86    | Cached, no functions             |
| `organiclever-www`     | 0        | —          | —        | 26    | Cached, no functions             |
| `organiclever-app-web` | 0        | —          | —        | 11    | Cached, no functions             |
| `ose-app-web`          | 0        | —          | —        | 1     | Cached, no functions             |
| `web-ui` (Storybook)   | 0        | —          | —        | —     | No runtime events at all         |

`ayokoding-www` accounts for **43,105 of 43,150** function events across all seven projects —
**99.90%**. DD-6's exclusion of the four already-cached projects is confirmed by measurement, not
just by cache headers.

## `ayokoding-www` over 72h — the wider window

| source     | 72h count | implied per-day |
| ---------- | --------- | --------------- |
| middleware | 274,463   | 91,488          |
| function   | 273,487   | 91,162          |
| redirect   | 18,304    | 6,101           |
| cache      | 1         | 0               |

**Independent corroboration of the plan's premise**: the plan's opening figure was 341K invocations
over ~4 days = **85,250/day**, read off the billing dashboard on 2026-07-30. This measurement, taken
two days later from a different data source, gives **91,162/day** — within ~7%. Two independent
methods agree.

The 24h window (43,105) is roughly half the 72h daily rate, so **daily volume is variable**; use the
72h rate for projections and never a single 24h sample.

**`middleware ≈ function` is now measured, not inferred**: 274,463 vs 273,487 over 72h — a 0.36%
difference. Every function invocation is preceded by a middleware invocation, which is exactly the
circular-cost finding in tech-docs.md.

## `ayokoding-www` function volume by route — production, last 24h

| route                                       | count  | share |
| ------------------------------------------- | ------ | ----- |
| `/[locale]/[...slug]`                       | 36,881 | 85.6% |
| `/[locale]`                                 | 1,421  | 3.3%  |
| `/[locale]/browse`                          | 1,323  | 3.1%  |
| `/[locale]/tools/ai-benchmark`              | 1,273  | 3.0%  |
| `/[locale]/tools/cost-of-living-calculator` | 1,212  | 2.8%  |
| `/[locale]/tools`                           | 979    | 2.3%  |
| `/robots.txt`                               | 190    | 0.4%  |
| `/`                                         | 98     | 0.2%  |
| `/sitemap.xml`                              | 27     | 0.1%  |
| `/api/trpc/[trpc]`                          | 12     | 0.0%  |

**The content catch-all `[...slug]` alone is 85.6% of all function volume.** Phases 1–2 target
precisely this route, so the plan's leverage ordering is confirmed against measured data.

Note the two `tools/*` routes still invoke functions (1,273 + 1,212) despite already using the
`<Suspense>` + `useSearchParams()` pattern — because **Cause A in the root layout makes every route
dynamic regardless**. This is direct evidence that Cause A, not per-route code, is the binding
constraint. Phase 4's "confirm the tools routes stay static" check should therefore expect these
counts to collapse after Phase 1, and that is a falsifiable prediction of the fix.

## `ayokoding-www` status codes — production, last 24h

| statusCode | count  | note                                                           |
| ---------- | ------ | -------------------------------------------------------------- |
| 200        | 42,524 | —                                                              |
| 404        | 731    | 1.7% of traffic is billed function time spent producing 404s   |
| 307        | 98     | the `/` → `/en` middleware redirect                            |
| 504        | 49     | **new finding — gateway timeouts, not previously in the plan** |
| 206        | 13     | —                                                              |

**New finding (504s)**: 49 gateway timeouts in 24h. Not in the original analysis. Each is a function
that ran to its limit and billed for it. This is consistent with the cold-start cost driver in
tech-docs.md (a full 2,068-file / 70 MiB content-index read per cold start). Static conversion should
eliminate the class outright; if 504s survive Phase 4, that is a signal worth a follow-up.

## Live header evidence — re-verified today

Three consecutive requests to the same content URL, 2026-08-01:

```text
GET https://www.ayokoding.com/en/learn/courses/debugging-and-profiling/learning
run1  x-vercel-cache: MISS  x-vercel-id: sin1::iad1::dmln6-...
run2  x-vercel-cache: MISS  x-vercel-id: sin1::iad1::qndm5-...
run3  x-vercel-cache: MISS  x-vercel-id: sin1::iad1::r7c97-...
cache-control: private, no-cache, no-store, max-age=0, must-revalidate
```

Unchanged from the 2026-07-30 observation. Same for `https://www.wahidyankf.com/cv`.

The four excluded projects remain cached:

| URL                             | `x-vercel-cache` | `x-nextjs-prerender` | `age`     |
| ------------------------------- | ---------------- | -------------------- | --------- |
| `https://oseplatform.com/`      | HIT              | 1                    | 69,711    |
| `https://www.organiclever.com/` | HIT              | 1                    | 4,036,579 |

## Phase 0.6 resolved — middleware **does** execute on Next.js 16.2.6

The blocking unresolved risk is answered by measurement rather than by reading conflicting secondary
sources: **274,463 `middleware`-source log events in 72h**. The middleware is live, not a silent
no-op. Corroborated by `curl`: `https://ayokoding.com/` still returns a redirect chain.

**Consequence for Phase 3**: it is the "replace before delete" branch. The `/` → `/en` and
uppercase-locale redirects must land in `next.config.ts` **before** `src/middleware.ts` is deleted.

## Phase 6 item re-verified — the apex redirect still downgrades to HTTP

```text
GET https://ayokoding.com/
HTTP/2 301
location: http://www.ayokoding.com     <-- http, not https
```

Still reproduces on 2026-08-01. Remains `[HUMAN]` — no MCP tool configures domains or redirects.

## What still needs a human

| Datum                                              | Why MCP cannot supply it                                     |
| -------------------------------------------------- | ------------------------------------------------------------ |
| Cycle-to-date Infrastructure Subtotal (was $7.43)  | No billing/usage tool in the MCP                             |
| Per-line-item costs (GB-Hrs, Observability Events) | Same                                                         |
| Whether Fluid Compute is on                        | `get_deployment` reports `type: "LAMBDAS"` and no fluid flag |
| Spend Management / firewall / Observability state  | No settings tool of any kind                                 |
