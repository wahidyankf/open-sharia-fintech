# Delivery — Vercel Function Cost Reduction

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (the safe-to-stop state and how to resume). A phase is not complete
> until its gate is green; do not start phase N+1 while any gate check fails.
>
> This plan **does** use `[HUMAN]` steps. Phase 0 is almost entirely `[HUMAN]` because no agent can
> reach the Vercel dashboard, and Phase 7 requires reading a billing figure only the account owner
> can see. Git-mechanical steps (worktree create/remove, branch, push, merge) remain `[AI]`.

## Worktree

This plan uses **three** worktrees, one per independent delivery unit, per the strict
1-PR ↔ 1-worktree rule:

| Unit | Worktree path                       | Branch                                           |
| ---- | ----------------------------------- | ------------------------------------------------ |
| 1    | `worktrees/vercel-cost-ayokoding/`  | `vercel-function-cost-reduction/ayokoding-www`   |
| 2    | `worktrees/vercel-cost-wahidyankf/` | `vercel-function-cost-reduction/wahidyankf-www`  |
| 3    | `worktrees/vercel-cost-secondary/`  | `vercel-function-cost-reduction/secondary-waste` |

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree vercel-cost-ayokoding
```

After any `git worktree add`, run `npm install` **and** `npm run doctor -- --fix` per the Worktree
Toolchain Initialization requirement.

Plan-document authoring and promotion happen on local `main` under the plan-docs-only carve-out;
execution-time delivery ticks go in the relevant worktree copy.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each unit works in its own worktree; a draft PR opens against `main` once that unit has committed
work; the PR-Review Maker→Fixer Cycle (3 sequential CI-gated cycles) runs before merge; `[AI]`
merges once the hardened preconditions hold. See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode).

## Parallelization Model

`1 main thread + N background agents`, **N=3**. The three code units touch disjoint apps and share
no files, so they are independent DAG leaves and fan out to fill all three slots. Phase 0 gates all
of them; Phase 7 joins them.

### Dependency DAG

```mermaid
flowchart TD
  P0["Phase 0<br/>platform settings + baseline<br/>(HUMAN, no PR)"]
  U1A["Phase 1<br/>Cause A: root layout"]
  U1B["Phase 2<br/>Cause B: searchParams"]
  U1C["Phase 3<br/>middleware elimination"]
  U1D["Phase 4<br/>bundle + cold-start hygiene"]
  U2["Phase 5<br/>wahidyankf-www<br/>(Unit 2)"]
  U3["Phase 6<br/>secondary waste<br/>(Unit 3)"]
  P7["Phase 7<br/>steady-state measurement<br/>(HUMAN)"]
  P8["Phase 8<br/>Knowledge Capture"]
  P9["Phase 9<br/>Archival + merge"]

  P0 --> U1A --> U1B --> U1C --> U1D --> P7
  P0 --> U2 --> P7
  P0 --> U3 --> P7
  P7 --> P8 --> P9

  style P0 fill:#0072B2,color:#FFFFFF
  style P7 fill:#0072B2,color:#FFFFFF
  style U1A fill:#D55E00,color:#FFFFFF
  style U2 fill:#009E73,color:#FFFFFF
  style U3 fill:#009E73,color:#FFFFFF
  style P9 fill:#CC79A7,color:#FFFFFF
```

Phases 1→2→3→4 are a dependent chain: Cause B's build verification needs Cause A fixed first; the
middleware can only be deleted once nothing reads `x-pathname`; and tracing scope depends on which
routes ended up static. One chain, one worktree, one PR.

### Delivery Boundaries

| Delivery unit | Phases                            | Worktree / branch                                                                      | PR opens at                                                  |
| ------------- | --------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Unit 1        | Phases 1–4 (`apps/ayokoding-www`) | `worktrees/vercel-cost-ayokoding/` on `vercel-function-cost-reduction/ayokoding-www`   | Phase 1 (draft); reviewed and merged at the Phase 4 boundary |
| Unit 2        | Phase 5 (`apps/wahidyankf-www`)   | `worktrees/vercel-cost-wahidyankf/` on `vercel-function-cost-reduction/wahidyankf-www` | Phase 5 (draft); reviewed and merged at the Phase 5 boundary |
| Unit 3        | Phase 6 (secondary waste)         | `worktrees/vercel-cost-secondary/` on `vercel-function-cost-reduction/secondary-waste` | Phase 6 (draft); reviewed and merged at the Phase 6 boundary |
| Closeout      | Phases 7–9                        | `worktrees/vercel-cost-ayokoding/` reused after Unit 1 merges                          | Phase 9                                                      |

Phase 0 opens **no PR** (hard rule); its evidence rides Unit 1's PR.

---

## Phase 0: Platform settings, baseline, and the middleware-behaviour question

> Almost every step here is `[HUMAN]` — an agent cannot authenticate to the Vercel dashboard. Do
> them in the stated order: the baseline snapshot must precede disabling Observability, or the
> per-project attribution is lost permanently.

### 0.1 Capture the per-project baseline — DO THIS FIRST

- [ ] `[HUMAN]` In Vercel → Observability, record **per-project** figures for the current cycle for
      each of the six projects (`ayokoding-www`, `ose-www`, `organiclever-www`, `wahidyankf-www`,
      `organiclever-app-web`, `ose-app-web`): Function Invocations, Function Duration (GB-Hrs), Edge
      Middleware Invocations, Edge Requests.
  - Acceptance: a table of six rows × four metrics is committed to
    `plans/in-progress/vercel-function-cost-reduction/evidence/baseline-per-project.md`. Before this
    step the file does not exist; after it, `test -f` exits 0 and the file names all six projects.
  - Rationale: aggregate billing cannot be split per project from repo evidence (DD-7). The
    middleware-count ≈ function-count equality _implies_ `ayokoding-www` dominates, but this step
    replaces inference with measurement — and step 0.5 destroys the ability to take it later.
- [ ] `[HUMAN]` Record the cycle-to-date Infrastructure Subtotal and the elapsed day count, so the
      monthly extrapolation is reproducible.
  - Acceptance: same evidence file states both numbers. Baseline for comparison: **$7.43 over ~4
    days as of 2026-07-30**.

### 0.2 Install the spend safety rail

- [ ] `[HUMAN]` Team → Settings → Billing → **Spend Management**: enable it, set the spend amount,
      and explicitly enable **"Pause production deployment"** (off by default; requires typing the
      team name to confirm).
  - Set the amount **below** the true ceiling — checks run only every few minutes, so spend can
    overshoot. Recommended: **$10**, giving a hard stop well inside the $20 credit.
  - Acceptance: the Spend Management panel shows a configured amount **and** the pause action
    enabled. Falsifiable both ways: before this step no amount is set and no pause action exists;
    after it, both are visible. Note the threshold governs **metered usage only** — not the $20 seat
    fee.

### 0.3 Migrate off legacy billing (DD-3)

- [ ] `[HUMAN]` For each project with functions, Project → Settings → Functions → enable **Fluid
      Compute**. Then trigger a redeploy so the setting takes effect.
  - Acceptance: after the next cycle's first usage appears, the dashboard reports **Active CPU** and
    **Provisioned Memory** line items and **no** "Function Duration (GB-Hrs)" line. Falsifiable both
    ways: today the reverse is true, which is precisely the diagnostic that identified legacy billing.

### 0.4 Enable the free firewall rulesets (DD-2)

- [ ] `[HUMAN]` Firewall → Managed Rulesets: set **Bot Protection** to active (from its default
      "Off") and **AI Bots** to **deny** (from its default "Allow"), for the public sites.
  - Acceptance: both rulesets show as active/deny in the dashboard.
- [ ] `[HUMAN]` **Mandatory indexability smoke-test** — documentation does not confirm that verified
      crawlers such as Googlebot are auto-allowlisted, so verify rather than assume:
      fetch a content page with a Googlebot user-agent and confirm a 200 with real HTML (not a
      challenge page), and confirm `robots.txt` and `sitemap.xml` still resolve.
  - Acceptance: the Googlebot-UA fetch returns 200 with page content. Falsifiable both ways: a
    challenge interstitial or a non-200 fails this check and triggers the rollback below.
  - **Rollback if it fails**: set Bot Protection back to "Off" (single toggle, no deploy). Record the
    outcome in the evidence file either way.

### 0.5 Disable Observability Plus (DD-1) — only after 0.1 is committed

- [ ] `[HUMAN]` Team → Settings → Billing → Observability Plus: disable team-wide.
  - Acceptance: the Observability Events line stops accruing in the next cycle. Removes a measured
    ~$10/month.
  - Precondition: step 0.1's evidence file is committed. Do not proceed otherwise.

### 0.6 Resolve the blocking middleware question empirically

- [ ] `[AI]` Determine whether `middleware.ts` still executes on Next.js 16.2.6, because sources
      conflict and a silent no-op is worse than a build error:
      `curl -sS -o /dev/null -D - https://www.ayokoding.com/ | head -20`
  - Acceptance: record whether a 307 to `/en` is returned. **If the redirect fires**, middleware is
    live and Phase 3 must replace it before deleting it. **If it does not fire**, middleware is
    already a silent no-op — Phase 3 becomes a pure cleanup, and the `/` → `/en` redirect is being
    served by something else (identify what before changing anything).
  - Falsifiable both ways: the two outcomes lead to materially different Phase 3 work, so this is
    not a formality.
- [ ] `[AI]` Record the finding and its consequence in
      `evidence/middleware-runtime-behaviour.md`.

### 0.7 Repo baseline

- [ ] `[AI]` `npm install` and `npm run doctor -- --fix` in the primary checkout.
- [ ] `[AI]` Build `apps/ayokoding-www` and record the prerendered route count:
      `nx build ayokoding-www && jq '.routes | length' apps/ayokoding-www/.next/prerender-manifest.json`
  - Acceptance: returns **4** (the documented pre-fix baseline). If it returns anything else, stop —
    the premise of the plan has changed and the analysis must be redone.
- [ ] `[AI]` Build `apps/wahidyankf-www` and record its route table.
  - Acceptance: three routes show `ƒ` (`/`, `/cv`, `/personal-projects`).
- [ ] `[AI]` Resolve preexisting failures in scope before any plan work begins.

### Phase 0 Gate

- [ ] `[HUMAN]` Spend Management configured **with** the pause action enabled.
- [ ] `[HUMAN]` Fluid Compute enabled and redeployed.
- [ ] `[HUMAN]` Bot Protection active, AI Bots denying, **and** the indexability smoke-test passed
      (or the rollback applied and recorded).
- [ ] `[HUMAN]` Observability Plus disabled, with the per-project baseline committed beforehand.
- [ ] `[AI]` Middleware runtime behaviour determined and recorded.
- [ ] `[AI]` Both baseline builds recorded: 4 prerendered routes, 3 dynamic wahidyankf routes.
- [ ] `[AI]` No PR opened in this phase.

> **Pause Safety**: this phase is a safe stop and is independently valuable — the platform changes
> alone are projected to cut roughly $10 (Observability) plus a large share of the $36 Function
> Duration line (Fluid Compute), with zero code risk. To resume: start Phase 1 in Unit 1's worktree.

---

## Phase 1: `apps/ayokoding-www` — Cause A, promote the locale layout

Highest-leverage single change in the plan. Isolated in its own phase because its blast radius is
every page on the site.

- [ ] `[AI]` **RED** — add a failing assertion that content routes are prerendered.
  - File: `apps/ayokoding-www/test/unit/build-output/prerender-coverage.test.ts` (new)
  - Command: `nx run ayokoding-www:test:unit`
  - Acceptance: the test asserts the prerendered route count is `>= 2000` and **fails** against the
    current build output (which has 4).
- [ ] `[AI]` **GREEN** — promote the locale layout and delete the root layout.
  - Delete `apps/ayokoding-www/src/app/layout.tsx` **entirely**. If it remains it stays the root
    layout, and nested layouts may not render `<html>`/`<body>`.
  - Move its contents into `apps/ayokoding-www/src/app/[locale]/layout.tsx`, rendering
    `<html lang={(await params).locale}>` and `<body>`. Remove the `headers()` import and the
    `x-pathname` read; the locale now comes from the route segment.
  - Preserve everything else the old root layout rendered, including the Google Analytics tags.
  - Command: `nx build ayokoding-www`
  - Acceptance: build exits 0 and
    `jq '.routes | length' apps/ayokoding-www/.next/prerender-manifest.json` returns `>= 2000`
    (was `4`).
- [ ] `[AI]` **REFACTOR** — confirm no other dynamic-API read remains in a layout.
  - Command: `grep -rn "headers()\|cookies()\|draftMode()\|noStore()\|connection()" apps/ayokoding-www/src --exclude-dir=node_modules`
  - Acceptance: zero hits in any `layout.tsx`. Note: use `--exclude-dir`, never `--glob`, and never
    `-L` — `grep` here routes to UGREP.
- [ ] `[AI]` Verify the `lang` attribute for both locales in the built output.
  - Acceptance: the prerendered English page contains `lang="en"` and the Indonesian page
    `lang="id"`. Falsifiable both ways: a wrong or missing `lang` fails.

**Gherkin (binds) →** "Content pages are statically prerendered and CDN-cached" and "The document
language still reflects the locale" — see [prd.md](./prd.md).

- [ ] `[AI]` Write the companion feature file under
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/`.

### Phase 1 Gate

- [ ] `[AI]` `apps/ayokoding-www/src/app/layout.tsx` no longer exists: `test ! -f` exits 0.
- [ ] `[AI]` Prerendered route count `>= 2000` (was 4).
- [ ] `[AI]` `nx run ayokoding-www:test:quick`, `typecheck`, and `lint` all exit 0.
- [ ] `[AI]` Draft PR opened for Unit 1.

> **Pause Safety**: safe to stop. The site is statically generated and functional. Rollback is a
> single revert commit restoring `app/layout.tsx`.

---

## Phase 2: `apps/ayokoding-www` — Cause B, move `?path=` client-side

The client-side equivalent **already ships**: `src/features/course-paths/shell/sidebar-host.tsx:36`
resolves `?path=` via `useSearchParams()` today. This phase removes the redundant server-side read.

- [ ] `[AI]` **RED** — assert the content catch-all is not dynamically rendered.
  - Command: `nx build ayokoding-www`
  - Acceptance: a test or build-output assertion fails while `[...slug]` still reads `searchParams`.
- [ ] `[AI]` **GREEN** — remove the `searchParams` prop.
  - File: `apps/ayokoding-www/src/app/[locale]/(content)/[...slug]/page.tsx` — drop the
    `searchParams` type member (line ~94) and the `await searchParams` read (line ~365).
  - Move any remaining `?path=`-dependent rendering into a client component behind `<Suspense>`,
    mirroring `tools/ai-benchmark/page.tsx`'s existing shape. Reuse `sidebar-host.tsx`'s resolution
    rather than duplicating it.
  - Command: `nx build ayokoding-www`
  - Acceptance: build exits 0 **and** the route table shows `●`/`○` for the content catch-all, not
    `ƒ`. A `next build` is mandatory here — dev mode hides a missing `<Suspense>` boundary, and a
    production build fails outright without one.
- [ ] `[AI]` **REFACTOR** — drop the now-vacuous `learn/paths/**` dynamic carve-out at
      `[...slug]/page.tsx:83` if it is still inert.
  - Note: `src/features/course-paths/manifests/` currently contains exactly one file, `README.md`, so
    `loadManifests()` returns `[]` on every request. Verify this still holds before removing;
    the sibling AI-benchmark plan does not add manifests, but confirm rather than assume.
  - Acceptance: state the manifest file count in the commit message; remove the carve-out only if it
    is zero.
- [ ] `[AI]` Verify `?path=` behaviour end-to-end against a real path context.

**Gherkin (binds) →** "Course-path context survives the move to client-side resolution".

- [ ] `[AI]` Write the companion feature file.

### Phase 2 Gate

- [ ] `[AI]` No `searchParams` read remains in any `apps/ayokoding-www` page:
      `grep -rn "await searchParams" apps/ayokoding-www/src --exclude-dir=node_modules` returns zero
      hits outside tests.
- [ ] `[AI]` Content catch-all is `●`/`○` in the route table, not `ƒ`.
- [ ] `[AI]` `test:quick`, `typecheck`, `lint` exit 0.

> **Pause Safety**: safe to stop. Both root causes are fixed and the site is fully static.

---

## Phase 3: `apps/ayokoding-www` — eliminate the middleware

Branch on Phase 0.6's finding. With Cause A fixed, nothing reads `x-pathname`, so the middleware's
only hot-path work is dead.

- [ ] `[AI]` **RED** — assert both redirects still work with middleware removed.
  - Acceptance: a test covering `/` → `/en` and uppercase-locale normalisation fails before the
    config redirects are added.
- [ ] `[AI]` **GREEN** — move both redirects into `apps/ayokoding-www/next.config.ts` `redirects()`.
  - `/` → `/en`, and the uppercase-locale variants. `path-to-regexp` is case-**sensitive** and cannot
    lowercase a captured parameter, so enumerate the finite variants literally for both locales
    (`/EN`, `/En`, `/eN`, plus their `/:path*` forms, and the same for `id`).
  - Append to the existing `redirects()` array — do **not** modify the 74 existing rules.
  - Config redirects are evaluated **before** middleware in Next.js's routing order, so behaviour is
    preserved.
  - Acceptance: `curl -sS -o /dev/null -D - <deploy-url>/ | grep -i location` shows `/en`, and the
    uppercase variants return 308 to lowercase. Falsifiable both ways: removing a rule breaks its URL.
- [ ] `[AI]` **REFACTOR** — delete `src/middleware.ts` and prune
      `src/features/i18n/shell/middleware.ts` to whatever pure helpers remain in use.
  - Acceptance: `test ! -f apps/ayokoding-www/src/middleware.ts` exits 0, and the build emits no
    middleware bundle (`.next/server/middleware-manifest.json` has no matcher for this app).
  - Note the secondary benefit: Vercel documents that middleware can accrue **Fast Origin Transfer
    twice** for a single function request, so this also trims that line item.
- [ ] `[AI]` If any middleware must survive for a reason discovered in Phase 0.6, migrate it to
      `proxy.ts` with the codemod `npx @next/codemod@canary middleware-to-proxy .` rather than
      leaving a deprecated `middleware.ts` whose runtime behaviour on 16.2.6 is unresolved.

**Gherkin (binds) →** "Locale entry redirects are preserved without middleware".

- [ ] `[AI]` Write the companion feature file.

### Phase 3 Gate

- [ ] `[AI]` No middleware file remains (or the surviving one is `proxy.ts`, deliberately).
- [ ] `[AI]` Both redirects verified live against a preview deployment.
- [ ] `[AI]` `test:quick`, `typecheck`, `lint` exit 0.

> **Pause Safety**: safe to stop. Middleware invocations (~$5/month at the measured rate) are gone.

---

## Phase 4: `apps/ayokoding-www` — bundle and cold-start hygiene

- [ ] `[AI]` Scope `outputFileTracingIncludes` per route instead of `"/**"`.
  - File: `apps/ayokoding-www/next.config.ts:25-27`
  - Acceptance: the `api/trpc` trace no longer includes the content tree. Measure with
    `jq '[.files[] | select(startswith("content/"))] | length' apps/ayokoding-www/.next/server/app/api/trpc/\[trpc\]/route.js.nft.json`
    — was **7,515**, must drop substantially. Falsifiable both ways.
- [ ] `[AI]` Wrap `getBySlug` in `React.cache()` to collapse the double per-request call
      (`[...slug]/page.tsx:130` in `generateMetadata` and `:339` in the body).
  - File: `apps/ayokoding-www/src/features/content/shell/service.ts`
  - Acceptance: an instrumented unit test shows one underlying read per render pass, not two.
    `React.cache()` dedupes **within** a render pass only, which is exactly the scope needed.
- [ ] `[AI]` Evaluate `output: "standalone"` (`next.config.ts:21`). It is dead configuration on
      Vercel but **is required by this app's Dockerfile** — do not delete it blindly.
  - Acceptance: whatever is decided, the Docker build path still succeeds. Record the decision.
- [ ] `[AI]` Confirm the sibling AI-benchmark route stays static.
  - `src/app/[locale]/tools/ai-benchmark/page.tsx` already wraps client content in `<Suspense>` with
    `useSearchParams()` in `benchmark-content.tsx:18`, so its `sortOpus`/`sortSonnet`/`sortLight`/
    `sortUnrated` query state is compliant. Verify this still holds after that plan merges.
  - Acceptance: the tools routes appear as `○`/`●` in the route table, not `ƒ`.

### Phase 4 Gate

- [ ] `[AI]` Content files traced into the tRPC function bundle substantially reduced from 7,515.
- [ ] `[AI]` `getBySlug` executes once per render pass.
- [ ] `[AI]` Tools routes confirmed static.
- [ ] `[AI]` Full local quality gate green: `typecheck`, `lint`, `test:quick`, `specs:coverage`.
- [ ] `[AI]` **Unit 1 delivery boundary** — PR-Review Maker→Fixer Cycle (3 CI-gated cycles), then
      `[AI]` merge once all five hardened preconditions hold.
- [ ] `[AI]` Deploy to `prod-ayokoding-www` and verify live: a repeat request to a content page
      returns `x-vercel-cache: HIT` (was `MISS`).

> **Pause Safety**: safe to stop. Unit 1 — the 65% line item — is fully delivered and deployed.

---

## Phase 5: `apps/wahidyankf-www` — static conversion and SEO files (Unit 2)

Independent of Unit 1; runs in parallel in its own worktree.

- [ ] `[AI]` **RED** — assert the three routes are static.
  - Command: `nx build wahidyankf-www`
  - Acceptance: an assertion on the route table fails while `/`, `/cv`, `/personal-projects` are `ƒ`.
- [ ] `[AI]` **GREEN** — remove the `searchParams` props and read the query client-side.
  - Files: `src/app/page.tsx:3-4`, `src/app/cv/page.tsx:10-11`,
    `src/app/personal-projects/page.tsx:10-11` — drop the prop.
  - Read `useSearchParams()` inside the already-`"use client"` consumers
    (`HomeContent.tsx:29-31`, `CvContent.tsx:477-484`, `PersonalProjectsContent.tsx:21-27`), each
    wrapped in `<Suspense>`. These components already only use the value to seed `useState`, so this
    is a prop swap, not a rewrite.
  - Command: `nx build wahidyankf-www`
  - Acceptance: all three routes show `○` in the route table (were `ƒ`). The production build fails
    outright if a `<Suspense>` boundary is missing, so a passing build is real evidence.
- [ ] `[AI]` **REFACTOR** — add `src/app/robots.ts` and `src/app/sitemap.ts` (neither exists today),
      modelled on `apps/ose-www/src/app/robots.ts` and its `sitemap-builder.ts`.
  - Acceptance: both routes prerender (`○` in the route table) and `robots.txt` names the sitemap.
    Falsifiable both ways: before this step, `test -f` on either file exits non-zero.
- [ ] `[AI]` Fix the 404 `og-image.jpg` referenced at `src/app/layout.tsx:39,51` — either ship the
      asset or remove the reference.
  - Acceptance: no metadata field points at a URL that 404s.
- [ ] `[AI]` Verify a shared filtered URL still works: opening `/cv?search=<term>` pre-fills the
      search box and filters results.

**Gherkin (binds) →** "Search-filtered portfolio routes are static yet still filterable".

- [ ] `[AI]` Locate the existing `specs/` path for `wahidyankf-www` (do not invent one) and write the
      companion feature file there.

### Phase 5 Gate

- [ ] `[AI]` Zero `ƒ` routes in the `wahidyankf-www` route table (was 3).
- [ ] `[AI]` `robots.ts` and `sitemap.ts` exist and prerender.
- [ ] `[AI]` `typecheck`, `lint`, `test:quick`, `specs:coverage` exit 0.
- [ ] `[AI]` **Unit 2 delivery boundary** — review cycle, then `[AI]` merge; deploy to
      `prod-wahidyankf-www` and confirm `x-vercel-cache: HIT` on a repeat request.

> **Pause Safety**: safe to stop. Unit 2 is self-contained.

---

## Phase 6: Secondary waste cleanups (Unit 3)

Independent of Units 1 and 2.

- [ ] `[AI]` Delete the 9 inert `export const dynamic = "force-dynamic"` lines in
      `apps/organiclever-app-web` — line 3 of `src/app/app/layout.tsx` and of the `home`, `history`,
      `progress`, `settings`, `routines/edit`, `workout`, and `workout/finish` pages.
  - These are no-ops today because every one of those files is `"use client"`, so Next.js already
    prerenders them as `○`. They are a latent cost landmine if any file is later converted to a
    server component.
  - Acceptance: `grep -rn "force-dynamic" apps/organiclever-app-web/src --exclude-dir=node_modules`
    returns exactly **one** hit — `src/app/system/status/be/page.tsx`, which is a genuine server
    component and keeps it. Falsifiable both ways: returns 10 before, 1 after.
  - Acceptance: the route table is unchanged (all still `○`), proving the directives were inert.
- [ ] `[AI]` Make `apps/organiclever-app-web/src/app/system/status/be/page.tsx` non-indexable.
  - It is a genuinely dynamic server component that `fetch`es a backend health endpoint with a 3s
    `AbortSignal.timeout` (line 15) — worst case 3s of billed function time per crawler hit, and it
    is currently crawlable.
  - Add `robots: { index: false }` metadata (server-side, so crawlers that do not run JS see it).
  - Acceptance: the rendered page emits a `noindex` directive in its HTML, not via client JS.
- [ ] `[AI]` Gate the daily Storybook rebuild.
  - `.github/workflows/web-ui-build-deploy-prod.yml:5` schedules `cron: "0 0 * * *"` and line 36
    force-pushes unconditionally, while `libs/web-ui/vercel.json` has no `ignoreCommand` — so Vercel
    rebuilds Storybook every single day whether or not `libs/web-ui` changed.
  - Gate it on a `libs/web-ui/` diff, mirroring `_reusable-www-test-local-deploy.yml:112,122`, and
    add an `ignoreCommand` to `libs/web-ui/vercel.json`.
  - Acceptance: the workflow has a change-detection step guarding the push, and the `vercel.json`
    has an `ignoreCommand`. Falsifiable both ways: neither exists today.
- [ ] `[HUMAN]` Fix the `ayokoding.com` → `www.ayokoding.com` redirect chain, which currently
      **downgrades HTTPS to HTTP** mid-chain (`301` to `http://www…`, then `308` to `https://www…`).
  - This is a Vercel domain/DNS setting, not a repo change. Two extra edge round trips plus a
    security smell.
  - Acceptance: `curl -sS -o /dev/null -D - https://ayokoding.com/` shows a single redirect straight
    to `https://www.ayokoding.com/`, with no `http://` hop.

### Phase 6 Gate

- [ ] `[AI]` Exactly one `force-dynamic` remains in `organiclever-app-web`, and route tables unchanged.
- [ ] `[AI]` `/system/status/be` emits a server-rendered `noindex`.
- [ ] `[AI]` Storybook deploy gated in both the workflow and `vercel.json`.
- [ ] `[HUMAN]` Domain redirect chain no longer downgrades to HTTP.
- [ ] `[AI]` `typecheck`, `lint`, `test:quick` exit 0; workflow lints clean (actionlint).
- [ ] `[AI]` **Unit 3 delivery boundary** — review cycle, then `[AI]` merge.

> **Pause Safety**: safe to stop. Unit 3 is pure waste removal.

---

## Phase 7: Steady-state measurement against the budget

- [ ] `[HUMAN]` After a **full billing cycle** has elapsed with all three units merged and deployed,
      read Vercel → Usage for the completed cycle and record every line item.
  - Acceptance: the recorded **Infrastructure Subtotal for the full cycle is under $20.00** (hard
    requirement), and the report states whether it is also under $10.00 (stretch).
  - Also record: the on-demand charge above the subscription, which must be **$0.00**.
- [ ] `[HUMAN]` Confirm the invoice total equals the $20 subscription with no additional line.
- [ ] `[AI]` Compare against Phase 0.1's per-project baseline and record actual versus projected
      savings per action, marking which figures were measured and which were estimated.
  - Projected path from the ~$57/month gross baseline:

    | Action                            | Line item affected                    | Projected effect                    | Confidence                                                                 |
    | --------------------------------- | ------------------------------------- | ----------------------------------- | -------------------------------------------------------------------------- |
    | Disable Observability Plus        | Observability Events                  | −$10/mo                             | **Measured rate**, certain                                                 |
    | Eliminate middleware              | Edge Middleware Invocations           | −$5/mo                              | **Measured rate**, certain                                                 |
    | Static conversion (ayokoding-www) | Function Duration + Invocations       | −$30/mo or more                     | Estimated; the 65% line item collapses when ~2,068 pages become CDN-served |
    | Fluid Compute migration           | Function Duration on whatever remains | roughly halves the residue          | Estimated from Vercel's own comparison                                     |
    | Bot/AI-bot blocking               | Invocations + Duration                | unknown but positive                | Unquantified — depends on the crawler share, which Phase 0.1 measures      |
    | wahidyankf-www static             | Function Duration + Invocations       | small but complete for that project | Estimated                                                                  |
    | **Projected total**               | —                                     | **~$2–4/mo gross**                  | Comfortably inside both targets                                            |

- [ ] `[AI]` If the hard requirement is missed, open a follow-up plan rather than widening this one.

### Phase 7 Gate

- [ ] `[HUMAN]` Full-cycle gross metered usage **< $20.00**, on-demand charge **$0.00**.
- [ ] `[AI]` Actual-versus-projected comparison committed to `evidence/`.

> **Pause Safety**: the objective is either met and verified, or a follow-up is scoped. Safe to stop.

---

## Phase 8: Knowledge Capture

- [ ] `[AI]` Triage `learnings.md` — every entry either finds a home (a convention, a doc, an idea
      two-pager) or is explicitly discarded with a reason.
- [ ] `[AI]` Candidate homes to consider, based on what this plan uncovered:
  - The diagnostic that legacy-vs-Fluid billing is readable from line-item **names** alone.
  - The rule that a dynamic API in a root layout forfeits static generation for the entire app, and
    that the locale-segment root layout is the documented i18n fix.
  - That `next build` — never a dev-server check — is the only valid evidence for a `<Suspense>`
    boundary around `useSearchParams()`.
  - That Vercel's WAF blocks **before** the billing meter, making the free rulesets a cost control.
  - That Spend Management's pause action is off by default and lags by minutes.
- [ ] `[AI]` Fold anything cross-cutting into the existing
      [`nx-affected-cross-worktree-contamination`](../../ideas/nx-affected-cross-worktree-contamination.md)
      two-pager if it belongs there rather than creating a duplicate.

### Phase 8 Gate

- [ ] `[AI]` `learnings.md` fully triaged, with no untriaged entries remaining.

> **Pause Safety**: safe to stop. All delivery is complete; only archival remains.

---

## Phase 9: Plan archival, final push, and merge

- [ ] `[AI]` `git mv plans/in-progress/vercel-function-cost-reduction plans/done/YYYY-MM-DD__vercel-function-cost-reduction`
      using the actual completion date.
- [ ] `[AI]` Update `plans/done/README.md` and `plans/in-progress/README.md` indexes.
- [ ] `[AI]` Commit the archival move on the PR branch and push **before** the merge, per the
      Delivery Mode convention's Archival-in-PR requirement.
- [ ] `[AI]` `[AI]` merge once all five hardened preconditions hold.
- [ ] `[AI]` Fast-forward local `main` after the final push, so the base worktree does not silently
      diverge.
- [ ] `[AI]` Remove all three worktrees after confirming each is clean and fully merged.

### Phase 9 Gate

- [ ] `[AI]` Plan folder lives under `plans/done/` with a date prefix.
- [ ] `[AI]` All three PRs merged; CI green on `main`.
- [ ] `[AI]` All three worktrees removed; local `main` fast-forwarded.

> **Pause Safety**: plan complete.
