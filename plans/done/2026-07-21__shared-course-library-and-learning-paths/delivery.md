# Delivery Checklist — Fundamentally Strong Shared Course Library, Four Paths

This checklist delivers a **shared course library + four composing paths** over the existing ayokoding
`/c/[...slug]` content route. A **course** is a standalone, path-neutral building block served at
`/en/c/learn/courses/<course-id>`; a **path** is an ordered manifest composing a curated subset of
course-ids, landing at `/en/c/learn/paths/<path-id>`. **Convergence is now a per-role property, not a
library-wide axiom (DD-22, amends DD-5)**: the three `software-engineer` paths converge on one shared
software-engineering deep-mastery endpoint; the fourth path converges on a **distinct AI-engineering**
endpoint:

1. `interview-ready/software-engineer` — experienced SWE re-entering the market: interview/job prep FIRST → production-effective → deeper.
2. `immediately-effective/software-engineer` — editor → one language → build a real app FIRST → then deepen.
3. `fundamentally-strong/software-engineer` — university-style: fundamentals/CS-theory FIRST → deeper.
4. `immediately-effective/software-engineer-to-ai-engineer` (fourth path, added 2026-07-20, DD-21–DD-28) — role-transition, immediately-effective arc: assumes an **already-working software engineer**; prerequisite software-engineer courses are **linked, not included** (DD-24); teaches **building** AI systems (models, agents, evals, inference serving), not driving them (`agentic-coding` stays a separate, unrelated axis, DD-21).

**Scope extension (2026-07-21, Phase 5A, DD-40–DD-45).** The checklist additionally revamps
**everything else** under `/{locale}/c/learn/`, so the section closes at **exactly three** structural
buckets — `paths/`, `courses/`, and a new **`legacy/`** bucket holding the six remaining `en/learn/`
domains (`software-engineering`, `artificial-intelligence`, `information-security`,
`personal-development`, `it-governance`, `business`; **1,148** `.md` [Repo-grounded]) — plus the
section's own two hub files (`_index.md`, `overview.md`). The relocation is a **prefix `git mv` that
rewrites no page**, covered by **per-domain 308 prefix rules** in a new
`apps/ayokoding-www/src/redirects/learn-three-bucket.ts`; a blanket `/en/c/learn/:path*` rule is
FORBIDDEN. Design, BEFORE/AFTER trees, and the URL-mapping table:
[tech-docs §Learn-Section IA](./tech-docs.md#learn-section-ia--the-three-bucket-model-scope-extension-2026-07-21).
**Six questions are OPEN** ([Q-A–Q-F](./tech-docs.md#open-questions--learn-section-scope-extension-unresolved));
Phase 5A executes each one's **recommended default** and names the alternative inline.

Navigation is **additive** — after re-homing, a reader can still browse the material **the old way**
(the legacy hand-curated, spiral-ordered `_index.md` section tree, re-pointed to the new course URLs)
IN ADDITION to the new way (`/en/c/learn/paths/<path-id>` path landings + `/en/c/learn/courses/<course-id>`
canonical course pages); both coexist (§5a, enforced in Phase 5).

Every course declares `prerequisites: [course-id, ...]` in its canonical metadata, forming a
**prerequisite DAG**; every path manifest is a valid prerequisite-consistent ordering/entry into that
DAG. The catalog is **127 courses** (121 software-engineer-role baseline + the fourth path's 6 net-new
AI-engineering courses, DD-28; zero merges among the original 121; course surgery — update/merge/split/
create — is now permitted subject to a four-path blast-radius statement per surgery, DD-28). The
course-ID + manifest schema, the path-aware-navigation UI design, and all four path orderings live in
[tech-docs.md](./tech-docs.md) and the [syllabus detail layer](./syllabus/README.md); the
UI-design-funnel and NEW-course specs live in [prd.md](./prd.md). The authoritative catalog baseline is
the tracked [Course Library Catalog](./tech-docs.md#course-library-catalog) (127-course total; the six
AI-engineering courses are catalogued there by name only until Group F authors them — see
[Design Decisions DD-28](./tech-docs.md#design-decisions) — Phase 7 below adds their table rows). It was
originally derived from a gitignored `local-temp/` scratch file, which must not be relied on during
execution.

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). Each gate covers the phase's
> **content/code correctness** (tests, checkers, build) and its **integration** (draft PR opened,
> 3-cycle PR-Review, CI green, `[AI]` merge, `ayokoding-www` deployed). A phase is not complete until
> every gate check is green.

## Worktree

One **shared worktree** for the whole plan (one checkout, many branches, many PRs):

Worktree path: `worktrees/shared-course-library-and-learning-paths/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree shared-course-library-and-learning-paths
```

The plan-execution Step 0 gate enters this shared worktree by default: it auto-provisions from the
latest `origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this one shared worktree
(`git fetch origin && git checkout main && git pull && git checkout -b
shared-course-library-and-learning-paths/<phase-slug>`), authors its work there, commits, pushes that
branch, and opens **its own draft PR**.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each phase works in the shared worktree on its **own branch**, opens a **draft PR** against `main`,
runs the **PR-Review Maker→Fixer Cycle** (`pr-review-maker` / `pr-review-fixer`, 3 sequential
CI-gated cycles), flips the PR to ready, and `[AI]` **merges it automatically once all quality gates
are green** — then `[AI]` **deploys `ayokoding-www` to `prod-ayokoding-www` after every merge** (this
plan ships to ayokoding.com). See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)
and the [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).

> **DN-11 DECIDED — `[AI]` auto-merge (now the repo default)**: the repo's
> [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md) has `[AI]`
> merge the PR **by default** once its five hardened preconditions hold; a `[HUMAN]` merge gate is an
> explicit per-plan opt-in, and this plan does not opt in. When DN-11 was first recorded the protocol
> still defaulted to a `[HUMAN]` merge, so the maintainer authorized `[AI]` merge for this plan
> specifically (2026-07-18, in-session — modeled on the sibling plan
> `fundamentally-strong-software-engineer`'s own separately-recorded authorization) via two directives:
> (a) this plan uses the SAME delivery methods as the sibling plan, and (b) no maintainer permission is
> needed to merge a PR once it has passed 3 review cycles and the PR quality gate. The protocol has
> since been changed to match, so **DN-11 = AI-auto-merge** now simply confirms the repo default rather
> than deviating from it. The preconditions are unchanged either way — only the actor differs.

**Per-Phase Integration Protocol** (each phase's gate lists these as must-pass):

1. [AI] Sync the shared worktree to latest `origin/main` and branch:
   `git fetch origin && git checkout main && git pull && git checkout -b
shared-course-library-and-learning-paths/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `test:integration`, `test:e2e` where affected, `specs:behavior:coverage`, CI, the 3-cycle review) —
   `[AI]` auto-merge per DN-11.
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www` — a
   no-op redeploy for plan-side-only phases.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Group A (Phases 1–4)** is **serial** — each phase builds on the prior feature slice (schema →
  core → shell/route → landing/e2e). Group A is the **hard prerequisite** for every path.
- **interview-ready MVP (Phases 5–6)** is serial (re-home is a sync point; the manifest depends on the
  courses existing). Per **DD-27**, this MVP is now an **architecture smoke test only** — it ships
  against the topics already re-homed in Phase 5, with no NEW course authoring inside this group; the
  four interview-technique courses + `capstone-interview-loop` are **deferred** to Group E (Backfill,
  Band 9) so they never block the AI path's authoring start.
- **Legacy bucket (Phase 5A, Group L — scope extension, DD-40–DD-45)** runs immediately after the
  Phase 5 re-home and **before** the Phase 6 MVP manifest. It is **serial** and a single sync point:
  the six `git mv`s, the redirect module, and the two hub-file edits must land together (a live 308
  pointing at a not-yet-moved path, or a moved path with no 308, are both worse than either end
  state). It is placed after Phase 5 because the `courses/` bucket must already exist — otherwise
  `en/learn/` would transiently hold only `legacy/` — and before Phase 6 so the paths hub and every
  later manual verification see the final three-bucket shape rather than a hybrid one. It touches no
  file any other phase touches (the six relocated domains are outside the plan's course/path scope),
  so it neither blocks nor is blocked by Groups F/C/D/E beyond this ordering.
- **AI path (Phases 7–9, Group F — authoring priority #1, DD-27)** runs immediately after the MVP and
  ahead of Groups C/D. Phase 7's **six net-new AI courses** are content-independent (each writes only
  its own `courses/<id>/` subtree) and **pipeline concurrently** through review, bounded by the cap.
  Phase 8 (course-surgery scope contract) and Phase 9 (manifest + landing) are serial sync points.
- **immediately-effective manifest (Phase 10)** and **fundamentally-strong manifest (Phase 11)** are
  serial manifest+landing sync points authored over the currently-available library.
- **Backfill (Phase 12)** authors the 61 transferred topics + 10 remaining new courses + 8 remaining
  capstones (2 original + 6 DD-20 inter-topic capstones) + the **deferred 4 interview courses +
  `capstone-interview-loop`** (Band 9, DD-27) **natively**; these bodies are mutually content-independent
  and **pipeline concurrently** through review (bounded by the cap). Each landed band **grows** the
  affected manifests (append + re-run prerequisite-consistency + integrity) as a serial sync point —
  Bands 1–8 grow the three software-engineer-role manifests; Band 9 grows only `interview-ready` and
  `fundamentally-strong` (the two arcs whose ordering includes the interview-technique band per
  [tech-docs.md's path manifests](./tech-docs.md#path-manifests)); **Band 5 (plus Band 8 for
  `capstone-build-your-own-coding-agent`) additionally grows the fourth path's
  (`immediately-effective/software-engineer-to-ai-engineer`) manifest** from its Phase-9
  smoke-test-scoped six-course spine to its full **15-course** composition (DD-33) — the
  harness-cluster bodies these bands land are exactly the nine courses that manifest walks.
- **Finalization (Phases 13–17)** is serial.

**Path constants** (referenced throughout):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/c/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (thin path-landing anchors; served at `/en/c/learn/paths/<path-id>`)
- `<SE_OLD>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/` (legacy home of the 33 shipped topics + 4 existing capstones, incl. `capstone-solid-core` — the re-home source)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/` (standalone YAML data files, nested to mirror slash path ids — `<MANIFESTS><path-id>.yaml`)
- `<LEGACY>` = `apps/ayokoding-www/content/en/learn/legacy/` (**new bucket**, scope extension; served at `/en/c/learn/legacy/<domain>/…`)
- `<REDIR>` = `apps/ayokoding-www/src/redirects/`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- `<NAVSPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/` (existing domain — the three-bucket Gherkin lands beside `content-namespace-redirects.feature`)
- Path ids: `interview-ready/software-engineer`, `immediately-effective/software-engineer`, `fundamentally-strong/software-engineer`, `immediately-effective/software-engineer-to-ai-engineer` (fourth path, manifest at `<MANIFESTS>immediately-effective/software-engineer-to-ai-engineer.yaml`)

---

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_
>
> **No cross-plan precondition.** The sibling FS-SE plan is CLOSED
> (`plans/done/2026-07-19__fundamentally-strong-software-engineer/`) and its Passes 3–5 scope is
> absorbed here; there is **no "FS-SE must be DONE first" gate**. Topics 34–94 are authored NATIVE in
> Phase 10 (no legacy home, no re-home). Only the 33 shipped topics (1–33) + 4 existing capstones
> (incl. `capstone-solid-core`, per **DD-20**) live under `<SE_OLD>` and are re-homed in Phase 5.

- [ ] [AI] Enter/provision the worktree and install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build` and
      `npx nx run ayokoding-www:test:unit`
      — acceptance: all exit 0; record pass state.
- [ ] [AI] **Re-home source inventory (non-blocking snapshot)** — record the 33 shipped topics + 4
      existing capstones present under `<SE_OLD>` to `evidence/phase-0-snapshot.txt` via:
      `for s in just-enough-nvim just-enough-lua extending-neovim just-enough-python just-enough-bash version-control-and-git data-structures-and-algorithms-essentials advanced-algorithms object-oriented-programming-essentials object-oriented-design-and-patterns sql-essentials technical-communication just-enough-typescript frontend-essentials backend-essentials networking-essentials computer-science-foundations computer-architecture programming-paradigms functional-programming concurrency-and-parallelism advanced-networking advanced-sql-and-query-performance data-access-orms-and-query-builders build-your-own-orm-and-query-builder software-engineering-practices agentic-coding security-essentials software-testing debugging-and-profiling software-product-engineering engineering-management project-management capstone-forge-ready capstone-first-working-software capstone-full-stack-app capstone-solid-core; do test -d "<SE_OLD>$s" || echo "ABSENT $s"; done`
      — acceptance: snapshot committed. Any `ABSENT` line is recorded (not a hard stop) and reconciled
      against the catalog before Phase 5.
- [ ] [AI] Also snapshot the existing `content-url.ts` / `prev-next.tsx` / `breadcrumb.tsx` /
      `tree-builder.ts` behavior and the current `next.config.ts` locale set into
      `evidence/phase-0-snapshot.txt` — acceptance: snapshot committed.
- [ ] [AI] Confirm the twenty-three NEW slugs are absent (no collision) under `<SE_OLD>` and `<COURSES>`
      (fourteen new courses + nine new capstones: three original plus six **DD-20** inter-topic
      capstones):
      `for s in coding-interview take-home-and-live-coding system-design-interview behavioral-and-leadership-interviews capstone-interview-loop async-python-and-fastapi-services self-hosting-essentials browser-automation-with-cdp the-agent-loop agent-tools-and-mcp agent-context-and-memory agent-permissions-and-sandboxing agent-orchestration-subagents-and-observability capstone-build-your-own-coding-agent just-enough-cpp detection-engineering-and-siem-operations capstone-build-your-own-pentest-engine capstone-real-world-delivery capstone-secure-service capstone-data-pipeline capstone-concurrency-and-systems capstone-concurrency-showdown capstone-lead-at-altitude; do test -e "<SE_OLD>$s" && echo "EXISTS SE_OLD $s"; test -e "<COURSES>$s" && echo "EXISTS COURSES $s"; done`
      — acceptance: zero `EXISTS` lines.
- [ ] [AI] **Legacy-bucket source inventory (scope extension, DD-40)** — record the per-domain `.md`
      counts under `apps/ayokoding-www/content/en/learn/` to `evidence/phase-0-snapshot.txt` via:
      `for d in fundamentally-strong software-engineering artificial-intelligence information-security personal-development it-governance business; do printf '%s %s\n' "$d" "$(find apps/ayokoding-www/content/en/learn/$d -name '*.md' | wc -l)"; done`
      — acceptance: snapshot committed and matches the plan's stated baseline (563 / 979 / 55 / 51 /
      50 / 9 / 4; six relocated domains sum to **1,148**). A divergence is recorded and reconciled
      against [tech-docs §Ground-truth inventory](./tech-docs.md#ground-truth-inventory-measured-2026-07-21)
      before Phase 5A — it is not a hard stop here.
- [ ] [AI] **Legacy-bucket collision + `id` baseline check (scope extension)** —
      `test -e apps/ayokoding-www/content/en/learn/legacy && echo "EXISTS legacy"; test -e apps/ayokoding-www/src/redirects/learn-three-bucket.ts && echo "EXISTS module"; find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l`
      — acceptance: zero `EXISTS` lines (neither the bucket nor the redirect module exists yet), and
      the `id/belajar` count (**53** today) is recorded so the `en`-only scoping (DD-45) is verifiable
      as unchanged at archival.
- [ ] [AI] Confirm `learnings.md` scaffold exists in the plan folder — acceptance: file present with its H1.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] `ayokoding-www:build` + `test:unit` + `test:integration` baselines recorded green.
- [ ] [AI] Re-home source inventory + component snapshot committed to `evidence/phase-0-snapshot.txt`; all 23 new slugs absent.
- [ ] [AI] Legacy-bucket per-domain baseline (563 / 979 / 55 / 51 / 50 / 9 / 4) and the `id/belajar` count (53) recorded in `evidence/phase-0-snapshot.txt`; `<LEGACY>` and `<REDIR>learn-three-bucket.ts` confirmed absent.
- [ ] [AI] Draft PR opened; CI triggered; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      `ayokoding-www` deployed (no-op redeploy).

> **Pause Safety**: only the toolchain was verified and the current state snapshotted — no content or
> code changed. Safe to stop indefinitely. To resume: re-run the baselines.

---

## Group A — Architecture + path-aware navigation UI (hard prerequisite)

## Phase 1: UI design funnel + library/paths content homes + manifest & prerequisite schema

> _Suggested executor: `web-researcher` (R7 prior art) + `swe-developing-frontend-ui` skill for the
> funnel; `swe-typescript-dev` for the schema._

- [ ] [AI] **R5 survey** — read `libs/web-ui` component inventory + tokens + Storybook and the
      ayokoding app-shell + existing `sidebar-tree`/`breadcrumb`/`prev-next`/`section-card`
      [Repo-grounded] — plus `resizable-sidebar.tsx` and `app-shell/shell/mobile-nav.tsx`, the two
      existing hosts the selected Screen 3 Option B swaps content into — acceptance: net-new components
      (`PathCard`, `PathLanding`, `PathRail`, `PathBanner`, `PathCourseLinks`, `PrerequisiteList`) named
      in `tech-docs.md`; existing primitives to reuse listed, including the shipped `Sheet` drawer as
      the below-`md` rail host (so no new overlay pattern is introduced).
  - _Suggested executor: `swe-developing-frontend-ui` skill_
- [ ] [AI] **R7 prior art** — delegate to `web-researcher` a survey of how comparable platforms present
      a track/path over shared lessons **with prerequisites** (roadmap.sh, Exercism, freeCodeCamp,
      Coursera) — acceptance: cited findings folded into `prd.md` funnel notes; no `[Unverified]` claim.

### Hi-fi mockup matrix — 5 screens × 2 options × 3 viewports = 30 `.png`

> **This is a large render volume, so it is enumerated per asset rather than hidden behind one
> "render all mockups" checkbox.** 8 desktop renders (Screens 0-3) already exist on disk and were
> renamed to the `-desktop` suffix when the scheme was introduced; **16** more are produced here
> (Screens 0-3 × mobile + tablet) and **6** in Phase 5A (Screen 4 × 3 viewports). Naming scheme,
> render widths, and alt-text rules: [prd.md §Hi-fi asset matrix](./prd.md#hi-fi-asset-matrix-screen--option--viewport).
> Every file is `assets/<screen>-option-<a|b>-<mobile|tablet|desktop>.png`, rendered from
> `assets/src/<same-stem>.html` at **375 / 768 / 1280 px** — `.png` only, per the
> [UI Mockups convention](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope)
> (`.excalidraw.svg` and inline HTML+CSS are ruled out: GitHub strips styles and blocks Excalidraw fonts).

- [ ] [AI] **Verify the 8 existing desktop renders** carry the `-desktop` suffix and are still embedded
      — acceptance:
      `for s in landing-hero paths-hub path-landing course-path; do for o in a b; do test -f "assets/$s-option-$o-desktop.png" || echo "MISSING $s-$o"; done; done`
      prints nothing, AND
      `grep -o -- "assets/[a-z-]*option-[ab]-desktop.png" prd.md | sort -u | wc -l` returns **8**
      (falsifiable both ways: the pre-rename filenames had no `-desktop` segment, so the loop printed
      all eight and this count was **0**. Use the `grep -o … | sort -u` form, **not** a bare
      `grep -c -- "-desktop.png"` — that counts matching _lines_ including the prose in the asset-matrix
      section that merely names the convention, and already returns 9).
- [ ] [AI] Render `assets/landing-hero-option-a-mobile.png` from `assets/src/landing-hero-option-a-mobile.html` at 375 px — acceptance: file exists; single-column goal cards, no 2×2 grid.
- [ ] [AI] Render `assets/landing-hero-option-b-mobile.png` from `assets/src/landing-hero-option-b-mobile.html` at 375 px — acceptance: file exists.
- [ ] [AI] Render `assets/landing-hero-option-a-tablet.png` from `assets/src/landing-hero-option-a-tablet.html` at 768 px — acceptance: file exists; 2×2 grid visible (`md:grid-cols-2` active).
- [ ] [AI] Render `assets/landing-hero-option-b-tablet.png` from `assets/src/landing-hero-option-b-tablet.html` at 768 px — acceptance: file exists.
- [ ] [AI] Render `assets/paths-hub-option-a-mobile.png` from `assets/src/paths-hub-option-a-mobile.html` at 375 px — acceptance: file exists; four full-width cards stacked.
- [ ] [AI] Render `assets/paths-hub-option-b-mobile.png` from `assets/src/paths-hub-option-b-mobile.html` at 375 px — acceptance: file exists.
- [ ] [AI] Render `assets/paths-hub-option-a-tablet.png` from `assets/src/paths-hub-option-a-tablet.html` at 768 px — acceptance: file exists; 2×2 grid visible.
- [ ] [AI] Render `assets/paths-hub-option-b-tablet.png` from `assets/src/paths-hub-option-b-tablet.html` at 768 px — acceptance: file exists.
- [ ] [AI] Render `assets/path-landing-option-a-mobile.png` from `assets/src/path-landing-option-a-mobile.html` at 375 px — acceptance: file exists; phase headings inline (not sticky — sticky is `lg+` only).
- [ ] [AI] Render `assets/path-landing-option-b-mobile.png` from `assets/src/path-landing-option-b-mobile.html` at 375 px — acceptance: file exists.
- [ ] [AI] Render `assets/path-landing-option-a-tablet.png` from `assets/src/path-landing-option-a-tablet.html` at 768 px — acceptance: file exists; sidebar column present (`md:block` active).
- [ ] [AI] Render `assets/path-landing-option-b-tablet.png` from `assets/src/path-landing-option-b-tablet.html` at 768 px — acceptance: file exists.
- [ ] [AI] Render `assets/course-path-option-a-mobile.png` from `assets/src/course-path-option-a-mobile.html` at 375 px — acceptance: file exists; banner strip full-width, no rail, `PrevNext` stacked.
- [ ] [AI] Render `assets/course-path-option-b-mobile.png` **showing the collapsed rail plus the opened left drawer** (the selected design's mobile form) from `assets/src/course-path-option-b-mobile.html` at 375 px — acceptance: file exists; the drawer's ordered course list and the banner disclosure trigger are both visible.
- [ ] [AI] Render `assets/course-path-option-a-tablet.png` from `assets/src/course-path-option-a-tablet.html` at 768 px — acceptance: file exists; generic content-tree sidebar visible beside the banner.
- [ ] [AI] Render `assets/course-path-option-b-tablet.png` **showing the rail truncated at the 15 % width floor (~115 px)** from `assets/src/course-path-option-b-tablet.html` at 768 px — acceptance: file exists; rows render as number + ellipsised title, phase separators are bare rules with no labels.
- [ ] [AI] **Embed all 16 new renders in `prd.md`** under their screen's "Hi-fi finalists" block, each
      with viewport-specific descriptive alt text that names what differs **at that width** (never a
      copy of the desktop alt text) — acceptance:
      `grep -o -- "assets/[a-z-]*option-[ab]-mobile.png" prd.md | sort -u | wc -l` returns **8** and the
      same form with `-tablet.png` returns **8** (both return **0** today, verified — use the
      `grep -o … | sort -u` form, not `grep -c`, which counts lines and would be inflated by prose that
      merely names the convention), AND
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate`
      resolves every new `![]()` target.
- [ ] [AI] **Update each screen's selection line to name its selected finalist file** — acceptance:
      `grep -cE "Selected: Option [AB] .*" prd.md` returns **≥ 3**, and Screen 3's selection line names
      **Option B** — `grep -c "Selected: Option B — Left path rail" prd.md` returns **1** (returns
      **0** in the pre-Screen-3-reselection state, verified).
      **The bare `grep -c "Selected:" prd.md` MUST NOT be used** as the acceptance: it is already
      non-zero in the unexecuted plan (the authored design-intent selections plus a meta-reference), so
      it is pre-satisfied and contributes zero discriminating power. The artifacts and the specific
      selected-option strings are the deliverable, so they are what the acceptance tests.
- [ ] [AI] **Library + paths content homes** — create `<COURSES>_index.md` (library landing, weight +
      title) and `<PATHS>_index.md` (paths hub / choose-a-path landing whose 2×2-grid layout has room
      for **all four** paths, populated as each ships) mirroring an existing section `_index.md` —
      acceptance: `test -f <COURSES>_index.md` and `test -f <PATHS>_index.md`; build green.
- [ ] [AI] **Course-prerequisite metadata contract** — document the canonical course metadata field
      `prerequisites: [course-id, ...]` (declared in each course `_index.md` frontmatter) in
      [tech-docs §Prerequisite DAG](./tech-docs.md#prerequisite-dag-illustrative-excerpt) — acceptance: contract documented;
      the field is the single source of truth for the prerequisite DAG surfaced on each course page.
- [ ] [AI] **Manifest data-file schema definition** — write the `PathManifest` zod schema (`pathId`,
      `title`, `description`, `courseOrder[]`, optional per-course `framing`) into `<FEAT>core/schemas.ts`,
      matching the standalone YAML data-file format (NOT `_index.md` frontmatter), per
      [tech-docs §Path = ordered manifest](./tech-docs.md#path--ordered-manifest-manifest-format)
      — acceptance: schema compiles (`npx nx run ayokoding-www:typecheck` exits 0).
- [ ] [AI] **Manifest data-file directory** — create `<MANIFESTS>` (the standalone-data-file home,
      source of truth) with a `README.md` note that nested `<path-id>.yaml` files land here in Phase 6
      (interview-ready MVP) and Phases 9–11 (the AI, immediately-effective, and fundamentally-strong
      manifests — the latter three each grown further as Phase 12 backfill lands) — acceptance:
      `test -d <MANIFESTS>` and `test -f <MANIFESTS>README.md`.

### Phase 1 Gate

- [ ] [AI] Funnel finalists (2×2-grid four-path hub + prerequisite display) + selections + rationale present in `prd.md`; assets resolve.
- [ ] [AI] **24 of the 30 hi-fi renders exist** (Screens 0-3 × 2 options × 3 viewports; Screen 4's remaining 6 land in Phase 5A) — `find assets -name '*-option-*-*.png' | wc -l` returns **24** (returns **8** before this phase, verified), and every one is embedded in `prd.md` with viewport-specific alt text.
- [ ] [AI] Screen 3's selection reads **Option B — Left path rail**, and no surviving text in `prd.md`, `tech-docs.md`, or `delivery.md` asserts that every screen selected Option A.
- [ ] [AI] `<COURSES>_index.md` + `<PATHS>_index.md` created; prerequisite metadata contract documented; `PathManifest` schema compiles; `<MANIFESTS>` exists.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:typecheck` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the design is fixed and the empty library/paths homes + manifest/prerequisite
> schema exist; no bodies moved, no nav behavior changed. Safe to stop. To resume: re-run `:typecheck`.

---

## Phase 2: `course-paths` core (pure) — TDD + specs RED

> _Suggested executor: `swe-typescript-dev` (core logic) + `specs-maker` (Gherkin)._

- [ ] [AI] **Specs RED** — author the `course-paths` Gherkin companion under `<SPECS>` (one `.feature`
      per behavior: path-order nav, breadcrumb, canonical fallback, invalid-path fallback, omitted
      course, manifest integrity, prerequisite display, prerequisite-consistent ordering) from
      [prd.md §Acceptance Criteria](./prd.md#acceptance-criteria-gherkin) + a `<SPECS>README.md`
      — acceptance: `npx nx run ayokoding-www:specs:behavior:coverage` fails (no step bindings yet).
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED** — write failing unit tests in `<FEAT>core/path-nav.test.ts` for
      `resolvePathNav(manifest, courseId)` (prev/next at both boundaries; course-missing → nulls) and
      `parsePathContext(searchParams, manifests)` (valid → pathId; unknown → null; absent → null)
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: tests fail (functions undefined).

  **Gherkin (underpins) →** "Prev and next follow the active path's order"; "A course omitted from a
  path shows no path nav for that path"; "A course deep-linked without path context renders the
  canonical view"; "An invalid path context falls back to the canonical view"

  ```gherkin
  Scenario: Prev and next follow the active path's order
    Given a reader is on a course with an active path context
    When the reader reads the prev/next navigation
    Then prev and next are the neighboring courses in that path's manifest
    And both links preserve the path context query parameter

  Scenario: A course omitted from a path shows no path nav for that path
    Given a course is not listed in a given path's manifest
    When a reader opens that course with that path's context
    Then the course renders the canonical standalone view
    And neither the path rail nor the path banner is shown for that path

  Scenario: The path rail shows the whole ordered arc beside a course at desktop width
    Given a reader opens a course in path context on a desktop-width viewport
    When the page renders
    Then the left rail lists that path's courses in manifest order with the current course marked
    And the current course is distinguished by a marker and weight, not by colour alone
    And the rail offers a link back to the full path and to the whole course library

  Scenario: The path rail collapses into the existing navigation drawer on a phone
    Given a reader opens a course in path context on a phone-width viewport
    When they activate the path readout's "open path course list" control
    Then the existing left navigation drawer opens showing that path's ordered courses
    And focus moves into the drawer and returns to the control when the drawer is dismissed

  Scenario: A course opened without path context renders the generic sidebar unchanged
    Given a reader opens a canonical course URL with no path context query parameter
    When the page renders
    Then the left sidebar shows the generic content tree exactly as it does elsewhere in the site
    And no path rail, path readout, or path breadcrumb segment appears

  Scenario: A course deep-linked without path context renders the canonical view
    Given a reader opens a course URL /en/c/learn/courses/<course-id> with no path context query parameter
    When the course page renders
    Then the course body renders in full with the content-tree breadcrumb and its prerequisite list
    And a "this course is part of" affordance lists every path that includes the course

  Scenario: An invalid path context falls back to the canonical view
    Given a reader opens a course URL with a path context that names no known path
    When the course page renders
    Then the course renders the canonical standalone view
    And no error is shown
  ```

- [ ] [AI] **GREEN** — implement `<FEAT>core/manifest.ts` (course-ref normalization `id | {id, framing}`),
      `<FEAT>core/path-nav.ts` (`resolvePathNav`), `<FEAT>core/path-context.ts` (`parsePathContext`)
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: the new tests pass; no others break.
- [ ] [AI] **RED** — write a failing unit test in
      `apps/ayokoding-www/src/features/content/core/content-url.test.ts` for
      `contentUrl(locale, slug, pathId)` appending `?path=<pathId>` and producing the
      `/en/c/learn/courses/<course-id>` shape — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: fails (param + new URL shape not yet supported).

  **Gherkin (underpins) →** "A path landing page lists its courses in manifest order"; "The breadcrumb
  reflects the active path"; "A legacy fundamentally-strong URL redirects to the canonical course URL"

  ```gherkin
  Scenario: A path landing page lists its courses in manifest order
    Given the interview-ready/software-engineer path manifest is published
    When a reader opens the path landing page at /en/c/learn/paths/interview-ready/software-engineer
    Then the courses appear in the manifest's courseOrder
    And every course link carries the path context query parameter

  Scenario: The breadcrumb reflects the active path
    Given a reader is on a course with an active path context
    When the breadcrumb renders
    Then it shows Home, Learn, the path title, and the course title
    And the path crumb links to the path landing page /en/c/learn/paths/<path-id> with the path context preserved

  Scenario: A legacy fundamentally-strong URL redirects to the canonical course URL
    Given a re-homed course previously lived under the legacy fundamentally-strong/software-engineer content path
    When a reader requests the legacy URL
    Then the app redirects to the course's canonical /en/c/learn/courses/<course-id> URL
    And the redirect preserves any path context query parameter
  ```

- [ ] [AI] **GREEN** — extend `content-url.ts` with the optional `pathId` param appending `?path=` and
      the `/en/c/learn/courses/<course-id>` canonical shape
      [Repo-grounded — `apps/ayokoding-www/src/features/content/core/content-url.ts`] — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the new test passes; existing `content-url`
      tests still pass (or are updated for the new canonical shape in the same commit).
- [ ] [AI] **RED** — write failing unit tests in `<FEAT>core/prerequisites.test.ts` for
      `resolvePrerequisites(courseId, prerequisitesByCourse)` (returns declared prereq IDs; missing →
      empty) and `checkPrerequisiteConsistency(manifest, prerequisitesByCourse, libraryCourseIds)`
      (reports any course whose declared, in-library prerequisite is absent-from or later-than the
      course in `courseOrder`) — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
      (functions undefined).

  **Gherkin (underpins) →** "A course page surfaces its declared prerequisites"; "A path manifest is a
  valid topological entry into the prerequisite DAG"

  ```gherkin
  Scenario: A course page surfaces its declared prerequisites
    Given a course declares prerequisites in its canonical metadata
    When a reader opens the course page with or without a path context
    Then the page lists each prerequisite course with a link to its canonical URL
    And the prerequisite list renders even in the canonical no-path view

  Scenario: A path manifest is a valid topological entry into the prerequisite DAG
    Given a path manifest lists a courseOrder of course IDs
    When the manifest-integrity check runs
    Then no course appears before any of its declared prerequisites that are also in the manifest
    And every listed course ID resolves to an existing course in the library
  ```

- [ ] [AI] **GREEN** — implement `resolvePrerequisites` + `checkPrerequisiteConsistency` in
      `<FEAT>core/prerequisites.ts` (pure; no IO) — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: the new tests pass.
- [ ] [AI] **RED** — write a failing unit test in `<FEAT>core/manifest-integrity.test.ts` for
      `checkManifestIntegrity(manifest, libraryCourseIds)` asserting it reports every `courseOrder`
      entry whose ID is absent from `libraryCourseIds` and every ID that appears more than once
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails (`checkManifestIntegrity` undefined).

  **Gherkin (underpins) →** "Every manifest course reference resolves to a real course"

  ```gherkin
  Scenario: Every manifest course reference resolves to a real course
    Given a path manifest lists a courseOrder of course IDs
    When the manifest-integrity check runs
    Then every listed course ID resolves to an existing course in the library
    And no course ID appears more than once in the manifest
  ```

- [ ] [AI] **GREEN** — implement `checkManifestIntegrity(manifest, libraryCourseIds)` in
      `<FEAT>core/manifest-integrity.ts` (pure; returns unresolved + duplicate ID sets) — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the new test passes.
- [ ] [AI] **REFACTOR** — extract shared course-ref types; ensure `core/` stays IO-free (pure) —
      command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck` — acceptance:
      all green; no `fs`/React import in `core/`.

### Phase 2 Gate

- [ ] [AI] `resolvePathNav` + `parsePathContext` + `contentUrl(pathId)` + `resolvePrerequisites` + `checkPrerequisiteConsistency` + `checkManifestIntegrity` implemented; unit tests green.
- [ ] [AI] `course-paths` Gherkin authored under `<SPECS>`; `specs:behavior:coverage` maps the new features (step bindings land in Phase 3 — record the coverage delta).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:typecheck` + `:lint` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the pure ordering + context + prerequisite logic is implemented and unit-tested; no
> route or component consumes it yet, so nav behavior is unchanged. Safe to stop. To resume: `:test:unit`.

---

## Phase 3: `course-paths` shell + route wiring + prerequisite display + redirects — integration TDD

> _Suggested executor: `swe-typescript-dev`._

- [ ] [AI] **RED** — write failing integration tests for `<FEAT>shell/manifest-repository.ts` (loads and
      validates each `<MANIFESTS>**/*.yaml` data file into a `PathManifest[]` via the `schemas.ts` zod
      schema, keyed by the nested path id) — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: tests fail (repository wiring absent).

  **Gherkin (binds) →** "The three software-engineer paths reference a shared course with no body
  duplication" — scoped to the three `software-engineer`-role paths only; the fourth path
  (`immediately-effective/software-engineer-to-ai-engineer`) links to shared courses rather than
  including them in its manifest (DD-24), so it is deliberately excluded from this scenario.

  ```gherkin
  Scenario: The three software-engineer paths reference a shared course with no body duplication
    Given a course appears in all three of the interview-ready, immediately-effective/software-engineer, and fundamentally-strong/software-engineer manifests
    When the course library is inspected
    Then exactly one canonical path-neutral body exists for that course
    And each manifest references the course by its stable course ID
  ```

- [ ] [AI] **RED** — write a failing integration test for the content service resolving
      `(courseId, activePath)` → path-aware prev/next — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: test fails (service wiring absent).

  **Gherkin (binds) →** "Prev and next follow the active path's order"

  ```gherkin
  Scenario: Prev and next follow the active path's order
    Given a reader is on a course with an active path context
    When the reader reads the prev/next navigation
    Then prev and next are the neighboring courses in that path's manifest
    And both links preserve the path context query parameter
  ```

- [ ] [AI] **Declare direct dependency** — `js-yaml` is currently only a nested transitive dependency
      (via `gray-matter`) and is not exact-pinned in `apps/ayokoding-www/package.json`; add it as a
      direct `dependencies` entry, exact-pinned per the
      [Dependency Bump Stability & Safety Policy](../../../repo-governance/development/workflow/dependency-bump-policy.md)
      (Path A: current LTS-compatible latest patch, CVE-clean) — acceptance: `js-yaml` appears in
      `apps/ayokoding-www/package.json` `dependencies` with an exact version; `npm install` resolves
      with no peer-dependency warning for it.
- [ ] [AI] **GREEN** — implement `<FEAT>shell/manifest-repository.ts` to read + parse each
      `<MANIFESTS>**/*.yaml` data file via the now-direct `js-yaml` dependency (manifest data files are
      always `.yaml`; no JSON fallback); extend the content index to carry loaded manifests +
      per-course `prerequisites` alongside `trees`/`prevNext`
      [Repo-grounded — `ContentIndex` in `apps/ayokoding-www/src/features/content/core/types.ts` and
      the service in `.../content/shell/service.ts`] — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the new integration tests pass. Wire
      `checkManifestIntegrity` + `checkPrerequisiteConsistency` into the repository so a load with any
      unresolved/duplicate ID or prerequisite-order violation throws at build time.
- [ ] [AI] **GREEN** — wire the course route: in
      `apps/ayokoding-www/src/app/[locale]/(content)/c/[...slug]/page.tsx` [Repo-grounded] read
      `searchParams.path`, call `parsePathContext`, and render path-aware prev/next + breadcrumb when a
      valid path context resolves and the course is in that manifest; else render the canonical view.
      Extend `navigation/shell/prev-next.tsx` and `navigation/shell/breadcrumb.tsx` to accept an
      optional path context (links carry `?path=`) — command: `npx nx run ayokoding-www:build` —
      acceptance: build green; canonical (no-path) rendering unchanged for non-path routes.
- [ ] [AI] **GREEN** — author `<FEAT>shell/prerequisite-list.tsx` (**prerequisite display** — reads the
      course's `prerequisites` metadata, links each to its canonical `/en/c/learn/courses/<id>` URL),
      `<FEAT>shell/path-banner.tsx` (in-path readout; below `md` it also carries the rail's disclosure
      trigger), and `<FEAT>shell/path-course-links.tsx`
      ("this course is part of: …") consumed by the course page — command:
      `npx nx run ayokoding-www:test:unit` (component tests) — acceptance: tests pass; prerequisite
      display renders declared prerequisites.
- [ ] [AI] **RED** — write failing component tests for `<FEAT>shell/path-rail.tsx` _(New test)_ — the
      **selected Screen 3 Option B** — asserting: a `<nav>` whose accessible name is
      `{Path} course list`; a semantic `<ol>` in manifest order; the current course carrying
      `aria-current="page"` **and** a non-colour signal (`▸` marker + `font-semibold` class); every row
      link carrying `?path=<path-id>`; each row's `aria-label` holding the untruncated title; and the
      footer's `view full path` + `browse all courses` escape links present — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the suite fails with `path-rail` module not
      found (`test -f apps/ayokoding-www/src/features/course-paths/shell/path-rail.tsx` returns non-zero
      today — the whole `course-paths` feature is new, verified).
- [ ] [AI] **GREEN** — author `<FEAT>shell/path-rail.tsx` and wire it as a **content swap in the two
      existing hosts**, per [prd.md Screen 3](./prd.md#screen-3--course-page-in-path-context): pass
      `<PathRail>` instead of `<Sidebar>` as `ResizableSidebar`'s `children` when `parsePathContext`
      resolves, and instead of `<SidebarTree>` inside `MobileNav`'s `SheetContent` below `md`. **Do not
      fork `ResizableSidebar`, do not add a second `<aside>`, and do not add a second `localStorage`
      width key** — the `hidden … md:block` gate, the 15 %-35 % band, the resize handle, and
      `ayokoding-sidebar-width` are all reused unchanged [Repo-grounded —
      `apps/ayokoding-www/src/features/navigation/shell/resizable-sidebar.tsx`,
      `apps/ayokoding-www/src/features/app-shell/shell/mobile-nav.tsx`] — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:build` — acceptance: both exit 0;
      `grep -c "ResizableSidebar" apps/ayokoding-www/src/features/navigation/shell/*.tsx` still finds
      exactly one component definition (no fork).
- [ ] [AI] **GREEN** — add the below-`md` disclosure trigger to `path-banner.tsx`: a `md:hidden`
      `<button>` with accessible name `Open path course list — {Path}, course {k} of {N}`, plus
      `aria-expanded` and `aria-controls` pointing at the drawer, opening the **same** `MobileNav` sheet
      the header `☰` opens (single `open` state in `header.tsx`, not a second overlay) — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: a test asserts the button's accessible name and
      that `aria-expanded` flips on activation.
- [ ] [AI] **GREEN — no-path regression guard** — assert the canonical (no `?path=`) render is unchanged:
      `ResizableSidebar` receives `<Sidebar>`, `MobileNav` receives `<SidebarTree>`, and neither the rail
      nor the banner appears — command: `npx nx run ayokoding-www:test:unit` — acceptance: the guard test
      passes and fails if the rail is rendered without a path context (assert both directions explicitly,
      not just the positive case).
- [ ] [AI] **GREEN** — add redirects for re-homed courses: for every existing (topics 1–33 + 4
      capstones, incl. `capstone-solid-core`) course, a redirect from
      `.../fundamentally-strong/software-engineer/<slug>` to
      `/en/c/learn/courses/<course-id>` in `apps/ayokoding-www/src/redirects/` [Repo-grounded —
      precedent `.../gherkin/navigation/learn-reorg-redirects.feature`] — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: redirect resolution test passes.
- [ ] [AI] **GREEN (specs)** — implement the step bindings so the `<SPECS>` Gherkin scenarios execute —
      command: `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: exits 0.
- [ ] [AI] **REFACTOR** — deduplicate breadcrumb/prev-next path-vs-canonical branches; keep `shell/`
      the only IO — command:
      `npx nx run ayokoding-www:test:unit && :typecheck && :lint` — acceptance: all green. (`:test:integration` is a no-op echo for this content app — the integration tier is deliberately unused; unit consumes the Gherkin mocked.)

### Phase 3 Gate

- [ ] [AI] Manifest loading + path-aware route wiring + prerequisite display + redirects implemented; integration tests green.
- [ ] [AI] `PathRail` (selected Screen 3 Option B) renders in **both** hosts via content swap — `ResizableSidebar` is not forked, no second `<aside>` and no second width key exist, and the no-path render is proven unchanged in both directions.
- [ ] [AI] `specs:behavior:coverage` green; canonical (no-path) nav unchanged (retained nav specs pass).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:build` + `:typecheck` + `:lint` exit 0. (`:test:integration` is a no-op echo — omitted deliberately, not overlooked.)
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the feature resolves a manifest + path context + prerequisites end-to-end (no
> manifests published yet, so the canonical view is what renders); redirects are in place. Safe to
> stop. To resume: `npx nx run ayokoding-www:test:unit`.

---

## Phase 4: Path landing + paths hub (2×2-grid, four cards) + e2e

> _Suggested executor: `swe-typescript-dev` + `swe-e2e-dev`._

- [ ] [AI] **GREEN** — author `<FEAT>shell/path-landing.tsx` (renders a manifest's ordered course list,
      links carry `?path=`) and `<FEAT>shell/path-card.tsx` (paths-hub card), rendered by
      `<PATHS>_index.md` / `<PATHS><path-id>/_index.md`, per
      [prd.md Screen 1/2 selected designs](./prd.md#ui-design-funnel-path-aware-navigation-screens) —
      command: `npx nx run ayokoding-www:build` — acceptance: build green; components render; the hub
      supports a **2×2 grid of up to four** path cards (only the interview-ready card is populated once
      Phase 6 ships; the other three cards populate as Phases 9/10/11 land — no manifest is published
      yet at this point in Group A).
- [ ] [AI] **RED (e2e)** — write failing Playwright e2e specs in the ayokoding e2e suite for: path
      landing lists courses in manifest order; prev/next walks the path and preserves `?path=`;
      breadcrumb shows the path; a course page shows its prerequisites; deep-link without `?path=` →
      canonical view; invalid `?path=` → canonical view; old
      `fundamentally-strong/software-engineer/<slug>` URL → redirect to `/en/c/learn/courses/<id>` —
      command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: e2e specs fail (no published manifest yet).
  - _Suggested executor: `swe-e2e-dev`_

  **Gherkin (binds) →** "A path landing page lists its courses in manifest order"; "Prev and next
  follow the active path's order"; "The breadcrumb reflects the active path"; "A course page surfaces
  its declared prerequisites"; "A course deep-linked without path context renders the canonical view";
  "An invalid path context falls back to the canonical view"; "A legacy fundamentally-strong URL
  redirects to the canonical course URL"

  ```gherkin
  Scenario: A path landing page lists its courses in manifest order
    Given the interview-ready/software-engineer path manifest is published
    When a reader opens the path landing page at /en/c/learn/paths/interview-ready/software-engineer
    Then the courses appear in the manifest's courseOrder
    And every course link carries the path context query parameter

  Scenario: Prev and next follow the active path's order
    Given a reader is on a course with an active path context
    When the reader reads the prev/next navigation
    Then prev and next are the neighboring courses in that path's manifest
    And both links preserve the path context query parameter

  Scenario: The breadcrumb reflects the active path
    Given a reader is on a course with an active path context
    When the breadcrumb renders
    Then it shows Home, Learn, the path title, and the course title
    And the path crumb links to the path landing page /en/c/learn/paths/<path-id> with the path context preserved

  Scenario: A course page surfaces its declared prerequisites
    Given a course declares prerequisites in its canonical metadata
    When a reader opens the course page with or without a path context
    Then the page lists each prerequisite course with a link to its canonical URL
    And the prerequisite list renders even in the canonical no-path view

  Scenario: A course deep-linked without path context renders the canonical view
    Given a reader opens a course URL /en/c/learn/courses/<course-id> with no path context query parameter
    When the course page renders
    Then the course body renders in full with the content-tree breadcrumb and its prerequisite list
    And a "this course is part of" affordance lists every path that includes the course

  Scenario: An invalid path context falls back to the canonical view
    Given a reader opens a course URL with a path context that names no known path
    When the course page renders
    Then the course renders the canonical standalone view
    And no error is shown

  Scenario: A legacy fundamentally-strong URL redirects to the canonical course URL
    Given a re-homed course previously lived under the legacy fundamentally-strong/software-engineer content path
    When a reader requests the legacy URL
    Then the app redirects to the course's canonical /en/c/learn/courses/<course-id> URL
    And the redirect preserves any path context query parameter
  ```

**Gherkin (binds) →** "The navigation feature meets accessibility requirements"

```gherkin
Scenario: The navigation feature meets accessibility requirements
  Given a reader uses a keyboard and a screen reader on a course in path context
  When they navigate the path rail, banner, breadcrumb, prerequisite list, and prev/next
  Then each is a labelled landmark reachable and operable by keyboard with visible focus
  And the document language attribute matches the active locale
```

- [ ] [AI] **RED (a11y)** — this suite is **playwright-bdd**, so the scenario above is authored as
      Gherkin under `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/` and bound by a step
      definition at `apps/ayokoding-www-fe-e2e/src/steps/course-paths-a11y.steps.ts` (follow the
      existing `accessibility.steps.ts` pattern). The steps assert, on a course rendered in path
      context: the path rail, path banner, path breadcrumb, prerequisite list, and prev/next controls are each a
      labelled landmark reachable and operable by keyboard with a visible focus ring; the current item
      carries `aria-current`; and `<html lang>` equals the active locale (`en`) — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the `course-paths-a11y` scenario fails (the path-aware navigation landmarks do not
      exist yet). This RED step exists because the a11y scenario was previously bound only by the
      REFACTOR step below, which gave it no prior failing state.
      **Do NOT target `ayokoding-www:test:e2e`**: that target is `echo 'no-op: target not applicable
for this project'` and always exits 0, so any RED clause pointed at it can never fail. E2E for
      this app lives entirely in the paired `ayokoding-www-fe-e2e` project (`npx bddgen && npx
playwright test`).
- [ ] [AI] **GREEN (a11y)** — add the landmark roles, accessible labels, `aria-current`, focus
      styling, and locale-correct `lang` attribute so the scenario passes — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the `course-paths-a11y` scenario passes.
- [ ] [AI] **GREEN (e2e fixtures)** — add a minimal fixture manifest (a few real course IDs with
      declared prerequisites) so the e2e specs exercise the real components — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: all `course-paths` e2e specs pass in `en`
      (this plan's content locale; see [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals)).
- [ ] [AI] **RED (Screen 0 hero)** — write a failing Playwright e2e spec asserting the landing hero at
      `/en` renders a "Choose your path" eyebrow with a `PathCard` grid (populated from the same
      fixture manifest as the other `course-paths` e2e specs) and a "Compare all paths" link to
      `/en/c/learn/paths`, per
      [prd.md Screen 0 hi-fi spec](./prd.md#screen-0-hi-fi--landing-hero-en-option-a-four-goal-cards-in-the-hero)
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new spec fails (today's
      `hero.tsx` renders only the H1/tagline/Learn+Tools buttons — no "Choose your path" eyebrow, no
      `PathCard` grid, no "Compare all paths" link).

  **Gherkin (binds) →** "The landing hero surfaces the four goal paths directly"

  ```gherkin
  Scenario: The landing hero surfaces the four goal paths directly
    Given a first-time visitor opens the site landing page at /en
    When the hero section renders
    Then the hero shows a goal-labeled path card for each published path
    And a "Compare all paths" link to /en/c/learn/paths is visible below the cards
  ```

- [ ] [AI] **GREEN (Screen 0 hero)** — edit
      `apps/ayokoding-www/src/features/app-shell/shell/hero.tsx` per the same hi-fi spec: add the
      "Choose your path" eyebrow + a `PathCard` grid (`context="hero"` variant, 2×2 at `md+`, single
      column below, sourced from the same loaded-manifest data as the paths hub) and the escape-hatch
      row ("Not sure which fits? Compare all paths →" to `/en/c/learn/paths`, "Browse the full course
      library →" to `/en/c/learn/courses`); move the existing Learn/Tools CTAs into the global nav —
      command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the Screen 0 hero e2e spec
      passes.
- [ ] [AI] **REFACTOR** — ensure the landing + hub + hero reuse `libs/web-ui` primitives (no bespoke
      CSS where a token exists) and the hero's `PathCard` grid is the same component and
      manifest-loading path as the hub's (no duplicated card markup or a second data source); a11y pass
      (labels, focus, `aria-current`) — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e && :lint` — acceptance: green; a11y assertions pass; no
      second `PathCard`-rendering implementation exists (`rg -c "function PathCard" apps/ayokoding-www/src`
      returns exactly `1`).

### Phase 4 Gate

- [ ] [AI] Path landing + 2×2-grid paths hub (up to four cards) + the landing-hero `PathCard` grid and
      escape hatch render from the same manifest data; prerequisite display verified; all
      `course-paths` e2e specs green in `en` (this plan's content locale), including the Screen 0 hero
      spec.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:build` + `:lint` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0. (`ayokoding-www:test:e2e` and `:test:integration` are both no-op echoes — e2e lives in the paired `ayokoding-www-fe-e2e` project, and the integration tier is deliberately unused for content apps.)
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the full path-aware navigation UI (incl. prerequisite display + the 2×2-grid hub +
> the landing-hero path-card grid) is implemented, tested (unit + integration + e2e + specs), and
> live — but no real path manifests are published yet, so production still shows the canonical
> library. **Group A (the hard prerequisite) is complete.** Safe to stop. To resume:
> `npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Group B — interview-ready MVP (ships first, end-to-end)

## Phase 5: Re-home the 33 shipped topics + 4 existing capstones into `courses/`

> _Suggested executor: `swe-typescript-dev`_ (mechanical `apps/ayokoding-www/content/` moves +
> redirect wiring — `docs-file-manager` is scoped to `docs/` only and does not cover app content).
> Only the **shipped** legacy bodies move here (33 topics 1–33 + 4 existing capstones, incl.
> `capstone-solid-core` per **DD-20**). Topics 34–94 have no legacy home and are authored NATIVE in
> Phase 12.

- [ ] [AI] For **every** shipped topic + existing capstone, `git mv <SE_OLD><slug>/ <COURSES><slug>/`
      (course-id = slug; no rename), preserving the full page-bundle (`_index.md` + `overview.md` +
      `learning/` + `drilling/`) — acceptance: `<SE_OLD>` holds no course folders from the re-home set;
      every re-homed course resolves under `<COURSES>`; `npx nx run ayokoding-www:generate-indexes`
      succeeds and `:build` exits 0.
- [ ] [AI] **Add prerequisites to each re-homed course** — add `prerequisites: [course-id, ...]` to each
      re-homed `_index.md` frontmatter naming only earlier library courses, per the
      [prerequisite DAG](./tech-docs.md#prerequisite-dag-illustrative-excerpt) — command: `npx nx run ayokoding-www:build`
      — acceptance: every re-homed course declares `prerequisites` (empty list allowed for roots); build green.
- [ ] [AI] Confirm each re-homed course has its redirect (Phase 3) old-URL → new-URL resolving —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: redirect specs green for all moved courses.
- [ ] [AI] Update `<COURSES>_index.md` (library landing) to list the re-homed catalog by course ID —
      acceptance: link-checker green; every catalog link resolves.
- [ ] [AI] Sweep any intra-course cross-links that referenced the old
      `fundamentally-strong/software-engineer/<slug>` path and repoint them to
      `/en/c/learn/courses/<course-id>` (Root Cause Orientation) — command:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` (the actual
      link-validation mechanism — not an `nx run` target; runs pre-commit via `lint-staged` for staged
      `.md` files, and repo-wide in CI's `md-links` job, which currently excludes
      `apps/ayokoding-www/content`, so the Phase 5 e2e nav check below is the binding verification for
      this content tree) — acceptance: zero broken links.

**Preserve the "old-way" `_index.md` section browse (§5a — ADDITIVE model, required).** The
library/paths model is additive: a reader must keep navigating the material **the old way** (the legacy
hand-curated, spiral-ordered `_index.md` section tree) IN ADDITION to the new way (paths + canonical
course pages). Every impacted legacy section index is UPDATED (not deleted), re-pointing each entry to
wherever the content now lives.

- [ ] [AI] **RED** — write a failing integration/e2e nav check asserting the legacy ordered browse
      resolves end-to-end: from `.../fundamentally-strong/software-engineer/_index.md` (and the
      `fundamentally-strong/_index.md` parent + each per-topic `_index.md`), every listed entry link
      resolves to live content (the re-homed `/en/c/learn/courses/<course-id>` URL or a working
      redirect) — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the legacy-browse nav spec
      fails (links still point at drained `<SE_OLD>` locations).

  **Gherkin (binds) →** "The legacy section-index browse still resolves after re-homing"

  ```gherkin
  Scenario: The legacy section-index browse still resolves after re-homing
    Given the 33 shipped topics have been re-homed into the course library
    When a reader browses the legacy fundamentally-strong software-engineer section index the old way
    Then every section-index entry links to live content at its /en/c/learn/courses/<course-id> URL or via a redirect
    And no legacy section-index entry resolves to a drained or missing location
  ```

- [ ] [AI] **RED** — write a failing integration/e2e nav check asserting that a course reached via the
      legacy section-index browse and the same course reached via its
      `/en/c/learn/paths/<path-id>` path landing resolve to the identical canonical course body (same
      rendered content, same canonical URL) — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: the coexistence nav spec fails (no assertion yet ties the two navigation routes to
      the same canonical body).

  **Gherkin (binds) →** "Old-way and new-way navigation coexist"

  ```gherkin
  Scenario: Old-way and new-way navigation coexist
    Given a course now lives at its canonical /en/c/learn/courses/<course-id> URL
    When a reader reaches it via the legacy section-index browse
    And another reader reaches it via a /en/c/learn/paths/<path-id> path landing
    Then both navigations resolve to the same single canonical course body
  ```

  _The two RED steps above are each bound to exactly one scenario per the Gherkin-Tagged Delivery
  Steps HARD rule; the GREEN and REFACTOR steps below are shared across both because the single fix
  (re-pointing every legacy `_index.md` entry to its canonical URL) satisfies both scenarios at once —
  the REFACTOR step's acceptance criterion explicitly re-asserts the old-way/new-way body-equivalence
  scenario._

- [ ] [AI] **GREEN** — enumerate every impacted `_index.md` under
      `apps/ayokoding-www/content/en/learn/fundamentally-strong/**` (`find apps/ayokoding-www/content/en/learn/fundamentally-strong -name _index.md`
      — esp. `.../software-engineer/_index.md`, each per-topic `_index.md`, and the
      `fundamentally-strong/_index.md` parent) and update each so every entry it lists is re-pointed to
      the new `/en/c/learn/courses/<course-id>` URL (or via the redirect) — the legacy sections are
      preserved and ordered, no dead links, no orphaned section — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: both the legacy-browse nav spec and the
      coexistence nav spec now pass.
- [ ] [AI] **REFACTOR** — run
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` +
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md` over the updated legacy `_index.md` tree (the heading-hierarchy validator
      already runs automatically pre-commit via `lint-staged` for every staged `.md` file; this step
      re-runs it explicitly over the full legacy tree) — acceptance: zero broken links; both old-way
      and new-way navigations resolve to the same canonical bodies; validators green.

### Phase 5 Gate

- [ ] [AI] All 33 shipped topics + 4 existing capstones (incl. `capstone-solid-core`) live under `<COURSES>` with declared prerequisites; `<SE_OLD>` drained of the re-home set; redirects resolve; catalog updated.
- [ ] [AI] Every impacted legacy `_index.md` under `.../fundamentally-strong/**` updated; old-way section browse resolves end-to-end (link validator + e2e nav check green); old-way and new-way navigation coexist.
- [ ] [AI] `npx nx run ayokoding-www:build` + link + heading validation green.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: every shipped course now lives at its canonical `/en/c/learn/courses/<id>` URL with
> a redirect + declared prerequisites, AND the legacy `_index.md` section browse still resolves the old
> way (additive); no manifest exists yet, so all courses render the canonical view. Safe to stop. To
> resume: re-run link validation + the legacy-browse e2e + `:build`.

---

## Group L — Legacy bucket / whole-section IA revamp (scope extension, 2026-07-21)

## Phase 5A: Relocate the six non-course `en/learn/` domains into `legacy/` + per-domain 308 redirects

> _Suggested executor: `swe-typescript-dev`_ (redirect module + unit test + `next.config.ts` wiring)
> _plus `apps-ayokoding-www-content-fixer`_ for the two hub-file rewrites.
>
> **Why this is one phase, not two.** The six `git mv`s and the redirect module must land **together**:
> a live 308 pointing at a not-yet-moved path 404s, and a moved path with no 308 breaks ~1,148 URLs.
> Neither half is a safe stopping state, so the phase boundary sits after both.
>
> **Why it sits here.** After Phase 5 (so `courses/` already exists and `en/learn/` is never
> transiently `legacy/`-only) and before Phase 6 (so the paths hub and every later manual
> verification see the final three-bucket shape). See
> [tech-docs §Learn-Section IA](./tech-docs.md#learn-section-ia--the-three-bucket-model-scope-extension-2026-07-21),
> DD-40 through DD-45, and the BEFORE/AFTER trees at
> [tech-docs §Content tree — AFTER](./tech-docs.md#content-tree--after-target-state).
>
> **Open questions.** Every step below executes the **recommended default** of its governing question
> and names the alternative inline, so an overturned ruling is a bounded edit:
> [Q-A](./tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive) (staging pen),
> [Q-B](./tech-docs.md#q-b--does-the-id-locale-get-the-same-three-bucket-shape-now) (`id` out of
> scope), [Q-C](./tech-docs.md#q-c--if-id-is-in-scope-are-the-bucket-segments-translated) (moot while
> Q-B = A), [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy) (indexed + banner),
> [Q-E](./tech-docs.md#q-e--what-happens-to-fundamentally-strongs-three-residual-index-pages)
> (fold into the path landing), [Q-F](./tech-docs.md#q-f--what-happens-to-enlearnoverviewmd)
> (keep `overview.md`, rewritten).

### 5A.1 · Redirect module (TDD)

- [ ] [AI] **RED** — write a failing unit test at `<REDIR>learn-three-bucket.unit.test.ts`
      _(New test)_, mirroring the existing `<REDIR>content-namespace.unit.test.ts` structure
      [Repo-grounded], asserting all six properties: (a) exactly **12** rules — one pair per relocated
      domain; (b) every rule `permanent: true` with non-empty `source`/`destination`; (c) each
      destination equals its source with `legacy/` inserted at the bucket position; (d) **no** rule
      whose source matches `/^\/en\/c?\/?learn\/:path\*$/` (the self-recursing blanket, DD-42); (e)
      **no** rule whose first path segment after `learn/` is `courses`, `paths`, or
      `fundamentally-strong` (DD-42/DD-43); (f) the six expected domain names are all covered —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: the suite fails with
      `learn-three-bucket` module not found (falsifiable both ways: the module does not exist today —
      `test -f apps/ayokoding-www/src/redirects/learn-three-bucket.ts` returns non-zero, verified).

  **Gherkin (binds) →** "The legacy redirect never swallows the courses or paths buckets"; "A
  re-homed fundamentally-strong course is not routed into the legacy bucket"

  ```gherkin
  Scenario: The legacy redirect never swallows the courses or paths buckets
    Given the legacy bucket redirect rules are configured
    When a reader requests a canonical course URL or a path landing URL
    Then the app serves the page without redirecting it
    And no redirect rule declares a bucket-wide learn-section wildcard source

  Scenario: A re-homed fundamentally-strong course is not routed into the legacy bucket
    Given the fundamentally-strong topic directories were collapsed into flat course bodies
    When a reader requests a legacy fundamentally-strong course URL
    Then the app redirects to that course's canonical course URL
    And no legacy-bucket rule matches the fundamentally-strong prefix
  ```

- [ ] [AI] **GREEN** — author `<REDIR>learn-three-bucket.ts` _(New file)_ exporting
      `learnThreeBucketRedirects` with the 12 rules (per domain: a **tier-1** bare rule
      `/en/learn/<domain>/:path*` → `/en/c/learn/legacy/<domain>/:path*` and a **tier-2** `/c` rule
      `/en/c/learn/<domain>/:path*` → same destination), each `permanent: true`, for
      `software-engineering`, `artificial-intelligence`, `information-security`,
      `personal-development`, `it-governance`, `business`. Carry a header comment stating the blanket
      ban and the ordering requirement, in the style of `content-namespace.ts` — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the new suite passes; no existing redirect
      test breaks.
- [ ] [AI] **GREEN** — wire the module into `apps/ayokoding-www/next.config.ts` `redirects()` as
      `return [...learnReorgRedirects, ...learnThreeBucketRedirects, ...contentNamespaceRedirects];`
      — the order is load-bearing (DD-42): **after** `learnReorg` so historical within-`/en/learn/`
      renames resolve to their canonical domain first, **before** `contentNamespace` so the tier-1
      rules collapse a three-hop chain to one hop — command:
      `npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:build` — acceptance: both exit 0;
      `grep -c "learnThreeBucketRedirects" apps/ayokoding-www/next.config.ts` returns **2** (the import
      and the spread) — returns **0** today, verified.
- [ ] [AI] **REFACTOR** — extract the six domain names into one exported `RELOCATED_DOMAINS` array
      that both tiers map over, so a seventh domain cannot be added to one tier and forgotten in the
      other — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` —
      acceptance: both exit 0; the 12-rule assertion still passes.

### 5A.2 · Relocate the six domains (pure `git mv`, DD-41)

- [ ] [AI] Create the bucket root and `git mv` each domain, preserving its sub-taxonomy verbatim:
      `mkdir -p apps/ayokoding-www/content/en/learn/legacy && for d in software-engineering artificial-intelligence information-security personal-development it-governance business; do git mv "apps/ayokoding-www/content/en/learn/$d" "apps/ayokoding-www/content/en/learn/legacy/$d"; done`
      — acceptance: `find apps/ayokoding-www/content/en/learn/legacy -name '*.md' | wc -l` returns
      **1148**, and
      `for d in software-engineering artificial-intelligence information-security personal-development it-governance business; do test -e "apps/ayokoding-www/content/en/learn/$d" && echo "STILL AT ROOT $d"; done`
      prints nothing (falsifiable both ways: it prints all six today, verified).
- [ ] [AI] **Prove the move rewrote nothing** — `git diff --cached --stat -M --diff-filter=M -- apps/ayokoding-www/content/en/learn/legacy`
      — acceptance: **no** modified (`M`) content file under `<LEGACY>` other than files this phase
      explicitly authors; `git diff --cached --summary -M` shows the relocated files as pure renames
      (DD-41). A content-modifying hunk here is a defect, not a cleanup.

  **Gherkin (binds) →** "The relocation rewrites no page content"

  ```gherkin
  Scenario: The relocation rewrites no page content
    Given the six non-course learn-section domains have been relocated
    When the relocation commit's diff is inspected
    Then every relocated file appears as a pure rename with no content change
    And the only edited content files are the section overview and the new legacy bucket index
  ```

- [ ] [AI] Author `<LEGACY>_index.md` _(New file)_ — **required**, not optional: `generate-indexes`
      only rewrites `_index.md` files that already exist
      [Repo-grounded — `processAllIndexFiles` filters `allContent.filter(c => c.isSection)` in
      `apps/ayokoding-www/src/features/content/shell/index-generator.ts`], and without it
      `buildTreeForLocale` synthesizes a `weight: 0` "Legacy" node that would sort **first** in the
      sidebar, ahead of `courses/` and `paths/`
      [Repo-grounded — `apps/ayokoding-www/src/features/content/core/tree-builder.ts`]. Give it
      `title`, `date`, `draft: false`, and an explicit `weight` greater than the `courses/` and
      `paths/` weights, plus the Q-D landing notice per
      [prd.md Screen 4](./prd.md#screen-4--legacy-bucket-landing-and-page-banner-scope-extension) —
      acceptance: `test -f apps/ayokoding-www/content/en/learn/legacy/_index.md`; and after
      `npx nx run ayokoding-www:build` the sidebar order under `learn` is `paths`, `courses`,
      `legacy` (verified in 5A.5's Playwright pass, not asserted by grep).

  **Gherkin (binds) →** "The legacy bucket landing tells a reader what the bucket is"

  ```gherkin
  Scenario: The legacy bucket landing tells a reader what the bucket is
    Given a reader opens the legacy bucket landing page
    When the page renders
    Then it states that the material is older and kept for reference while the course library fills
    And it links onward to the course library and to the paths hub
  ```

- [ ] [AI] Rewrite the hand-authored `apps/ayokoding-www/content/en/learn/overview.md` so its
      inventory names the **three buckets** instead of the six domains (Q-F recommended answer A —
      keep it as the section hub page; do **not** move its prose into `_index.md`, which
      `generate-indexes` machine-rewrites and would clobber) — acceptance:
      `grep -cE '/en/c/learn/(paths|courses|legacy)' apps/ayokoding-www/content/en/learn/overview.md`
      returns **≥ 3**, and
      `grep -cE '\(/en/learn/(software-engineering|artificial-intelligence|information-security|personal-development|it-governance|business)' apps/ayokoding-www/content/en/learn/overview.md`
      returns **0** (falsifiable both ways: it returns 6 today — the file links all six domains at
      their bare pre-`/c` URLs, verified).
- [ ] [AI] Regenerate the derived artifacts: `npx nx run ayokoding-www:generate-indexes` then
      `npx nx run ayokoding-www:generate-search-data` — acceptance: both exit 0;
      `npx nx run ayokoding-www:validate-indexes` exits 0 afterward (proving regeneration converged);
      `generated/search-data.json` is rewritten and every relocated doc's `slug` now begins
      `learn/legacy/`.

  **Gherkin (binds) →** "The learn section exposes exactly three structural buckets"; "Navigation
  surfaces follow the relocated tree with no code change"

  ```gherkin
  Scenario: The learn section exposes exactly three structural buckets
    Given the learn-section IA revamp has landed
    When the content tree under the en learn section is inspected
    Then its only structural buckets are paths, courses, and legacy
    And no former subject domain remains as a direct child of the learn section
    And the section keeps its own index and overview hub pages

  Scenario: Navigation surfaces follow the relocated tree with no code change
    Given the six domains now live under the legacy bucket
    When the sidebar tree, browse index, sitemap, feed, and search data are regenerated
    Then each lists every relocated page at its new legacy URL
    And no navigation source file required a hardcoded domain slug to be edited
  ```

### 5A.3 · Specs + e2e (Gherkin-bound)

- [ ] [AI] **RED (specs)** — author `<NAVSPECS>learn-three-bucket.feature` _(New file)_ beside the
      existing `content-namespace-redirects.feature` [Repo-grounded], carrying the three-bucket
      scenarios from [prd.md](./prd.md#three-bucket-learn-section-ia-scope-extension-2026-07-21) —
      command: `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: fails (no step
      bindings yet).
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED (e2e)** — write failing Playwright specs in the paired `ayokoding-www-fe-e2e` project
      asserting: one relocated URL per domain 308s to its `legacy/` address in **both** inbound forms
      (bare `/en/learn/<domain>/…` and `/en/c/learn/<domain>/…`); the deep path
      `/en/c/learn/software-engineering/programming-languages/python/by-example/advanced` lands at its
      `legacy/` twin; a historical `learn-reorg` source (`/en/learn/human/…`) chains to
      `/en/c/learn/legacy/personal-development/…`; a `courses/` URL and a `paths/` URL are **not**
      rewritten; and an old `fundamentally-strong` course URL still resolves to
      `/en/c/learn/courses/<id>` (DD-43) — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: the new specs fail. **Do NOT target `ayokoding-www:test:e2e`** — that target is
      `echo 'no-op: target not applicable for this project'` and always exits 0
      [Repo-grounded — `apps/ayokoding-www/project.json`], so a RED clause pointed at it can never
      fail.
  - _Suggested executor: `swe-e2e-dev`_

  **Gherkin (binds) →** "A relocated legacy domain URL redirects to its legacy address"; "A deep
  legacy path keeps its sub-taxonomy verbatim"

  ```gherkin
  Scenario: A relocated legacy domain URL redirects to its legacy address
    Given a page previously lived at a learn-section domain that is not a course or a path
    When a reader requests that page's old URL
    Then the app permanently redirects to the same page under the legacy bucket
    And the rest of the path after the domain segment is preserved unchanged

  Scenario: A deep legacy path keeps its sub-taxonomy verbatim
    Given a legacy page previously lived several levels below its domain
    When a reader follows the redirect to its new legacy address
    Then every path segment below the domain is unchanged
    And the page body is byte-identical to the body served before the relocation
  ```

- [ ] [AI] **GREEN (specs + e2e)** — implement the step bindings so both the `<NAVSPECS>` scenarios
      and the e2e specs execute against the landed module and moved tree — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — run
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` +
      `... -- md heading-hierarchy validate` + `npm run lint:md` over the relocated tree and the two
      rewritten hub files (the actual link/heading mechanism — **not** `nx run` targets; both also run
      pre-commit via `lint-staged` for staged `.md`) — acceptance: zero broken links; validators green.

### 5A.4 · Screen 4 design funnel (Q-D)

> **Screen 4 closes the 30-asset matrix.** Six renders (2 options × 3 viewports) at 375 / 768 / 1280 px,
> named per [prd.md §Hi-fi asset matrix](./prd.md#hi-fi-asset-matrix-screen--option--viewport), each from
> its own `assets/src/<stem>.html`. Enumerated per asset — a single "render the Screen 4 mockups"
> checkbox could be ticked with four of six missing. Option C is deliberately **not** rendered: it is
> Option B's landing plus a `robots` metadata change, which a mockup cannot depict.

- [ ] [AI] Render `assets/legacy-landing-option-a-mobile.png` from `assets/src/legacy-landing-option-a-mobile.html` at 375 px — acceptance: file exists; single-column domain list, per-page banner above the H1.
- [ ] [AI] Render `assets/legacy-landing-option-a-tablet.png` from `assets/src/legacy-landing-option-a-tablet.html` at 768 px — acceptance: file exists; two-column domain list, sidebar column present.
- [ ] [AI] Render `assets/legacy-landing-option-a-desktop.png` from `assets/src/legacy-landing-option-a-desktop.html` at 1280 px — acceptance: file exists.
- [ ] [AI] Render `assets/legacy-landing-option-b-mobile.png` from `assets/src/legacy-landing-option-b-mobile.html` at 375 px — acceptance: file exists; relocated page shows **no** banner (the option's defining absence).
- [ ] [AI] Render `assets/legacy-landing-option-b-tablet.png` from `assets/src/legacy-landing-option-b-tablet.html` at 768 px — acceptance: file exists.
- [ ] [AI] Render `assets/legacy-landing-option-b-desktop.png` from `assets/src/legacy-landing-option-b-desktop.html` at 1280 px — acceptance: file exists.
- [ ] [AI] **Embed all six in `prd.md` Screen 4** with viewport-specific descriptive alt text (each
      naming what differs at that width, never a copy of the desktop text) — acceptance:
      `grep -o "assets/legacy-landing-option-[ab]-[a-z]*\.png" prd.md | sort -u | wc -l` returns **6**
      (returns **0** before this phase, verified — the two prose mentions of the naming convention use
      brace notation and do not match this pattern), AND
      `find assets -name '*-option-*-*.png' | wc -l` returns **30** — the complete
      matrix (returns **24** after Phase 1, verified), AND
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate`
      resolves every new `![]()` target.
- [ ] [AI] **Record the Screen 4 selection** — replace prd.md Screen 4's
      "**Selection: PENDING…**" line with the ruled answer once Q-D is settled; under the recommended
      default (option A) that is "**Selected: Option A — indexed + landing notice + per-page banner**"
      — acceptance: `grep -c "Selection: PENDING" prd.md` returns **0** and
      `grep -c "Selected: Option" prd.md` increases by 1 relative to its pre-step value (record both
      values in the PR description; the bare post-value is not falsifiable on its own because the
      Screen 0-3 selections already match).
- [ ] [AI] Apply the ruled Q-D treatment: under option A, add the `Alert`-based "legacy / superseded"
      notice to `<LEGACY>_index.md` and the per-page banner affordance; under option C instead set
      `robots: noindex` metadata for the bucket. Reuse the existing composite `Alert` primitive — **no
      net-new component** (DD-44) — acceptance: the ruled treatment is present and
      `npx nx run ayokoding-www:build` exits 0.

### 5A.5 · Manual verification (`en`, all breakpoints)

- [ ] [AI] Start the dev server (`npx nx dev ayokoding-www`) and, via Playwright MCP at
      375 / 768 / 1280 px, open `/en/c/learn`, `/en/c/learn/legacy`, one relocated page per domain, and
      one deep relocated page; confirm the sidebar shows `learn` with exactly `paths`, `courses`,
      `legacy` (in that order); confirm the legacy page breadcrumb reads
      `Home / Browse / Learn / Legacy / <domain> / <title>` and — per the
      [prd Screen 4 responsive note](./prd.md#screen-4--legacy-bucket-landing-and-page-banner-scope-extension)
      — **does not wrap to multiple lines at 375 px**; confirm `browser_console_messages` is clean —
      acceptance: all behaviors correct; zero console errors.
- [ ] [AI] Capture one screenshot per screen per breakpoint to
      `evidence/phase-5a-<screen>-en-<breakpoint>px.png` — acceptance: files exist in `evidence/`.
- [ ] [AI] **Record the `id` deferral explicitly (DD-45 / Q-B)** — confirm `id/belajar/` is untouched:
      `find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l` returns **53** (its Phase-0
      baseline) and `test -e apps/ayokoding-www/content/id/belajar/legacy` returns non-zero; then note
      in this checklist that the `id` locale is deliberately out of scope per Q-B's recommended answer
      — acceptance: both checks hold and the deferral note is written here, not left implicit.

  **Gherkin (binds) →** "The Indonesian locale is left unchanged and the deferral is recorded"

  ```gherkin
  Scenario: The Indonesian locale is left unchanged and the deferral is recorded
    Given the learn-section IA revamp is scoped to the English locale
    When the Indonesian content tree is inspected after the revamp
    Then its section is unchanged with no bucket directories and no relocation
    And the plan records the Indonesian deferral explicitly as a non-goal
  ```

### Phase 5A Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] `ls apps/ayokoding-www/content/en/learn` lists exactly `_index.md`, `overview.md`, `courses`, `legacy`, `paths` — the three structural buckets plus the two hub files (DD-40/DD-45). Falsifiable both ways: it lists seven domain directories today.
- [ ] [AI] `find apps/ayokoding-www/content/en/learn/legacy -name '*.md' | wc -l` returns **1148**; the relocation diff shows pure renames with no content-modifying hunk under `<LEGACY>` (DD-41).
- [ ] [AI] `<REDIR>learn-three-bucket.ts` exports 12 rules; `learn-three-bucket.unit.test.ts` green, including the negative assertions (no blanket source; no `courses`/`paths`/`fundamentally-strong` source prefix).
- [ ] [AI] `next.config.ts` spreads the module **between** `learnReorgRedirects` and `contentNamespaceRedirects` (DD-42).
- [ ] [AI] `npx nx run ayokoding-www:build` + `:typecheck` + `:lint` + `:test:unit` + `:validate-indexes` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0. (`ayokoding-www:test:e2e` and `:test:integration` are no-op echoes — omitted deliberately.)
- [ ] [AI] `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` and `... -- md heading-hierarchy validate` green over the relocated tree.
- [ ] [AI] All six Screen 4 renders exist in `assets/` and are embedded in `prd.md` with viewport-specific alt text; `find assets -name '*-option-*-*.png' | wc -l` returns **30** (the full 5 × 2 × 3 matrix); the Q-D selection is recorded (no "Selection: PENDING" remains).
- [ ] [AI] `id/belajar` still holds 53 `.md` and has no bucket directory; the deferral is written into this checklist (DD-45).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: `/en/c/learn/` is at its final three-bucket shape, every relocated URL 308s to its
> new address in both inbound forms, `courses/` and `paths/` are provably unaffected, and no page body
> was edited. Production serves a coherent section. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 6: Author the `interview-ready/software-engineer` manifest + landing + wire + smoothness (architecture smoke test — MVP ships, DD-27)

> _Suggested executor: `apps-ayokoding-www-general-maker` (manifest/landing) + `web-researcher` (smoothness facts)._
> **Amended 2026-07-20 (D7/DD-27).** This phase is now an **architecture smoke test only** — it ships
> against the 33 topics + 4 capstones already re-homed in Phase 5, proving routing, manifest loading,
> `?path` context propagation, prev/next, breadcrumb, and prerequisite display against real content,
> quickly (days, not months). The four interview-technique courses (`coding-interview`,
> `take-home-and-live-coding`, `system-design-interview`, `behavioral-and-leadership-interviews`) plus
> `capstone-interview-loop` are **no longer bundled into this MVP gate** — they are deferred to Phase 12
> Band 9 and inserted into this same `courseOrder`, in their correct topological position, when they
> land, growing this manifest without blocking the AI path's authoring start in Phase 7.

- [ ] [AI] Author the manifest **data file** `<MANIFESTS>interview-ready/software-engineer.yaml`
      (standalone data file): `pathId: interview-ready/software-engineer`, `title`, `description`, and
      the ordered `courseOrder` = the interview-first arc from
      [tech-docs §Path `interview-ready/software-engineer`](./tech-docs.md#path-interview-readysoftware-engineer-interview-first)
      and [syllabus/paths/README.md](./syllabus/paths/README.md), **restricted to the 33 shipped topics + 4 existing capstones already live under `<COURSES>`** (the five deferred interview-technique
      bodies are inserted later, DD-27) — acceptance: the manifest loads + validates (`npx nx run
ayokoding-www:test:unit` exits 0); references only extant courses; the five deferred course IDs
      are absent from the published `courseOrder` right now —
      `grep -E "coding-interview|take-home-and-live-coding|system-design-interview|behavioral-and-leadership-interviews|capstone-interview-loop" <MANIFESTS>interview-ready/software-engineer.yaml`
      returns nothing (falsifiable both ways: after Phase 12 Band 9 lands and grows this manifest, the
      same command must return all five lines).
- [ ] [AI] Author the thin landing anchor `<PATHS>interview-ready/software-engineer/_index.md`
      (prose/SEO only — no `courseOrder`); the ordered course list renders from the loaded manifest per
      [prd.md Screen 2](./prd.md#screen-2--path-landing-page) — acceptance: landing renders the
      manifest-ordered list over the smoke-test-scoped `courseOrder` (phase-grouped, fast-path callout;
      the interview-loop map is added when Phase 12 Band 9 lands).
- [ ] [AI] **Manifest integrity + prerequisite-consistency check** — every `courseOrder` ID resolves
      under `<COURSES>`; no duplicate ID; every in-library prerequisite of each listed course appears
      earlier in the ordering — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] **Architecture smoke test** — verify, against this real manifest, the six things D7/DD-27
      names: routing resolves, the manifest loads, `?path=interview-ready/software-engineer` context
      propagates, prev/next walks the manifest order, the breadcrumb shows the path, and course pages
      show their prerequisites — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the
      path-walk e2e spec passes in `en` (this plan's content locale).

  **Gherkin (binds) →** "The interview-ready MVP proves the architecture before other path work begins"

  ```gherkin
  Scenario: The interview-ready MVP proves the architecture before other path work begins
    Given the interview-ready/software-engineer MVP (an architecture smoke test over already-live topics 1-33) is delivered end-to-end
    When the software-engineer-to-ai-engineer path's authoring begins
    Then the interview-ready MVP's landing page, manifest, and path-aware nav are already live in production
    And the interview cluster's remaining NEW courses are not required for that MVP to be considered shipped
  ```

- [ ] [AI] **Progression smoothness audit (interview-first, DD-16, smoke-test-scoped)** — walk the
      published `courseOrder` and confirm the levers hold (prereq-chaining with SF-1/SF-2 bridges;
      monotonic-ish difficulty; skip/fast-path affordances on the landing) per
      [tech-docs §Smoothness Architecture](./tech-docs.md#smoothness-architecture-per-path) —
      acceptance: every lever assessable over the current `courseOrder` verified; any regression fixed
      by soften/bridge in place, never reorder. The **refresh-register** lever lives inside the four
      deferred interview courses and is **not yet assessable** — it is audited as part of Phase 12 Band
      9's manifest-growth step, not fabricated here.

### Phase 6 Gate

- [ ] [AI] `interview-ready/software-engineer` manifest published (smoke-test-scoped over the 33 topics + 4 capstones); integrity + prerequisite-consistency green; path-walk e2e + breadcrumb + prerequisite display green in `en` (this plan's content locale).
- [ ] [AI] Smoothness audit passes for every lever assessable at this stage (levers, SF-1/SF-2 bridges); refresh-register lever explicitly deferred to Phase 12 Band 9.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0 (e2e lives in the paired `ayokoding-www-fe-e2e` project — `ayokoding-www:test:e2e` is a no-op echo and can never fail).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the `interview-ready/software-engineer` path is **live end-to-end** in production
> (landing + manifest + path-aware nav + prerequisites + smoothness) over its smoke-test-scoped
> `courseOrder` — the **architecture is proven against real content; the interview-ready MVP has
> shipped** (DD-27). The path is not yet content-complete (the five interview-technique bodies land in
> Phase 12 Band 9) — this is a deliberate, documented gap, not an oversight. Safe to stop indefinitely.
> To resume: re-run the path-walk e2e.

---

## Group F — `immediately-effective/software-engineer-to-ai-engineer` (authoring priority #1, DD-27)

> Runs immediately after the interview-ready architecture smoke test and ahead of Groups C/D (D7/DD-27):
> nothing in this path exists on disk yet (~17 courses' worth of harness-cluster + AI-band content, of
> which six are entirely NEW), so ordering it first gives it first claim on every unit of authoring
> effort while the architecture is already proven against real content (Phase 6). See
> [tech-docs §Path `immediately-effective/software-engineer-to-ai-engineer`](./tech-docs.md#path-immediately-effectivesoftware-engineer-to-ai-engineer-fourth-path-added-2026-07-20)
> and [prd.md's AI-engineering specialization courses](./prd.md#ai-engineering-specialization-courses-software-engineer-to-ai-engineer-path-added-2026-07-20).

## Phase 7: Author the six net-new AI courses

> Each NEW course is authored as a full page-bundle into `<COURSES><course-id>/`. These six bodies are
> content-independent (each writes only its own subtree) and **pipeline concurrently** through review
> (bounded by the cap). Author each per the **NEW-course authoring convention** below. Per-course
> concept/example/prerequisite/capstone detail is **already settled** in
> [`syllabus/courses/`](./syllabus/courses/README.md) — each of the six courses has a complete,
> 295-425-line spec file (`evaluating-ai-output-essentials.md`, `evaluating-ai-systems-in-depth.md`,
> `statistics-for-evaluation.md`, `product-patterns-for-probabilistic-systems.md`,
> `inference-serving-and-model-deployment.md`, `fine-tuning-and-adaptation.md`) with concrete `co-NN`
> concept enumeration, `ex-NN` worked examples, a concrete prerequisite chain, and a capstone spec —
> these are the **source of truth** for authoring the actual
> `apps/ayokoding-www/content/en/learn/courses/<id>/` bundle; author each course body **from** its
> `syllabus/courses/<id>.md` spec, not from a fresh judgment call.
> [prd.md's AI-engineering specialization courses](./prd.md#ai-engineering-specialization-courses-software-engineer-to-ai-engineer-path-added-2026-07-20)
> retains a narrative summary drawn from those same settled specs.
>
> Every course below is split into a **stable spine** and **dated accuracy-note sidebars** (volatile
> SDK/model/pricing/framework specifics), matching the pattern the existing AI-band courses already use
> (DD-28's durability constraint) — this is an explicit authoring requirement, not optional polish.

**NEW-course authoring convention** (apply to each course sub-phase; identical in shape to the
convention this plan uses for every other NEW course — restated here since it first appears in this
phase, Phase 6's predecessor "Author the four interview courses" step having been deferred to Phase 12
Band 9, DD-27):

1. [AI] **V (accuracy pre-verify)** — spot-check version-pinned / market / pre-1.0-stack facts via
   `web-researcher`; per DD-28's durability constraint this applies with extra weight here — volatile
   SDK/model/pricing/framework facts belong ONLY in dated accuracy-note sidebars, never the stable
   spine — acceptance: no version-pinned claim written `[Unverified]`; every volatile fact sits in an
   accuracy-note sidebar, not the spine.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` with `prerequisites: [...]` +
   `overview.md` + `learning/_index.md` + `drilling/_index.md`), mirroring the matching sibling bundle
   shape; the `course-id` slug and prerequisite-linking targets are **settled** — use the exact
   course-id and prerequisite chain declared in the matching `syllabus/courses/<id>.md` spec file, not
   a fresh decision — acceptance: `test -d` passes for folder + `learning/` + `drilling/`;
   `prerequisites` declared (the shared software-engineer-fundamentals prerequisites this path assumes
   are **linked, not included** in the manifest per DD-24 — that constraint governs Phase 9, not this
   skeleton step).
3. [AI] **Author learning track** — `overview.md` (purpose + `## Prerequisites` naming only earlier
   library courses + register per prd), concept coverage, example/scenario pages + colocated `code/`
   where code-bearing, and `learning/capstone/`; the concept-coverage floor and example volume are
   **settled** in the matching `syllabus/courses/<id>.md` spec file's `co-NN`/`ex-NN` enumeration —
   author from that spec, not a fresh judgment call — acceptance: the course's own `overview.md` states
   its scope boundary against any sibling AI-band course it could be confused with (deep evals vs.
   light eval gate; statistics-for-evals vs. `analytics-and-experimentation`).
4. [AI] **Author drilling track** — `drilling/_index.md` + `drilling/overview.md` in the fixed
   five-section order — acceptance: all five sections present.
5. [AI] **Run content checkers** — run the matching learning checker, `apps-ayokoding-www-facts-checker`,
   and `apps-ayokoding-www-link-checker` (plus `apps-ayokoding-www-general-checker` on
   `drilling/overview.md`) — acceptance: findings recorded. _(Content authoring is a
   maker-checker-fixer cycle, not code TDD — no RED/GREEN/REFACTOR labels; see steps 6-7.)_
6. [AI] **Apply content fixers** — resolve every CRITICAL/HIGH/MEDIUM finding via the matching fixer —
   acceptance: every finding addressed.
7. [AI] **Re-verify** — re-run checkers + `npx nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; build + lint exit 0.

Each course below is its own sub-phase (own branch → draft PR → 3-cycle review → `[AI]` merge →
deploy), applying the convention:

- [ ] [AI] Light eval gate (`evaluating-ai-output-essentials` — Annotated-concept, Python, settled per
      [`syllabus/courses/evaluating-ai-output-essentials.md`](./syllabus/courses/evaluating-ai-output-essentials.md))
      — sits right after the first working LLM call, before RAG/agents; answers "how will you know this
      works?" (D5/DD-25) — acceptance: all 7 convention steps complete; checkers report zero
      CRITICAL/HIGH/MEDIUM; its overview states the scope boundary against the deep-evals course.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Deep evals (`evaluating-ai-systems-in-depth` — By Example, Python, settled per
      [`syllabus/courses/evaluating-ai-systems-in-depth.md`](./syllabus/courses/evaluating-ai-systems-in-depth.md))
      — sits after agents; error analysis, task-specific criteria, LLM-as-judge with measured human
      agreement, CI gating, judge-scope reliability (D5/DD-25); declares `statistics-for-evaluation` a
      **hard prerequisite** — acceptance: all 7 convention steps complete; checkers report zero
      CRITICAL/HIGH/MEDIUM; its overview states the scope boundary against the light eval gate.

  **Gherkin (binds) →** "The light eval gate and deep evals course do not overlap"

  ```gherkin
  Scenario: The light eval gate and deep evals course do not overlap
    Given the light-eval-gate course and the deep-evals course are authored
    When a reader compares their overviews
    Then each overview states an explicit scope boundary against the other
    And neither course re-teaches the material the other owns
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] Statistics for evals (`statistics-for-evaluation` — Annotated-concept, code-bearing, Python,
      settled per
      [`syllabus/courses/statistics-for-evaluation.md`](./syllabus/courses/statistics-for-evaluation.md))
      — scoped tightly to what evals demand (judge concordance, significance testing), not a general
      statistics survey (D6/DD-26); is a **hard prerequisite** of `evaluating-ai-systems-in-depth`, so
      it must be authored before (or in the same review cycle as) the deep-evals course —
      acceptance: all 7 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.

  **Gherkin (binds) →** "The statistics-for-evals course stays scoped to what evals demand"

  ```gherkin
  Scenario: The statistics-for-evals course stays scoped to what evals demand
    Given the statistics-for-evals course is authored
    When a reader compares it with analytics-and-experimentation
    Then it covers judge concordance and significance testing for evals only
    And it does not re-teach general product A/B testing, which stays analytics-and-experimentation's scope
  ```

  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_

- [ ] [AI] Product patterns for probabilistic systems (`product-patterns-for-probabilistic-systems` —
      Annotated-concept, no code, settled per
      [`syllabus/courses/product-patterns-for-probabilistic-systems.md`](./syllabus/courses/product-patterns-for-probabilistic-systems.md))
      — product design patterns for probabilistic (not deterministic) outputs; no course owns this
      today (DD-28) — acceptance: all 7 convention steps complete; checkers report zero
      CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Inference serving and model deployment (`inference-serving-and-model-deployment` — By
      Example, Python, settled per
      [`syllabus/courses/inference-serving-and-model-deployment.md`](./syllabus/courses/inference-serving-and-model-deployment.md))
      — vLLM/TGI, KV-cache, batching, GPU considerations; entirely absent from the library today
      (DD-28) — acceptance: all 7 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Fine-tuning and adaptation (`fine-tuning-and-adaptation` — By Example, Python, settled per
      [`syllabus/courses/fine-tuning-and-adaptation.md`](./syllabus/courses/fine-tuning-and-adaptation.md))
      — fine-tuning/LoRA/PEFT versus RAG as a foil (DD-28) — acceptance: all 7 convention steps
      complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] **Add catalog rows** — replace `tech-docs.md`'s Course Library Catalog by-name-only
      placeholder for these six courses with real rows (course-id · origin `N` · format · primary
      language · prerequisites · one-line scope) and update `<COURSES>_index.md` to list all six —
      acceptance: six new rows present in
      [tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog); `<COURSES>_index.md`
      link-checker green.

### Phase 7 Gate

- [ ] [AI] All six AI courses live under `<COURSES>` with declared prerequisites; each passed its checker + facts + link checkers; each states its scope boundary against any course it could be confused with.
- [ ] [AI] Every course's volatile facts sit in dated accuracy-note sidebars, not the stable spine (DD-28 durability constraint).
- [ ] [AI] Six new rows added to `tech-docs.md`'s Course Library Catalog; `<COURSES>_index.md` updated.
- [ ] [AI] `npx nx run ayokoding-www:build` + link + heading + markdownlint green.
- [ ] [AI] Every course sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the library now holds the 33 shipped topics + 4 existing capstones + the six new AI
> courses, all at canonical URLs; no AI-path manifest published yet, so all render the canonical view.
> Safe to stop. To resume: re-run the section build + link validation.

---

## Phase 8: Course surgery — evals scope contract, D9 naming/citation, D11 concept additions (four-path blast-radius)

> **Sequencing note (follows directly from D7/DD-27's own build order, not invented here):** the evals
> donor courses (`creating-ai-powered-apps`, `agentic-ai`,
> `agent-orchestration-subagents-and-observability`) and the D9/D11 target courses (the harness cluster:
> `the-agent-loop`, `agent-tools-and-mcp`, `agent-context-and-memory`,
> `agent-permissions-and-sandboxing`, `agent-orchestration-subagents-and-observability`, plus
> `capstone-build-your-own-coding-agent`) are **not yet authored anywhere in `apps/ayokoding-www/content`
> at this point in the build order** (verified by direct search: zero hits) — they are native-authored in
> Phase 12 Band 5 (the harness cluster + the evals donors) and Band 8
> (`capstone-build-your-own-coding-agent`, which assembles the harness cluster). DD-28's "trim the three
> donors to forward-links" therefore cannot be a file-edit
> action here; there is nothing yet to edit. This phase instead **locks the contract** those future
> authoring steps must honor, and **bakes its acceptance criteria into Phase 12 Band 5** (see that
> phase's bullets below) so the surgery is applied by construction — authored correctly from the start —
> rather than as a later retrofit.

- [ ] [AI] **State the four-path blast radius (DD-28 binding rule)** — for the evals extraction (D8),
      the D9 naming/citation additions, and the D11 concept additions, name every course and every
      manifest each touches: the evals extraction touches `deep-evals` (this plan, Phase 7, done) plus
      the three not-yet-authored donor courses (Phase 12 Band 5), and the `fundamentally-strong` and
      `immediately-effective` manifests that will carry those donors once grown (the AI path's own
      manifest already carries `deep-evals` from Phase 9); the D9/D11 additions touch only the harness
      cluster (Phase 12 Band 5) + `capstone-build-your-own-coding-agent` (Phase 12 Band 8) and every
      manifest that carries those course IDs — the same two software-engineer-role manifests, plus the
      fourth path's manifest once Band 5/8 grow it to include the harness cluster (DD-33) — acceptance:
      the blast radius is written into this delivery checklist (the two clauses above) before any of
      the three surgeries is considered "applied".
- [ ] [AI] **Lock the evals forward-link contract** — record, for Phase 12 Band 5's authoring of
      `creating-ai-powered-apps`, `agentic-ai`, and `agent-orchestration-subagents-and-observability`,
      that each course's evals-adjacent material MUST forward-link to the `deep-evals` course rather than
      re-teaching it, in the style of the existing AI-band scope-guard (DD-11) — acceptance: this
      requirement is added as an explicit acceptance criterion on each of the three courses' Phase 12
      Band 5 checklist items; `grep -c "deep-evals" <course>/overview.md` returns **0** today for all
      three (none authored yet — falsifiable both ways: each must return ≥1 once Band 5 lands that
      course).
- [ ] [AI] **Lock the D9 naming/citation contract** — record, for Phase 12 Band 5's authoring of
      `agent-context-and-memory`, that it MUST include a naming/lineage line citing Lütke (2025-06-19),
      Karpathy (2025-06-25), Willison (2025-06-27), and Anthropic's Effective Context Engineering
      methodology (2025-09-29); and for the harness cluster (Band 5) + `capstone-build-your-own-coding-agent`
      (Band 8), that they MUST include the harness-engineering equivalent citing Anthropic (2025-11-26),
      OpenAI, and Böckeler/Thoughtworks (2026-04-02) — **no course is renamed** (D9 is explicit: "harness
      engineering" is unsettled terminology; cite the disagreement, do not resolve it or adopt a side as
      structure) — acceptance: these citation requirements are added as explicit acceptance criteria on
      the relevant Phase 12 Band 5 and Band 8 checklist items.
- [ ] [AI] **Lock the D11 concept-addition contract** — record, for Phase 12 Band 5's authoring, the four
      concept-level additions: cache-aware prefix ordering (framed as a general stable-before-variable
      principle, not tied to one vendor's mechanism) → `agent-context-and-memory`; tool-count degradation + tool-result token efficiency → `agent-tools-and-mcp`; train-vs-production permission asymmetry
      (framed as a risk distinction, not a capability distinction) → `agent-permissions-and-sandboxing`
      — acceptance: each concept is added as an explicit acceptance criterion on the relevant Phase 12
      Band 5 checklist item, naming the concept and its target course.
- [ ] [AI] **Re-verify manifests prerequisite-consistent to date** — re-run `checkManifestIntegrity` +
      `checkPrerequisiteConsistency` across every manifest published so far
      (`interview-ready/software-engineer` from Phase 6) — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0; no violation introduced by this phase's contract-locking, which is
      documentation-only (no manifest file changes here). The AI path's own manifest (Phase 9, not yet
      authored) is re-verified in that phase's own gate.

### Phase 8 Gate

- [ ] [AI] Four-path blast radius stated for all three surgeries (evals extraction, D9, D11); forward-link, citation, and concept-addition contracts locked as explicit Phase 12 Band 5 acceptance criteria.
- [ ] [AI] "Harness engineering" is cited, not adopted as structure — no course renamed (D9).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 (manifest integrity unaffected by this documentation-only phase).
- [ ] [AI] Draft PR opened (this phase's PR touches only this delivery checklist's own text — no app content changes); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: the evals/D9/D11 contracts are locked and will be enforced when Phase 12 Band 5
> authors their target courses; no app content changed in this phase. Safe to stop. To resume: re-read
> this phase's four bullets and confirm Phase 12 Band 5 still carries the matching acceptance criteria.

---

## Phase 9: Author the `immediately-effective/software-engineer-to-ai-engineer` manifest + landing + wire + smoothness (AI path ships)

> _Suggested executor: `apps-ayokoding-www-general-maker` (manifest/landing) + `web-researcher` (smoothness facts)._
> Authored **behind** the interview-ready MVP and **ahead of** Groups C/D (D7/DD-27) — this is the
> second shippable path. Per **DD-33**, this path's full manifest composition is **15 courses**: the
> existing 9-course AI/harness cluster **walked** directly, plus the six new AI-engineer-role courses.
> The 9 harness-cluster course bodies are not authored until Phase 12 Band 5/Band 8 (Group E), so this
> phase ships the manifest **smoke-test-scoped** to `courseOrder` = **the six new AI courses only**
> (the only spine members whose bodies exist by this phase) — mirroring the same partial-ship pattern
> Group B's Phase 6 already uses for its own deferred courses. The manifest **grows** to the full 15 at
> Phase 12 Band 5/Band 8 (see that phase's growth step). The six new courses' settled order — light
> eval gate → statistics for evals → deep evals → product patterns for probabilistic systems →
> inference serving and model deployment → fine-tuning and adaptation — is per the already-authored
> [`syllabus/paths/manifest-immediately-effective-software-engineer-to-ai-engineer.md`](./syllabus/paths/manifest-immediately-effective-software-engineer-to-ai-engineer.md),
> which also fixes the eventual full 15-course ordering. The shared software-engineer-**fundamentals**
> prerequisites this path assumes are **linked, not included** (DD-24 — scoped to SWE-fundamentals
> only, not the harness cluster, DD-33) — they never appear in `courseOrder`.

- [ ] [AI] Author the manifest **data file**
      `<MANIFESTS>immediately-effective/software-engineer-to-ai-engineer.yaml`: `pathId:
immediately-effective/software-engineer-to-ai-engineer`, `title`, `description`, and the ordered
      `courseOrder` = the six new AI courses, smoke-test-scoped (DD-33 — the harness-cluster courses
      this path's full 15-course composition also walks are not authored until Phase 12 Band 5/8),
      ordered per the settled order in
      [tech-docs §Path `immediately-effective/software-engineer-to-ai-engineer`](./tech-docs.md#path-immediately-effectivesoftware-engineer-to-ai-engineer-fourth-path-added-2026-07-20)
      and the already-authored
      [manifest mirror](./syllabus/paths/manifest-immediately-effective-software-engineer-to-ai-engineer.md)
      (light eval gate → statistics for evals → deep evals → product patterns for probabilistic
      systems → inference serving and model deployment → fine-tuning and adaptation)
      — acceptance: the manifest loads + validates (`npx nx run ayokoding-www:test:unit` exits 0); NO
      shared software-engineer-fundamentals course ID (e.g. `just-enough-typescript`,
      `backend-essentials`, `api-design`) appears anywhere in `courseOrder` —
      `grep -cE "just-enough-typescript|backend-essentials|api-design" <MANIFESTS>immediately-effective/software-engineer-to-ai-engineer.yaml`
      returns **0** (falsifiable both ways: a manifest that mistakenly included one of these would make
      this return ≥1).

  **Gherkin (binds) →** "The AI path is authored before the other two manifests are composed"

  ```gherkin
  Scenario: The AI path is authored before the other two manifests are composed
    Given the interview-ready MVP has shipped
    When authoring effort is allocated across the remaining paths
    Then the software-engineer-to-ai-engineer path's six net-new courses and manifest are authored first
    And the immediately-effective/software-engineer and fundamentally-strong/software-engineer manifests are composed only afterward
  ```

- [ ] [AI] Author the thin landing anchor
      `<PATHS>immediately-effective/software-engineer-to-ai-engineer/_index.md` (prose/SEO only — no
      `courseOrder`); the ordered course list renders from the loaded manifest, and the landing narrative
      **links out** to the canonical pages of the prerequisite software-engineer courses this path
      assumes (DD-24) — acceptance: landing renders the manifest-ordered six-course list; at least one
      outbound link to a canonical `/en/c/learn/courses/<id>` page for a prerequisite software-engineer
      course is present in the landing prose.

  **Gherkin (binds) →** "The software-engineer-to-ai-engineer path links prerequisites instead of
  including them"

  ```gherkin
  Scenario: The software-engineer-to-ai-engineer path links prerequisites instead of including them
    Given the immediately-effective/software-engineer-to-ai-engineer path manifest is published
    When a reader inspects its courseOrder
    Then no shared software-engineering-fundamentals course from the other three manifests is included in courseOrder
    And the path landing page links out to those prerequisite courses' canonical pages instead
  ```

- [ ] [AI] Update `<PATHS>_index.md` (paths hub) so the fourth card (`SWE → AI Engineer`) is present in
      the 2×2 grid alongside `interview-ready`, per
      [prd.md Screen 1](./prd.md#screen-1--paths-hub-choose-your-path) — acceptance: hub shows both
      published paths (two of the four cards populated).
- [ ] [AI] **Manifest integrity + prerequisite-consistency check** — every `courseOrder` ID resolves
      under `<COURSES>`; no duplicate ID; every declared prerequisite among the six new courses that is
      also in `courseOrder` appears earlier in the ordering — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] Verify path-aware nav end-to-end for this path: from the landing, prev/next walks the
      manifest order and preserves `?path=immediately-effective/software-engineer-to-ai-engineer`;
      breadcrumb shows the path; course pages show their prerequisites — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the path-walk e2e spec passes in `en`
      (this plan's content locale).
- [ ] [AI] **Progression smoothness audit (AI-transition-first, DD-16)** — walk the manifest order and
      confirm the levers hold (prereq-chaining; monotonic-ish difficulty; the light-eval-gate/deep-evals
      scope boundary from Phase 7 doesn't itself constitute a smoothness break) per
      [tech-docs §Smoothness Architecture](./tech-docs.md#smoothness-architecture-per-path) —
      acceptance: all levers verified; any regression fixed by soften/bridge in place, never reorder.

### Phase 9 Gate

- [ ] [AI] `immediately-effective/software-engineer-to-ai-engineer` manifest published (smoke-test-scoped six-course spine — grows to its full 15-course composition at Phase 12 Band 5/8, DD-33; SWE-fundamentals prerequisites linked, not included); integrity + prerequisite-consistency green; path-walk e2e + breadcrumb + prerequisite display green in `en` (this plan's content locale).
- [ ] [AI] Paths hub shows two of four cards; smoothness audit passes.
- [ ] [AI] Re-run `checkManifestIntegrity` + `checkPrerequisiteConsistency` across all published manifests to date (`interview-ready`, `immediately-effective/software-engineer-to-ai-engineer`) — exits 0 (closes out Phase 8's deferred cross-manifest check).
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0 (e2e lives in the paired `ayokoding-www-fe-e2e` project — `ayokoding-www:test:e2e` is a no-op echo and can never fail).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the `immediately-effective/software-engineer-to-ai-engineer` path is **live
> end-to-end** in production (landing + manifest + path-aware nav + prerequisites + smoothness) — **the
> AI path has shipped** (DD-27's authoring priority #1 is delivered). **Group F is complete.** Safe to
> stop indefinitely. To resume: re-run the path-walk e2e.

---

## Group C — immediately-effective manifest

## Phase 10: Author the `immediately-effective/software-engineer` manifest + landing + smoothness (zero new bodies)

> _Suggested executor: `apps-ayokoding-www-general-maker`._
> Adds **no new course body** — it composes existing library courses into the immediately-effective
> arc (editor → one language → **build a real app first** → then deepen). Authored over the
> currently-available library and **grows** during Phase 12 backfill as deeper courses land.

- [ ] [AI] Author the manifest **data file** `<MANIFESTS>immediately-effective/software-engineer.yaml`:
      `pathId: immediately-effective/software-engineer`, `title`, `description`, and the ordered
      `courseOrder` = the shipping-first arc from
      [tech-docs §Path `immediately-effective/software-engineer`](./tech-docs.md#path-immediately-effectivesoftware-engineer-build-fast-first)
      and [syllabus/paths/README.md](./syllabus/paths/README.md) — the arc places editor/tooling → one
      language end-to-end → **build a real app first** ahead of CS-fundamentals/DS&A/systems depth —
      acceptance: body duplication = 0 (references shared course IDs only); references only extant
      courses; manifest loads + validates (`npx nx run ayokoding-www:test:unit` exits 0).
- [ ] [AI] Author the thin landing anchor `<PATHS>immediately-effective/software-engineer/_index.md`
      (prose/SEO only — no `courseOrder`); the ordered course list renders from the loaded manifest —
      acceptance: landing renders the manifest-ordered arc.
- [ ] [AI] Update `<PATHS>_index.md` (paths hub) so the `immediately-effective` card is present
      alongside `interview-ready` and `SWE → AI Engineer` per
      [prd.md Screen 1](./prd.md#screen-1--paths-hub-choose-your-path) — acceptance: hub shows three of
      the four published paths.
- [ ] [AI] **Manifest integrity + prerequisite-consistency + no-forked-body check** — every
      `courseOrder` ID resolves; no dup ID; prereq-consistency holds; no body duplicated across
      manifests (all reference by ID) — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] Verify path-aware nav: prev/next walks the immediately-effective order and preserves
      `?path=immediately-effective/software-engineer`; a course shared with `interview-ready` shows the
      correct neighbor per active path — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance:
      e2e passes in `en` (this plan's content locale); a shared course's prev/next differs by active path.
- [ ] [AI] **Progression smoothness audit (shipping-first, DD-16)** — build-a-real-app precedes CS
      depth; the "you shipped; now understand why" bridge is present on the landing; prereq-chaining
      holds — acceptance: levers verified; regressions fixed by soften/bridge, never reorder.

  **Gherkin (binds) →** "The immediately-effective path is build-app-first"

  ```gherkin
  Scenario: The immediately-effective path is build-app-first
    Given the immediately-effective/software-engineer path manifest is published
    When a reader walks the path
    Then editor/tooling, one language end-to-end, and building a real app precede the CS-fundamentals and DS&A courses
    And the reader ships a real deployed app before any pure-theory course
  ```

### Phase 10 Gate

- [ ] [AI] `immediately-effective/software-engineer` manifest published (zero duplicated bodies, seeded over the available library); paths hub shows three of the four published paths.
- [ ] [AI] Integrity + prerequisite-consistency + no-forked-body checks green; per-path prev/next differs correctly for shared courses.
- [ ] [AI] Shipping-first smoothness audit passes.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0 (e2e lives in the paired `ayokoding-www-fe-e2e` project — `ayokoding-www:test:e2e` is a no-op echo and can never fail).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: three of the four paths are live over one shared library with zero body
> duplication. Safe to stop. To resume: re-run all path-walk e2e specs published so far.

---

## Group D — fundamentally-strong manifest

## Phase 11: Author the `fundamentally-strong/software-engineer` manifest + landing + smoothness (zero new bodies)

> _Suggested executor: `apps-ayokoding-www-general-maker`._
> The NEW university-style path (fundamentals/CS-theory FIRST → deeper). Adds **no new course body** —
> composes existing library courses. Authored over the currently-available library and **grows** during
> Phase 12 backfill.

- [ ] [AI] Author the manifest **data file** `<MANIFESTS>fundamentally-strong/software-engineer.yaml`:
      `pathId: fundamentally-strong/software-engineer`, `title`, `description`, and the ordered
      `courseOrder` = the fundamentals-first arc from
      [tech-docs §Path `fundamentally-strong/software-engineer`](./tech-docs.md#path-fundamentally-strongsoftware-engineer-theory-first)
      and [syllabus/paths/README.md](./syllabus/paths/README.md) — the arc places
      CS-foundations/computer-architecture/paradigms/DS&A/theory FIRST, then systems/architecture depth
      — acceptance: body duplication = 0 (references shared course IDs only); references only extant
      courses; manifest loads + validates (`npx nx run ayokoding-www:test:unit` exits 0).
- [ ] [AI] Author the thin landing anchor `<PATHS>fundamentally-strong/software-engineer/_index.md`
      (prose/SEO only — no `courseOrder`); the ordered course list renders from the loaded manifest —
      acceptance: landing renders the fundamentals-first arc.
- [ ] [AI] Update `<PATHS>_index.md` (paths hub) so **all four** path cards are present, completing the
      2×2 grid, per [prd.md Screen 1](./prd.md#screen-1--paths-hub-choose-your-path) — acceptance: hub
      shows all four paths.
- [ ] [AI] **Manifest integrity + prerequisite-consistency + no-forked-body check** across all four
      manifests (the three software-engineer-role manifests share bodies by ID; the AI path's manifest
      links rather than includes shared bodies per DD-24, so it never triggers a forked-body finding) —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] Verify path-aware nav: prev/next walks the fundamentals-first order and preserves
      `?path=fundamentally-strong/software-engineer`; a course shared across paths shows the correct
      neighbor per active path — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: e2e passes
      in `en` (this plan's content locale); a shared course's prev/next differs by active path.
- [ ] [AI] **Progression smoothness audit (fundamentals-first, DD-16)** — theory precedes application;
      the "why-before-how" bridges are present; prereq-chaining holds — acceptance: levers verified;
      regressions fixed by soften/bridge, never reorder.

  **Gherkin (binds) →** "The fundamentally-strong path is fundamentals-first"

  ```gherkin
  Scenario: The fundamentally-strong path is fundamentals-first
    Given the fundamentally-strong/software-engineer path manifest is published
    When a reader walks the path
    Then CS foundations, computer architecture, paradigms, and DS&A precede the build-real-software courses
    And the ordering is a valid topological entry into the prerequisite DAG
  ```

### Phase 11 Gate

- [ ] [AI] `fundamentally-strong/software-engineer` manifest published (zero duplicated bodies, seeded over the available library); paths hub shows all four paths.
- [ ] [AI] Integrity + prerequisite-consistency + no-forked-body checks green across all four manifests; per-path prev/next differs correctly for shared courses.
- [ ] [AI] Fundamentals-first smoothness audit passes.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0 (e2e lives in the paired `ayokoding-www-fe-e2e` project — `ayokoding-www:test:e2e` is a no-op echo and can never fail).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: all four paths are live over one shared library (zero body duplication among the
> three software-engineer-role paths; the AI path links rather than duplicates). The four-path product
> skeleton is complete. Safe to stop. To resume: re-run all four path-walk e2e specs.

---

## Group E — Backfill (topics 34–94 native + remaining new courses)

## Phase 12: Author the 61 transferred topics + 10 remaining new courses + 8 remaining capstones + 5 deferred interview-technique bodies NATIVE; grow the three software-engineer-role manifests

> Each body is authored NATIVE into `<COURSES><course-id>/` (no legacy home, no re-home) per the
> **NEW-course authoring convention** from Phase 7 (V → skeleton with `prerequisites` → learning →
> drilling → content checkers → content fixers → re-verify — see Phase 7's convention note on why
> this uses maker-checker-fixer labels, not RED/GREEN/REFACTOR). These 84 bodies (the original 79 —
> 61 transferred + 10 remaining new courses + 8 remaining capstones — plus **Band 9's 5 deferred
> interview-technique bodies**, DD-27) are content-independent and **pipeline concurrently** through
> review (bounded by the cap). As each **band** lands, **grow** the affected manifests (append the
> newly-available courses into whichever paths include them; re-run integrity +
> prerequisite-consistency) — a serial sync point per band; Bands 1–8 grow all three
> software-engineer-role manifests, Band 9 grows only `interview-ready` and `fundamentally-strong` (see
> Band 9's own growth step below). Per-course detail: [syllabus courses layer](./syllabus/courses/README.md)
> and the tracked [Course Library Catalog](./tech-docs.md#course-library-catalog) (the 127-course total;
> Bands 1–9 below author their table rows as part of "convention complete" — do **not** depend on any
> `local-temp/` scratch file here; those are gitignored and may be cleaned before this phase runs).
>
> This phase also **applies** the three contracts Phase 8 locked (evals forward-link, D9 naming/
> citation, D11 concept additions) — see each contract's target course in Band 5 below, now carrying an
> explicit acceptance criterion sourced from that phase.
>
> **Reconciliation rulings baked into authoring** (locked):
>
> - `defensive-security` is **By-Example hands-on** (Sigma/ELK/OpenSearch + IR + hardening) — author
>   it that way; the catalog's "(concept)" label is WRONG. `detection-engineering-and-siem-operations`
>   owns the deep Wazuh decoder/rule/FP-tuning/dashboard tier and declares `defensive-security` a
>   prerequisite; draw the scope line explicitly.
> - **AI-band scope-guard**: `creating-ai-powered-apps` (use-an-LLM-in-an-app) → `agentic-ai` (a single
>   survey that **forward-links each primitive to its harness-cluster course** and does NOT re-teach at
>   build-your-own depth) → the 5-course harness cluster (build-your-own depth). Bake the cross-reference contract in.
> - `async-python-and-fastapi-services` stays framework-concrete: defer async _concepts_ to
>   `concurrency-and-parallelism` and framework _internals_ to `build-your-own-web-framework`; cross-link both.

**Band 1 — Data depth (T):**

- [ ] [AI] `nosql-databases` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `graph-databases` (By Example · Cypher + Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `database-internals-and-storage-engines` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `data-engineering` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `search-and-information-retrieval` (By Example · Python) — convention complete; checkers clean. _by-example-maker_

**Band 2 — Web, backend & platform productivity (T + N):**

- [ ] [AI] `api-design` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `advanced-frontend` (By Example · TypeScript) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `backend-at-scale` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `async-python-and-fastapi-services` (By Example · Python; framework-concrete scope note) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `self-hosting-essentials` (By Example · ops/config) — convention complete; checkers clean. _by-example-maker_
      **Gherkin (binds) →** "The light self-hosting course stays below clusters and IaC"
      — scope-boundary acceptance: the course teaches running one box, containerizing a service, a
      reverse proxy, and PaaS git-push deploy; and its overview **explicitly excludes** clusters,
      Terraform/Packer/Ansible IaC, and Proxmox — verify with
      `grep -ciE 'cluster|terraform|packer|ansible|proxmox' <course>/overview.md` (ERE alternation) returning ≥1
      (the exclusions must be _stated_, not merely absent), and no lesson body teaching them.
- [ ] [AI] `containers-and-orchestration` (By Example · YAML/CLI) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `cloud-and-iac` (Annotated-concept · HCL/YAML) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `cicd-and-release-engineering` (By Example · YAML + Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-automation-and-task-runners` (By Example · multi-tool) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `information-architecture-and-seo` (Annotated-concept · HTML) — convention complete; checkers clean. _annotated-concept-maker_

**Band 3 — Mobile & desktop platforms (T):**

- [ ] [AI] `just-enough-kotlin` (Primer · Kotlin) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `android-app-development` (By Example · Kotlin) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-swift` (Primer · Swift) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `ios-app-development` (By Example · Swift) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-dart` (Primer · Dart) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `hybrid-app-development` (By Example · Dart) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-csharp` (Primer · C#) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `windows-app-development` (By Example · C#) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `linux-app-development` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `building-production-cli-tools` (By Example · Go + Rust) — convention complete; checkers clean. _by-example-maker_

**Band 4 — Concurrency languages (T):**

- [ ] [AI] `just-enough-go` (Primer · Go) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `csp-style-concurrency` (By Example · Go) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-elixir` (Primer · Elixir) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `actor-model-concurrency` (By Example · Elixir) — convention complete; checkers clean. _by-example-maker_

**Band 5 — Architecture, distributed & AI/harness (T + N):**

- [ ] [AI] `software-architecture` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `domain-driven-design` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `system-design` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `event-driven-architecture` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `distributed-systems` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-web-framework` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-reactive-ui` (By Example · TypeScript) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `creating-ai-powered-apps` (By Example · Python; use-an-LLM scope) — convention complete; checkers clean; **Phase 8 evals forward-link contract applied**: `grep -c "deep-evals" creating-ai-powered-apps/overview.md` returns ≥1 (its evals material forward-links to `deep-evals` rather than re-teaching it, DD-25/DD-28). _by-example-maker_
- [ ] [AI] `agentic-ai` (By Example · Python; survey + forward-links, no build-your-own depth) — convention complete; checkers clean; **Phase 8 evals forward-link contract applied**: `grep -c "deep-evals" agentic-ai/overview.md` returns ≥1. _by-example-maker_
      **Gherkin (binds) →** "The agentic-ai survey forward-links each primitive without re-teaching it"
      — forward-link acceptance: `agentic-ai/overview.md` names and links each of the five
      harness-cluster courses (`the-agent-loop`, `agent-tools-and-mcp`, `agent-context-and-memory`,
      `agent-permissions-and-sandboxing`, `agent-orchestration-subagents-and-observability`) — verify
      with
      `grep -ciE 'the-agent-loop|agent-tools-and-mcp|agent-context-and-memory|agent-permissions-and-sandboxing|agent-orchestration-subagents-and-observability' agentic-ai/overview.md`
      (ERE alternation) returning ≥5 distinct lines, and no lesson in `agentic-ai/` builds a working
      agent-loop/tool/memory/permission/orchestration implementation (that depth stays in the cluster
      courses).
- [ ] [AI] `browser-automation-with-cdp` (By Example · Python/CDP) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `the-agent-loop` (By Example · Python) — convention complete; checkers clean; **Phase 8 D9 citation contract applied**: harness-engineering naming/lineage line present, citing Anthropic (2025-11-26), OpenAI, and Böckeler/Thoughtworks (2026-04-02) — no rename. _by-example-maker_
- [ ] [AI] `agent-tools-and-mcp` (By Example · Python) — convention complete; checkers clean; **Phase 8 D9 + D11 contracts applied**: harness-engineering citation line present; concept coverage includes tool-count degradation (Berkeley Function-Calling Leaderboard + GeoEngine 46-vs-19-tool evidence) and tool-result token efficiency. _by-example-maker_
- [ ] [AI] `agent-context-and-memory` (Annotated-concept · Python) — convention complete; checkers clean; **Phase 8 D9 + D11 contracts applied**: context-engineering naming/lineage line present, citing Lütke (2025-06-19), Karpathy (2025-06-25), Willison (2025-06-27), and Anthropic's Effective Context Engineering methodology (2025-09-29); concept coverage includes cache-aware prefix ordering framed as a general stable-before-variable principle, not tied to one vendor's mechanism. _annotated-concept-maker_
- [ ] [AI] `agent-permissions-and-sandboxing` (By Example · Python) — convention complete; checkers clean; **Phase 8 D11 contract applied**: concept coverage includes the train-vs-production permission asymmetry, framed as a risk distinction, not a capability distinction. _by-example-maker_
- [ ] [AI] `agent-orchestration-subagents-and-observability` (Annotated-concept · Python) — convention complete; checkers clean; **Phase 8 evals forward-link contract applied**: `grep -c "deep-evals" agent-orchestration-subagents-and-observability/overview.md` returns ≥1. _annotated-concept-maker_
      **Gherkin (binds) →** "The harness cluster builds a working agent from runnable code"
      — runnable-example acceptance: each of the five harness-cluster courses above (`the-agent-loop`,
      `agent-tools-and-mcp`, `agent-context-and-memory`, `agent-permissions-and-sandboxing`,
      `agent-orchestration-subagents-and-observability`) ships a runnable typed-Python worked example
      covering its slice of the loop/tools/memory/permissions/orchestration, and each names
      `remotebrowser`'s bundled MCP or CDP browser only as an illustrative pickup, never a required
      dependency — verified during each course's checker pass (the by-example-maker/
      annotated-concept-maker convention already requires runnable examples; this bind adds the
      remotebrowser-scope check).

**Band 6 — Low-level systems, JVM & languages, internals builds (T + N):**

- [ ] [AI] `just-enough-c` (Primer · C) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `just-enough-cpp` (Primer · C++; prereq `just-enough-c`) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `linux-os` (By Example · C + shell) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `windows-os` (By Example · C + PowerShell) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `system-programming` (By Example · C) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-rust` (Primer · Rust) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `modern-system-programming` (By Example · Rust) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-java` (Primer · Java) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `enterprise-java-and-the-jvm` (By Example · Java) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `lisp` (By Example · Scheme + Clojure) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-fsharp` (Primer · F#) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `type-systems` (By Example · OCaml + Haskell + F#) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `compilers-parsers-and-transpilers` (By Example · F#) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-git` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-database` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-raft` (By Example · Go) — convention complete; checkers clean. _by-example-maker_

**Band 7 — Security, ops, quality & delivery (T + N):**

- [ ] [AI] `it-and-application-security` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `offensive-security` (By Example · Python + shell) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `defensive-security` (By Example · Python + shell; hands-on, NOT concept) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `detection-engineering-and-siem-operations` (By Example · XML/rules + config + Python; prereq `defensive-security`) — convention complete; checkers clean. _by-example-maker_
      **Gherkin (binds) →** "Hands-on detection engineering stays distinct from generalist defensive security"
      — distinctness acceptance: this course has the reader author working Wazuh decoders, correlation
      rules, and a dashboard with false-positive tuning; and `defensive-security` retains the
      generalist Sigma/ELK breadth, IR, and hardening as its distinct scope — verify no lesson title
      is duplicated across the two courses' syllabi.
- [ ] [AI] `vulnerability-management-and-assessment` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `it-governance-grc` (Annotated-concept · no code) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `bare-metal-virtualization` (By Example · HCL/YAML/shell) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `self-managed-kubernetes-and-gitops` (By Example · YAML/CLI) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `platform-engineering-and-devex` (Annotated-concept · no code) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `site-reliability-engineering` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `analytics-and-experimentation` (By Example · Python) — convention complete; checkers clean. _by-example-maker_

**Band 8 — Remaining capstones (N, incl. six DD-20 inter-topic capstones):**

- [ ] [AI] `capstone-build-your-own-coding-agent` (Python; assembles the harness cluster) — convention complete; checkers clean; **Phase 8 D9 citation contract applied**: harness-engineering naming/lineage line present, citing Anthropic (2025-11-26), OpenAI, and Böckeler/Thoughtworks (2026-04-02) — no rename. _by-example-maker_
      **Gherkin (binds) →** "The coding-agent capstone assembles the harness cluster into a working CLI"
      — assembly acceptance: the capstone's done-bar produces a runnable coding-agent CLI composed from
      the agent loop, tools/MCP, memory, permissions, and orchestration courses; a disallowed action
      fails closed and every run emits a trace — verify with the capstone's own runnable
      acceptance-criteria checklist (per the capstone-policy shape) naming all five source courses.
- [ ] [AI] `capstone-build-your-own-pentest-engine` (TypeScript; swarm + MCP + CDP + security chaining) — convention complete; checkers clean. _by-example-maker_
      **Gherkin (binds) →** "The pentest-engine capstone assembles the convergence track into a scoped engine"
      — assembly acceptance: the capstone's done-bar produces a runnable engine composed from swarm
      orchestration, MCP tooling, CDP browser driving, and security-tool-chaining; scope enforcement
      refuses an out-of-scope target, and `vacti-pentest-engine` is named only as an illustration, never
      a required dependency — verify with the capstone's own runnable acceptance-criteria checklist.
- [ ] [AI] `capstone-real-world-delivery` (Python + TS + IaC; DD-20 — embedded spec in `defensive-security.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-secure-service` (Python + shell; DD-20 — embedded spec in `defensive-security.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-data-pipeline` (SQL + Python; DD-20 — embedded spec in `defensive-security.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-concurrency-and-systems` (Go or Elixir + C; DD-20 — embedded spec in `compilers-parsers-and-transpilers.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-concurrency-showdown` (Go + Elixir; DD-20 — embedded spec in `compilers-parsers-and-transpilers.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-lead-at-altitude` (polyglot + prose; DD-20 — embedded spec in `site-reliability-engineering.md`) — convention complete; checkers clean. _annotated-concept-maker_

**Band 9 — Deferred interview-technique courses (deferred from the interview-ready MVP gate, DD-27):**

- [ ] [AI] `coding-interview` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `take-home-and-live-coding` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `system-design-interview` (Annotated-concept · no code; forward-links `system-design`) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `behavioral-and-leadership-interviews` (Annotated-concept · no code) — convention complete; checkers clean.

  **Gherkin (binds) →** "The behavioral course covers the layoff and employment-gap narrative"; "Interview
  courses are written in a refresh register"
  — coverage acceptance: the learning track explicitly covers framing an employment gap, a layoff, and
  a re-entry story, and treats senior/staff/EM leadership rounds as core (not optional) material —
  verify with `grep -ciE 'employment gap|layoff|re-entry' <course>/**/*.md` (ERE alternation) returning
  ≥3 distinct lessons.
  — register acceptance (all four Band 9 courses: `coding-interview`, `take-home-and-live-coding`,
  `system-design-interview`, `behavioral-and-leadership-interviews`): each course's `overview.md`
  states it assumes prior professional experience and frames the material as technique/breadth
  refresh, never a from-zero concept teach — verify with
  `grep -ciE 'assumes|prior experience|refresh' <course>/overview.md` (ERE alternation) returning ≥1 for
  each of the four (returns 0 today since none of the four course directories exist yet).
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_

  ```gherkin
  Scenario: Interview courses are written in a refresh register
    Given the four new interview-technique courses are authored
    When an experienced engineer reads them
    Then each assumes prior professional experience and focuses on interview technique and breadth refresh
    And none teaches core concepts from zero
  ```

- [ ] [AI] `capstone-interview-loop` (Python + prose) — convention complete; checkers clean. _by-example-maker_

**Manifest growth (serial sync point after each band):**

- [ ] [AI] After each of Bands 1–8 lands, append its newly-available courses into the three
      software-engineer-role manifests
      (`<MANIFESTS>{interview-ready,immediately-effective,fundamentally-strong}/software-engineer.yaml`)
      per each path's arc, then re-run `checkManifestIntegrity` + `checkPrerequisiteConsistency` +
      no-forked-body — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0 after each
      growth.
- [ ] [AI] **Band 9 manifest growth (interview-ready + fundamentally-strong only)** — insert the five
      landed interview-technique courses into `<MANIFESTS>interview-ready/software-engineer.yaml`
      (closing the gap the Phase 6 smoke test deliberately left open) and
      `<MANIFESTS>fundamentally-strong/software-engineer.yaml` (its own trailing optional interview
      band, per
      [tech-docs §Path `fundamentally-strong/software-engineer`](./tech-docs.md#path-fundamentally-strongsoftware-engineer-theory-first)),
      each in its correct topological position; `immediately-effective/software-engineer` does **not**
      grow here — that path omits the interview-technique band from its `courseOrder` by design (its
      reader reaches these courses via their canonical pages, not the manifest) — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0; the falsifiable check Phase 6 opened
      now closes the other way —
      `grep -E "coding-interview|take-home-and-live-coding|system-design-interview|behavioral-and-leadership-interviews|capstone-interview-loop" <MANIFESTS>interview-ready/software-engineer.yaml`
      now returns all five lines; the same command against
      `<MANIFESTS>immediately-effective/software-engineer.yaml` still returns nothing.
- [ ] [AI] **Interview-ready smoothness re-audit (refresh-register lever, closes Phase 6's deferral)** —
      with the five interview-technique courses now in `courseOrder`, re-run the
      [smoothness audit](./tech-docs.md#smoothness-architecture-per-path)'s refresh-register lever that
      Phase 6 explicitly deferred — acceptance: the lever verified; any regression fixed by soften/bridge
      in place, never reorder.
- [ ] [AI] **AI-path manifest growth (Band 5 + Band 8, DD-33)** — once Band 5 lands the harness cluster
      (`creating-ai-powered-apps`, `agentic-ai`, `browser-automation-with-cdp`, `the-agent-loop`,
      `agent-tools-and-mcp`, `agent-context-and-memory`, `agent-permissions-and-sandboxing`,
      `agent-orchestration-subagents-and-observability`) and Band 8 lands
      `capstone-build-your-own-coding-agent`, insert all nine into
      `<MANIFESTS>immediately-effective/software-engineer-to-ai-engineer.yaml` in their correct
      topological position (per the already-authored
      [manifest mirror](./syllabus/paths/manifest-immediately-effective-software-engineer-to-ai-engineer.md)),
      growing the manifest from its Phase-9 smoke-test-scoped six-course spine to its full **15-course**
      composition — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0; the Phase 9
      falsifiable check now closes the other way —
      `grep -cE "the-agent-loop|agent-tools-and-mcp|agent-context-and-memory|agent-permissions-and-sandboxing|agent-orchestration-subagents-and-observability|capstone-build-your-own-coding-agent" <MANIFESTS>immediately-effective/software-engineer-to-ai-engineer.yaml`
      returns **0** before Band 5/8 land and returns **6** once they do.
- [ ] [AI] After the final band, confirm all three software-engineer-role manifests reference the
      intended full arcs (no omitted-by-mistake courses; omit-or-create honored) and the library holds
      the full **127-course** catalog (121 software-engineer-role baseline + the 6 AI courses authored in
      Phase 7) — command: `npx nx run ayokoding-www:build` — acceptance: 127 course bundles resolve; all
      four manifests validate (the AI path's own manifest has grown to its full 15-course composition by
      Band 5/Band 8, DD-33, and is re-validated here as the final confirmation).

### Phase 12 Gate

- [ ] [AI] All 61 transferred topics + 10 remaining new courses + 8 remaining capstones (2 original + 6 DD-20 inter-topic capstones) + the 5 deferred interview-technique bodies (Band 9, DD-27) authored NATIVE under `<COURSES>` with declared prerequisites; each passed its checker + facts + link checkers.
- [ ] [AI] Reconciliation rulings applied (defensive-security By-Example label; AI-band scope-guard; async-fastapi scope note); Phase 8's three locked contracts (evals forward-link, D9 citation, D11 concept additions) applied and verified on their target Band 5/Band 8 courses.
- [ ] [AI] The three software-engineer-role manifests grown to their full arcs (interview-ready and fundamentally-strong now carry Band 9's five interview-technique courses; immediately-effective does not); integrity + prerequisite-consistency + no-forked-body green; full 127-course library resolves.
- [ ] [AI] The fourth path's (`immediately-effective/software-engineer-to-ai-engineer`) manifest grown from its Phase 9 six-course smoke-test spine to its full 15-course composition (Band 5 harness cluster + Band 8 capstone, DD-33); integrity + prerequisite-consistency green.
- [ ] [AI] Interview-ready's refresh-register smoothness lever, deferred at Phase 6, now verified.
- [ ] [AI] `<COURSES>_index.md` catalog updated to the full 127; `npx nx run ayokoding-www:build` + link + heading + markdownlint green.
- [ ] [AI] Every band/course sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the full 127-course library exists and all four path manifests are complete over
> one shared library (zero body duplication among any of the four paths — the AI path walks the shared
> AI/harness cluster by ID (DD-33) and links out only its SWE-fundamentals prerequisites, DD-24). The
> whole four-path product is content-complete. Safe to stop. To resume: re-run the section build +
> integrity checks.

---

## Group Finalization

## Phase 13: Section & App Verification

- [ ] [AI] Run affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit test:integration test:e2e specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation),
      committing preexisting fixes separately.
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` +
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md` (the actual mechanism — not `nx run` targets; both `md` subcommands also run
      automatically pre-commit via `lint-staged` for every staged `.md` file) — acceptance: all green.

  **Gherkin (binds) →** "The app builds and validates green"

  ```gherkin
  Scenario: The app builds and validates green
    Given the navigation feature and the interview-ready path are complete
    When nx run ayokoding-www:build, the three test tiers, and the link/heading validators run
    Then the build and all tiers succeed
    And link, heading-hierarchy, and markdownlint validation report no errors
  ```

- [ ] [AI] **Manifest-integrity + prerequisite-consistency sweep** — all four manifests: every
      `courseOrder` ID resolves; no dup ID; prereq-consistency holds; no forked body across the three
      software-engineer-role paths (the AI path links rather than shares bodies, DD-24) —
      acceptance: integrity check reports zero violations across all four.
- [ ] [AI] **All-path smoothness re-check (DD-16)** — re-verify the levers for each manifest in the
      landed content — acceptance: all four paths pass.
- [ ] [AI] **Three-bucket structural sweep (Group L, DD-40)** — `ls apps/ayokoding-www/content/en/learn`
      lists exactly `_index.md`, `courses`, `legacy`, `overview.md`, `paths` and nothing else, AND
      `find apps/ayokoding-www/content/en/learn/legacy -name '*.md' | wc -l` still returns **1148**, AND
      `find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l` still returns **53** with no
      bucket directory (`test -e apps/ayokoding-www/content/id/belajar/legacy` returns non-zero, DD-45)
      — acceptance: all four checks hold. Falsifiable both ways: before Phase 5A the `ls` lists seven
      domain directories and the `find` under `legacy/` fails outright.
- [ ] [AI] **Redirect-order regression check (DD-42)** — `apps/ayokoding-www/next.config.ts` still
      spreads `learnThreeBucketRedirects` **between** `learnReorgRedirects` and
      `contentNamespaceRedirects`, and `npx nx run ayokoding-www:test:unit` passes the
      `learn-three-bucket` negative assertions (no blanket source; no `courses`/`paths`/
      `fundamentally-strong` source prefix) — acceptance: both hold.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 13 Gate

- [ ] [AI] Affected `typecheck/lint/test:quick/test:unit/test:integration/test:e2e/specs:behavior:coverage` exit 0.
- [ ] [AI] Build + link + heading + markdown validation green; manifest integrity + prerequisite-consistency + all-path smoothness pass.
- [ ] [AI] Three-bucket structural sweep green (exactly three buckets + two hub files; 1148 legacy `.md`; `id/belajar` untouched at 53) and the redirect ordering + negative assertions still hold.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the whole four-path product passes all automated gates. Safe to stop. To resume:
> re-run the affected quality gates + build.

---

## Phase 14: Manual UI Verification + Rule-15 Three-Tester Retest

> Path-aware navigation is a user-facing change, so a live-site retest is required before archival.
> **Locale scope**: this plan's course/path content is authored `en`-only — per
> [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals), an Indonesian content mirror
> is explicitly deferred. Retest content screens (paths hub, path landings, course pages) in `en`
> only; do not fabricate an `id` content walk-through for a feature with no `id` content. The
> path-aware nav UI code itself remains locale-neutral (it renders whatever locale-specific content
> exists), so this scoping is a content-availability fact, not a code limitation.

- [ ] [AI] Confirm `en` is the content locale for the course library (no `id` mirror exists for this
      feature) — command: `test -d apps/ayokoding-www/content/en/learn/courses` — acceptance: directory
      exists; no sibling `id/learn/courses` directory is expected or required.
- [ ] [AI] Start dev server: `npx nx dev ayokoding-www` — acceptance: server up.
- [ ] [AI] For `en` × breakpoints (375 / 768 / 1280 px), via Playwright MCP: open the paths hub
      (2×2 grid, four cards), each of the four path landings, walk 2–3 courses via prev/next (confirm
      `?path=` persists + order + breadcrumb), open a course and confirm its **prerequisite display**,
      deep-link a course without `?path=` (canonical view + "part of paths" affordance), hit an invalid
      `?path=` (canonical view), and an old `fundamentally-strong/software-engineer/<slug>` URL (redirect
      to `/en/c/learn/courses/<id>`). For the AI path landing specifically, confirm the outbound links to
      prerequisite software-engineer courses' canonical pages resolve (DD-24). Verify `html[lang]` is
      `en` and `browser_console_messages` is clean — acceptance: all behaviors correct; zero console
      errors.
- [ ] [AI] **Three-bucket learn section (Group L)** — at the same three breakpoints, open
      `/en/c/learn` (sidebar shows exactly `paths`, `courses`, `legacy`, in that weight order),
      `/en/c/learn/legacy` (landing renders with the Q-D-ruled notice), one relocated page per domain,
      and one deep relocated page; confirm both inbound forms of a relocated URL land in one hop and
      that a `courses/` and a `paths/` URL are **not** rewritten — acceptance: all correct; zero console
      errors; the legacy breadcrumb does not wrap to multiple lines at 375 px.
- [ ] [AI] **Path-rail responsive contract (the selected Screen 3 Option B, DD-46)** — on a course in
      path context, verify each breakpoint against
      [prd.md §Screen 3 responsive specification](./prd.md#screen-3-responsive-specification-the-selected-option-b-breakpoint-by-breakpoint):
      at **1280 px** the rail shows full course titles with labelled phase separators, `course k of N`,
      and the two escape links; at **768 px** the rail is present but truncated (rows read
      `<number> <ellipsised title>`, full title in the link's `aria-label`, phase separators are bare
      rules); at **375 px** there is **no** rail and the banner readout carries the disclosure button —
      acceptance: all three states match; the rail never appears below `md` and never disappears at or
      above `md`.
- [ ] [AI] **Path-rail mobile drawer** — at 375 px activate the banner's "Open path course list" control
      via `browser_click`, confirm the **same** left drawer the header `☰` opens now lists the path's
      ordered courses, that `Esc` and the scrim both dismiss it, and that focus enters the drawer on open
      and returns to the trigger on close — acceptance: all four behaviors correct; no second overlay
      appears (only one dialog in the accessibility tree at a time).
- [ ] [AI] **No-path regression sweep** — at all three breakpoints, open a canonical course URL with no
      `?path=` and confirm the generic content-tree sidebar (desktop/tablet) and generic drawer (mobile)
      render exactly as on any other content page, with no rail, no readout, and no path breadcrumb
      segment — acceptance: the no-path experience is indistinguishable from pre-plan behaviour.
- [ ] [AI] Capture one screenshot per screen per breakpoint to
      `evidence/phase-14-<screen>-en-<breakpoint>px.png`, **including** the three rail states
      (`rail-desktop`, `rail-tablet-truncated`, `rail-mobile-drawer-open`) — acceptance: files exist in
      `evidence/`.
- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the running
      paths hub, all four path landings, sample courses **in path context (the `PathRail` at all three
      breakpoints, including the mobile drawer)**, and the **three-bucket learn section** — `/en/c/learn`,
      the `/en/c/learn/legacy` landing, and a relocated legacy page carrying the Q-D-ruled banner
      (`en` content) — acceptance: EWT/UWT/DWT findings + spec-gaps recorded.
- [ ] [AI] Append each finding below as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); append
      any SG-###/USS-### items to the relevant spec/content step.

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every EWT/UWT/DWT defect finding must be fixed/ticked before
      archival; deferral of a defect requires explicit user permission and only when genuinely
      impossible; SG-###/USS-### may be triaged or deferred with rationale)_

### Phase 14 Gate

- [ ] [AI] All screens (2×2-grid four-card hub + four landings + sample courses + prerequisite display) verified in `en` across all breakpoints; screenshots in `evidence/`; console clean.
- [ ] [AI] All rule-15 EWT/UWT/DWT defect findings fixed (ticked) or explicitly permitted to defer.
- [ ] [AI] Draft PR opened (retest evidence + any fixes); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the four-path UI is verified live and defect-clean in `en` (this plan's content
> locale; the nav mechanism itself is locale-neutral). Safe to stop. To resume: re-run the three
> testers against the running app.

---

## Phase 15: Final `origin/main` Integration & CI Verification

- [ ] [AI] Confirm no plan PR is still open: every prior phase branch has been `[AI]`-merged to `main`
      (`gh pr list --search "shared-course-library-and-learning-paths" --state open` returns zero) —
      acceptance: no open plan PRs remain.
- [ ] [AI] Sync the shared worktree to latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit test:integration test:e2e specs:behavior:coverage` + `npx nx run ayokoding-www:build` — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run (poll every ~2 min; one `gh run view --json
status,conclusion` per wakeup; never `gh run watch`) — acceptance: all GitHub Actions green; fix root
      causes and push follow-ups (own PR → review → `[AI]` merge) until green.
- [ ] [AI] Confirm `prod-ayokoding-www` serves all four paths + the full 127-course library; re-dispatch
      `apps-ayokoding-www-deployer` if any earlier deploy lagged — acceptance: production serves the
      four-path product.

### Phase 15 Gate

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + build green on integrated `main`; final `main` CI run green.
- [ ] [AI] `prod-ayokoding-www` serving all four paths + the full 127-course library.

> **Pause Safety**: the whole plan is integrated on `main`, green in CI, and live in production. Safe
> to stop. To resume: re-run the affected suite on `main` and check CI/prod status.

---

## Phase 16: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason — acceptance: every
      entry has a route or a discard reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret to a
      `<placeholder>` token or discard if unsanitizable — acceptance: `learnings.md` contains no raw secret.
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content stays in `ose-infra` only and is
      never cross-routed here; public-governance content may propagate via the parity loop —
      acceptance: no infra-private content in routed output.
- [ ] [AI] Route each surviving learning to exactly one durable home; **code-homed** learnings
      (any `apps/`- or `libs/`-homed learning, e.g. `course-paths`, or tests) are ALWAYS filed as a
      separate `plans/backlog/<slug>/` plan, never landed inline — acceptance: every entry records its
      terminal routing state.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md` — acceptance: `learnings.md` is never silently empty.

### Phase 16 Gate

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded) or the "none" escape is present.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR.
- [ ] [AI] Draft PR opened (`learnings.md` triage); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: `learnings.md` is fully triaged; nothing depends on querying it later. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 17: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete (every entry terminal or explicit "none" escape; both safety gates applied).
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`; the `en` content locale exercised (per brd.md's Indonesian-mirror-deferred non-goal).
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible); SG-###/USS-### may be triaged/deferred.
- [ ] [AI] Verify all four path manifests are published, all four landings live, the paths hub shows all four paths (2×2 grid), and the library holds the full 127-course catalog (121 software-engineer-role baseline + 6 AI-specific); every prior-phase PR `[AI]`-merged and deployed (Phase 15 checkpoint green).
- [ ] [AI] **Verify the three-bucket learn section is final and `id` is untouched (Group L)** —
      `ls apps/ayokoding-www/content/en/learn` lists exactly `_index.md`, `courses`, `legacy`,
      `overview.md`, `paths`; `find apps/ayokoding-www/content/en/learn/legacy -name '*.md' | wc -l`
      returns **1148**; `find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l` returns
      **53** and `test -e apps/ayokoding-www/content/id/belajar/legacy` returns non-zero (DD-45's
      deferral held); and all six Q-A…Q-F rulings are recorded in `tech-docs.md` rather than left
      "RECOMMENDED".
- [ ] [AI] **Verify the design-funnel artefacts are complete (DD-46 / DD-47)** —
      `find assets -name '*-option-*-*.png' | wc -l` returns **30** (5 screens × 2 options × 3
      viewports); every one is embedded in `prd.md` with viewport-specific alt text; Screen 3's
      selection reads **Option B — Left path rail**; no "Selection: PENDING" remains.
- [ ] [AI] Move: `git mv plans/in-progress/shared-course-library-and-learning-paths/
plans/done/YYYY-MM-DD__shared-course-library-and-learning-paths/` using today's completion date (the
      `evidence/` subfolder moves with it).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [ ] [AI] Update any other READMEs that reference this plan (e.g. `plans/README.md`, `plans/backlog/README.md`).
- [ ] [AI] Commit the archival: `chore(plans): move shared-course-library-and-learning-paths to done`.

### Phase 17 Gate

- [ ] [AI] Three-bucket learn section final (exactly three buckets + two hub files, 1148 legacy `.md`, `id/belajar` untouched at 53); all 30 funnel renders present and embedded; Screen 3 recorded as Option B.
- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__...`; all READMEs updated; archival committed.
- [ ] [AI] Draft PR opened (archival move); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state. To
> resume: nothing — the plan is complete.

---

### Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits.
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period).
- [ ] [AI] Split domains/concerns into separate commits; preexisting fixes get their own commits.
- [ ] [AI] Do NOT bundle unrelated changes into a single commit.

### Local Quality Gates (Before Every Push)

- [ ] [AI] `npx nx affected -t typecheck` exits 0.
- [ ] [AI] `npx nx affected -t lint` exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit` exits 0 (add `test:integration test:e2e` for the nav-feature phases).
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` exits 0.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> Commit preexisting fixes separately with appropriate conventional-commit messages.

### Note: plan location at archival time

This plan was promoted from `backlog/` to `in-progress/` on 2026-07-19, then relegated back to
`backlog/shared-course-library-and-learning-paths/` on 2026-07-21. When work resumes it is
re-promoted to `in-progress/shared-course-library-and-learning-paths/` (date prefix stripped) per the
plan lifecycle; the `git mv` in Phase 17 then archives from that `in-progress/` path to
`done/YYYY-MM-DD__shared-course-library-and-learning-paths/` using the completion date.
