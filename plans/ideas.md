# Ideas

Quick ideas and todos that haven't been formalized into plans yet.

When an idea is ready for implementation, create a proper plan folder in `backlog/` and remove it from this list.

## Ideas List

### ayokoding-www-fe-e2e (added 2026-07-15 as ayokoding-resizable-docs-sidebar after-action)

- `apps/ayokoding-www-fe-e2e/playwright.config.ts` previously set `missingSteps: "fail-on-gen"`,
  which silently blocked `bddgen` (and therefore the entire `test:e2e` target, gating the
  twice-daily production-deploy cron) from generating ANY test file whenever ANY scenario in the
  Gherkin glob lacked a step def — roughly 104 pre-existing scenarios had no implementation. Fixed
  to `missingSteps: "skip-scenario"` (marks uncovered scenarios `test.fixme` instead of hard-block)
  during the `ayokoding-resizable-docs-sidebar` plan so its own new E2E scenarios could run at all.
- **Resolved 2026-07-16** (PR #49 review cycle 1, `pr-review-fixer`): that fix had newly surfaced
  what a 2026-07-15 run read as 8 full-suite failures, filed here as a deferred backlog note per a
  cited "Root Cause Orientation scope-discipline carve-out" — `pr-review-maker` correctly flagged
  that no such carve-out exists (the practice's "Medium Fixes" category explicitly covers "Broken
  tests," fix within the session). Re-investigation found 3 real, root-cause-fixable chromium
  failures (a genuine viewport-clamp gap in this plan's own new `resizable-sidebar.feature`
  coverage, plus 2 stale e2e-step assertions in `cost-of-living-calculator.feature.spec.js` —
  "Pre-school children incur childcare, not schooling" and "Household composition changes the
  minimum qualifying role") — all fixed at the root cause in
  `apps/ayokoding-www-fe-e2e/src/steps/{resizable-sidebar,cost-of-living-calculator}.steps.ts`.
  The 2 `ia-navigation-revamp.feature.spec.js` scenarios originally counted (sitemap/RSS) did not
  reproduce on re-verification and needed no fix. `npx nx run ayokoding-www-fe-e2e:test:e2e` now
  exits 0.
- Future plan: burn down the ~104 scenarios now marked `test.fixme` across
  `navigation.feature`/`content-rendering.feature`/`search.feature`/etc. — implement their missing
  E2E step defs so `skip-scenario` can eventually revert to `fail-on-gen` (the safer default).

### Rust Governance (added 2026-05-23 as rust-governance-audit after-action)

- Future plan: promote `tech-docs.md §4` (Rust crate structural checklist) to
  `repo-governance/development/quality/rust-crate-structural-checklist.md` once a second Rust crate
  is added to `ose-public`. Single-crate evidence is insufficient to validate the abstraction level.

### AyoKoding Web (added 2026-05-22 as ayokoding-web-learn-reorg after-action)

- Future plan: add canonical shape enforcement rules to `apps-ayokoding-www-by-example-checker` and `apps-ayokoding-www-in-the-field-checker` — validate that every checked topic follows the `<domain>/<area>/<topic>/{overview.md,by-example/,by-concept/,in-the-field/}` tree shape.
- Future plan: consider creating `apps-ayokoding-www-by-concept-checker` agent once the by-concept track has sufficient coverage to warrant dedicated structural validation.
- Indonesian content reorg (id/) is not needed: `content/id/` uses `belajar/` with Indonesian-named dirs and has no parallel platform-\*/human/ structure. No action required.

### Infrastructure

- Create IAM (Identity and Access Management) service/module for authentication and authorization

### Demo Apps

- Recheck all standards.

### Development Experience

- Standardize CIs
- .env backup scripts for rhino-cli
- simplify ayokoding-cli and ose-cli
- libraries update
- **Source-code credential scanning** — evaluate Betterleaks (gitleaks successor, MIT, v1.0.0 early 2026) for pre-commit + CI detection of hard-coded credentials in `.rs`/`.ts`/`.tf` source files once
  it reaches stable production use. This public repo already has free GitHub Secret Scanning
  post-push coverage (700+ partner patterns + AI-backed generic detection). Gitleaks itself is
  feature-frozen with an unresolved entropy false-positive regression
  ([#1830](https://github.com/gitleaks/gitleaks/issues/1830)) affecting Rust config struct field
  names. Re-evaluate after Betterleaks has 60+ days of production soak.
- Split mermaid diagrams in `plans/done/2026-04-26__organiclever-ci-staging-split/tech-docs.md` to satisfy validator rules (surfaced 2026-04-26 by `rhino-cli-mermaid-fixes`): 7 label_too_long + 2 width_exceeded violations across blocks 0 (line 7) and 1 (line 40), plus 2 subgraph_density warnings on 7-child WF subgraphs. Follow-up to `2026-04-26__rhino-cli-mermaid-fixes`.

### Stack Update Deferrals (added 2026-05-16 by stack-update plan)

- Future plan: migrate `aws-sdk-go` v1 → v2 (currently transitive via `narqo/go-badge`; v1 EOL 2025-07-31; S3-crypto CVEs CVE-2020-8911/8912 only affect `s3crypto` codepaths which our CLIs do not use).
- Future plan: TypeScript 6.0 migration once TS 6.x has 60+ days of soak (eligible after ~2026-05-23).
- Future plan: ESLint 10 + react-hooks 7 migration once those versions have 60+ days of soak.
- Future plan: Zod 4.x migration (post-cutoff; eligible after 60-day soak).
- Future plan: lucide-react 1.x migration (post-cutoff; eligible after 60-day soak).
- Future plan: @xstate/react 6.x migration (post-cutoff; eligible after 60-day soak).
- Future plan: TailwindCSS 4.3.x migration (post-cutoff; eligible after 60-day soak).
- Future plan: @effect/platform 0.96.x + effect 4.x migration (post-cutoff; eligible after 60-day soak).
- Future plan: Storybook 10.3/10.4 adoption (post-cutoff; downgrade in this plan to 10.2.10 for CVE clearance).
- Future plan: Volta → mise migration (volta last release Dec 2024).
- Future plan: Microsoft Defender / dotnet 10.0.300 brew bottle availability (currently install via dotnet-install.sh to ~/.dotnet).
- Future plan: bump `vite` to 7.4+ across all consumers, then adopt `@vitejs/plugin-react 6.0.1` (this plan reverted plugin-react 6.0.1 → `^5.1.4` because plugin-react 6 requires vite's `./internal` subpath which is unavailable on the installed transitive vite 7.3.1). Caret retained pending the vite bump.

### Behavior Coverage Engine (added 2026-07-05 by post-archival hollow-spec re-verification)

- **Runtime cross-check flags never wired** — `rhino-cli specs behavior-coverage validate`'s
  `--unit-report`/`--integration-report`/`--e2e-report` flags (the JSON-run-report ingestion engine
  built in `plans/done/2026-07-04__enforce-repo-wide-scenario-implementation`'s Phase 1) exist and
  work, but zero `project.json`/CI workflow file in any of the 3 repos (`ose-public`, `ose-primer`,
  `ose-infra`) actually passes them — confirmed via repo-wide grep, all 3 repos, 2026-07-05. The
  archived plan's Final Gate claims this mechanism is "wired to pre-push + CI," which is not
  accurate as literally described; today's anti-hollow-spec guarantee instead comes from two
  redundant mechanisms that ARE wired and verified working: static step-text matching (a `@covers`
  marker must resolve to a real, registered step function) plus per-language fail-on-skip
  grep-bans baked directly into each project's `test:unit`/`test:quick` command. No hollow spec
  exists today as a result, but wiring the JSON-report mechanism for real (deciding which tier
  emits which report format per language/tool, then threading it through 59 projects'
  `specs:behavior:coverage` targets) is a genuine follow-up engineering slice, not a quick fix.

### CI Flakes (added 2026-07-02 by unify-rhino-cli-sdlc-parity after-action)

- Fixed 2026-07-03 (root-caused, not a runner flake — two distinct bugs, one per app):
  - `ayokoding-www-test-local-deploy-prod`: `ayokoding-www-be-e2e/playwright.config.ts` had `reuseExistingServer: !process.env.CI`, inverting the intent — it disabled server reuse specifically in CI, where `_reusable-www-test-local-deploy.yml` always pre-starts the app via `docker compose`. Playwright then tried to start a second server on the same port and failed with `Error: http://localhost:3101 is already used`, taking `fe-e2e` down with it. Fixed to `reuseExistingServer: true`, matching the already-correct sibling `fe-e2e` config.
  - `wahidyankf-www-test-local-deploy-prod`: unrelated `Turbopack build failed... Module not found: Can't resolve 'cmdk'` inside the Docker build. `libs/web-ui`'s barrel `index.ts` re-exports `command.tsx` (which imports `cmdk`), and `apps/wahidyankf-www/Dockerfile` manually mirrors `web-ui`'s non-workspace-hoisted dependencies but never added `cmdk` when the `command` primitive was introduced. Fixed by installing `cmdk@1.1.1` (exact version match to `libs/web-ui/package.json`, already CVE-clean, no new dependency introduced); verified with a local `docker build`.
- **New finding, not yet fixed** (surfaced 2026-07-03 while verifying the `ayokoding-www-be-e2e`
  fix above): `ayokoding-www-fe-e2e` fails with `Missing step definitions: 83`, all in
  `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/cost-of-living-calculator.feature`
  (country-filter interaction, ASEAN-region grouping, qualifying/non-qualifying divider rows,
  minimum-role-rank threshold scenarios — e.g. no `When("the Country filter is set to {string}", ...)`
  step exists at all in `cost-of-living-calculator.steps.ts`, only `Then` assertions reading its
  state). `git blame` dates these scenarios to `86b1d2ae9e`/`49cca4d54` (2026-06-19 through 06-22) —
  a genuine, ~2-week-old content gap, not new work-in-progress. It was invisible until now because
  `ayokoding-www-be-e2e` always failed first on the port-conflict bug (fixed above), which ran before
  `fe-e2e` in the same job and masked whether `fe-e2e` itself passed. This is a real, substantial
  UI-interaction feature-implementation gap (83 Playwright steps for a complex calculator's
  country/region filtering and savings-threshold logic) requiring live browser verification against
  the running app — deliberately not attempted blind in the same pass as the port-conflict fix. Needs
  a dedicated follow-up (ideally with `npx nx run ayokoding-www:serve` + browser automation to verify
  each step against the real UI, not just written from reading the `.feature` file).
