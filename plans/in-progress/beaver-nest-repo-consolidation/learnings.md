<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: beaver-nest-repo-consolidation

## Learning: Phase 1's "inert copy" Gate premise is false for this workspace

`nx.json` has no `plugins`/project-glob restriction, so Nx auto-discovers every `project.json` in
the tree regardless of whether it is wired into any other config. The Phase 1 Gate's
`npx nx run-many -t test:quick --all` therefore does **not** exit 0 immediately after copying —
the 5 copied `beaver-nest-*` project.json files register as real (if half-broken) Nx projects the
moment they land on disk, before Phase 2's registration step ever runs. Verified the actual intent
("existing projects must be unaffected") holds by excluding the new `beaver-nest*` projects from
the `test:quick` invocation — all 29 pre-existing projects and their 13 dependency tasks still pass.
One exception: `rhino-cli:test:quick` fails regardless of exclusion, because its
`fsharp_tool_invocation` Gherkin check scans **every** F# `project.json` repo-wide, not just
Nx-registered ones — this surfaced a real, separate preexisting defect (see next entry). Routed:
fold into `delivery.md`'s Phase 1 Gate wording during a future plan-quality pass — not urgent enough
to block this plan.

## Learning: ported `apps/beavernest-be/project.json` missing `dotnet tool restore` prefix on fantomas

Line 53 (`"fantomas --check apps/beaver-nest-be/src"`) lacked the `dotnet tool restore &&` prefix
that lines 54-55 in the same file correctly have. This is a preexisting defect in `beaver-nest`'s
own source, invisible under its own weaker/absent gate, caught here only because `ose-public`'s
`rhino-cli:test:quick` scans all F# project.json files repo-wide regardless of Nx registration.
Fixed directly (one-line prefix add) rather than deferred, per Root Cause Orientation — trivial,
in-scope, and blocking the repo-wide gate. Routed: inline fix, already applied; no further action.

## Learning: casing convention resolved directly by delivery.md text, no judgment call needed

Phase 2's task brief flagged the F# PascalCase casing (`BeaverNestBe` vs `BeavernestBe`) as an open
judgment call, but delivery.md's own Workspace-wiring bullet
(`dotnet sln open-sharia-enterprise.sln add apps/beavernest-be/src/BeaverNestBe/BeaverNestBe.fsproj
...`) already names the target literally. Verified against the ported source: the `BeaverNestBe`
folder/`.fsproj`/namespace name was **already correct** pre-rename (Phase 1's verbatim copy
preserved it) and needed zero edits. The rename touched only kebab-case identifiers
(`beaver-nest-*` → `beavernest-*`, with the frontend suffix `-fe` → `-app-web` to match this repo's
`[domain]-app-web` naming tier — confirmed against `organiclever-be`/`organiclever-app-web`'s
existing `specs/apps/organiclever/behavior/<full-project-name>/gherkin` directory convention) and the
`BEAVER_NEST_BE_*`/`beaver_nest_*` env-var and shell-variable prefixes. Routed: none — the ambiguity
was already resolved by the plan text; no convention gap to fix.

## Learning: ported staging-CI workflow called a reusable workflow it couldn't satisfy

`beavernest-app-test-local-deploy-stag.yml` (ported verbatim in Phase 1, before any Phase 2 edits)
called `_reusable-app-test-local-deploy-stag.yml` with only `web-project`/`be-project`/
`contracts-project`/`compose-dir` — missing `stag-web-branch`, `stag-be-branch`, `be-port`,
`web-port`, all `required: true` in the reusable workflow's `workflow_call` inputs. `actionlint`
failed immediately, independent of any renaming. Root cause: `beaver-nest`'s own reusable workflow
(from its origin repo) never required a mandatory `deploy` job; `ose-public`'s
`_reusable-app-test-local-deploy-stag.yml` does (it unconditionally force-pushes both stag branches
on success), and BeaverNest has no staging target yet — its own file comment already said "this
workflow never deploys." Rather than inventing placeholder stag branches (which the reusable
workflow's `deploy` job would then force-push into existence — the opposite of "never deploys"), or
weakening the shared reusable workflow's required inputs for the other two callers
(`organiclever-app-web`, `ose-app-web`), rewrote the BeaverNest caller as inline jobs mirroring the
reusable workflow's non-deploy stages (`specs-coverage`, `fe-lint`, `be-integration`,
`fe-integration`, `e2e`, `specs-gate`), omitting `deploy` entirely, and adapted `e2e` to BeaverNest's
single combined-image architecture (`apps/beavernest-be-e2e`/`apps/beavernest-app-web-e2e`'s
`test:e2e` targets already self-orchestrate their own disposable compose runtime via
`apps/beavernest-be/scripts/run-e2e.sh`, so the job doesn't need the reusable workflow's manual
compose-up/curl-wait steps). `actionlint` now exits 0. Routed: none — self-contained fix, scoped to
the single caller file, zero blast radius on the two other reusable-workflow callers. Standing up
BeaverNest's first real staging/production deploy target remains explicit future work (the
`plans/ideas/beavernest-first-deploy.md` brief named in this plan's tech-docs.md file tree, not yet
created).

## Learning: worktree path itself false-positives the literal `beaver-nest` REFACTOR-gate grep

Running `grep -rn 'beaver-nest' apps/beavernest-be apps/beavernest-app-web apps/beavernest-be-e2e
apps/beavernest-app-web-e2e specs/apps/beavernest infra/dev/beavernest-app` exactly as delivery.md's
Phase 2 REFACTOR step specifies returns non-zero matches — but every hit lives in gitignored
`obj/`/`bin`-style `.NET` build artifacts (`project.assets.json`, `*.nuget.dgspec.json`, etc.) that
embed the **absolute filesystem path**, which itself contains the substring `beaver-nest` because
this plan's own worktree is named `beaver-nest-repo-consolidation`. It is not residual product-name
drift. Confirmed by re-running with `--exclude-dir=obj --exclude-dir=bin
--exclude-dir=generated-contracts --exclude-dir=dist --exclude-dir=node_modules
--exclude-dir=.features-gen`, which returns zero matches, and by `git check-ignore -v` confirming
those exact `obj/` paths are gitignored. Routed: fold an `--exclude-dir=obj --exclude-dir=bin` (or
equivalent gitignore-respecting) caveat into this REFACTOR/Gate grep command during a future
plan-quality pass — not urgent enough to block this plan, and irrelevant once a worktree isn't
literally named after the old product identifier.

## Learning: delivery.md's `specs:coverage` target name is repo-wide stale terminology

Every "Affected spec coverage" step in delivery.md (Phase 3 through Phase 10, plus the Validation
section) says `npx nx affected -t specs:coverage` / `npx nx run-many -t specs:coverage ...`, but no
project in the repo defines a target literally named `specs:coverage` — it was renamed to
`specs:behavior:coverage` (aggregated, together with `specs:structure-validation` and, where
applicable, `specs:domain:coverage`/`specs:e2e:coverage`, under `test:specs`) repo-wide, confirmed by
`repo-governance/development/infra/nx-targets.md` explicitly noting "(renamed from `specs:coverage`)"
in three places. Phase 2's own delivery.md text (line ~307) already flagged the ported
`beavernest-be/README.md`'s claim of this nonexistent target as something to fix, but delivery.md's
own command text throughout Phases 3-10 never got the same correction. Substituted `npx nx run-many
-t test:specs -p beavernest-be,beavernest-app-web` for Phase 3's step 2 (result: 4 specs/beavernest-app-web

- 15 specs/beavernest-be = 19 total, all covered — matches the "19 feature files" acceptance) and
  `npx nx affected -t test:specs` for the Local Quality Gates step (exit 0, 34 projects). Routed: fold a
  one-time sed replace of `specs:coverage` → `test:specs` across delivery.md's remaining Phase 4-10
  command text during a future plan-quality pass — not urgent enough to block this plan; each future
  phase executor should substitute `test:specs` when it hits this same stale reference.

## Learning: `.dockerignore` never allow-listed `specs/apps/beavernest`, blocking every BeaverNest Docker build

The root `.dockerignore` blanket-excludes all of `specs/` and then allow-lists specific subtrees per
app (`a-demo`, `organiclever`, `ose-app`) that each app's Dockerfile needs in its build context.
`beavernest-be`'s Dockerfile (a from-scratch, no-host-generated-artifacts combined-runtime build —
different from `organiclever-be`'s Dockerfile, which copies a host-pre-generated
`apps/organiclever-be/generated-contracts` instead) needs the whole
`specs/apps/beavernest/containers/contracts/` directory in its build context to bundle the OpenAPI
contract and codegen the frontend client inside the image, but nobody added the matching allow-list
line during Phase 1/2's port — every `docker build`/`docker compose build` for `beavernest-app`
failed immediately with `"/specs/apps/beavernest/containers/contracts": not found`. Fixed by adding
`!specs/apps/beavernest/containers/contracts` to `.dockerignore` (alongside the existing
`a-demo`/`organiclever`/`ose-app` entries). This is a genuine, blocking, previously-undiscovered defect
— nothing in Phase 0-2's gates ever ran a Docker build. Routed: inline fix, already applied.

## Learning: `beavernest-be-e2e` test utilities referenced the wrong Compose service name

`apps/beavernest-be-e2e/utils/compose-runtime.ts` hardcoded `const backendService = "beavernest-be"`
and `apps/beavernest-be-e2e/steps/persistence.steps.ts` had one more hardcoded literal
`"beavernest-be"` in a `docker compose run` argument list — but the actual Compose service name in
`infra/dev/beavernest-app/docker-compose.yml` is `beavernest-app` (the single combined-runtime
service; there is no separate `beavernest-be` service — `beavernest-be` is only the Nx _project_
name). Every `docker compose exec/run/stop beavernest-be` call therefore failed with `no such
service: beavernest-be` / `service "beavernest-be" is not running`, silently failing 8 of 15 backend
E2E scenarios regardless of the app's actual behavior. Fixed both hardcoded literals to
`"beavernest-app"`. This unblocked 7 previously-silently-failing scenarios (all now pass); see the
next entry for the genuinely unresolved remainder. Routed: inline fix, already applied — the two
literal sites are the only occurrences (`grep -rn '"beavernest-be"' apps/beavernest-be-e2e` after the
fix returns only comment/doc-string matches, not compose-argument literals).

## Learning: 5 of 15 backend E2E scenarios need `dotnet fsi`/`dotnet run` inside `beavernest-app`, but the production runtime image intentionally has no .NET SDK — unresolved, needs a follow-up plan

After the service-name fix above, `compose-runtime.ts`'s `runFsi`, `runBackendCommand`, and
`runStoppedBackendCommand` helpers (used by 5 of the 8 remaining failing scenarios — fresh-database,
migration-restart, sqlite-contention, sqlite-settings, online-backup, verified-restore) execute
`dotnet fsi --exec ...` / `dotnet run --project ...` _inside_ the running `beavernest-app` container.
`apps/beavernest-be/Dockerfile`'s final `runtime` stage is deliberately
`mcr.microsoft.com/dotnet/aspnet:10.0.10-noble` (ASP.NET **runtime**, no SDK — a hardening choice, not
an oversight: the image also runs as a non-root UID with a strict entrypoint permission validator).
No Compose file wires an SDK-having image for this disposable E2E stack — the only SDK-based image in
the tree is `infra/dev/beavernest-app/Dockerfile.be.dev`, used exclusively by `npm run beavernest:dev`
(local dev, independent of Compose), not by `run-e2e.sh`'s disposable stack. The `broken-migration`
scenario additionally fails because its step script does `cp -a /workspace/. "$source"` assuming a
`/workspace` source-tree layout that doesn't exist in any current image stage. This is a genuine,
pre-existing architectural mismatch between the ported E2E test suite's assumptions and the current
(security-hardened, single-stage) container design — not a typo or config fix, and not something
introduced by this porting work. Verified it's not a rootless-podman UID-mapping artifact: identical
failures reproduced after switching the local podman machine from rootless to rootful. A proper fix
needs a dedicated CI-only image variant (e.g. an additional Dockerfile stage that keeps the SDK
alongside the full `/workspace` source, wired via `docker-compose.ci.yml`'s `build.target`) or a
rewrite of the affected step helpers to stop needing an SDK inside the runtime container — both are
non-trivial engineering, out of scope for a "prove it's green" verification phase. Current state:
backend E2E 7/15 pass (up from effectively 0 reachable before the two fixes above), frontend E2E 4/4
pass. Routed: needs a new backlog plan item to redesign the E2E-vs-runtime-image contract for
`beavernest-be-e2e`; flagged prominently in this execution's final report rather than silently
declared green.

## Learning: `beavernest-app`'s Compose healthcheck always failed — the runtime image never had `curl`

`infra/dev/beavernest-app/docker-compose.yml`'s healthcheck runs `curl -fsS
http://localhost:19300/api/v1/readiness` **inside** the container, but `apps/beavernest-be/Dockerfile`'s
`runtime` stage (`mcr.microsoft.com/dotnet/aspnet:10.0.10-noble`) never installs `curl` — confirmed via
`docker exec ... which curl` (exit 1) and the container's health log (18 consecutive exit-1 checks
with empty output, i.e. "command not found", not an app-readiness failure — the app itself answered
`HTTP/1.1 200 {"status":"ready"}` to a host-side curl the whole time). `Dockerfile.be.dev`'s own
comment already documents this exact class of problem for the _dev_ image ("curl is required by the
compose healthcheck — the SDK image does not ship it") but the same fix was never applied to the
_production_ Dockerfile's `runtime` stage. This is why `run-e2e.sh` and this plan's own step 3
acceptance ("`docker compose ps` reports the app service healthy") never caught it before — `run-e2e.sh`
polls readiness from the host directly and never checks Compose's own health status. Fixed by adding
`apt-get install curl` (with `rm -rf /var/lib/apt/lists/*` to keep the image lean) to the `runtime`
stage, matching `Dockerfile.be.dev`'s existing pattern. Routed: inline fix, already applied.

## Learning: the ReadinessPanel component legitimately renders "Ready" text twice; one E2E locator was ambiguous, not the component

`apps/beavernest-app-web-e2e/steps/workspace.steps.ts`'s `readiness-recovery` scenario asserted
`page.getByText("Ready", { exact: true })`, but `ReadinessPanel.tsx` intentionally renders "Ready" in
two places by design: a status badge (`<span>` next to a `check-circle` icon) and a "Database" `<dd>`
in the details list. Playwright's strict-mode locator resolution correctly refused to guess between
them. This is a pre-existing test-locator bug (unrelated to D6's stated web-ui-version risk — the
component structure is intentional, not a regression), caught only because Phase 3 actually ran the
E2E suite against the running app for the first time. Fixed by scoping the assertion to the status
badge's icon specifically — `page.getByRole("img", { name: "Ready", exact: true })` — since
`libs/web-ui`'s `Icon` component renders `role="img"` with the given `aria-label` when one is passed,
giving an unambiguous, semantically-correct match. Routed: inline fix, already applied.

## Learning: the app never shipped a favicon, producing a real (if trivial) browser console error

Manual UI Verification's `browser_console_messages` check (mandated zero error-level messages) caught
one real `[ERROR] Failed to load resource: 404 ... /favicon.ico` — `apps/beavernest-app-web/index.html`
never declared a `<link rel="icon">` and no `public/` directory exists, so the browser's automatic
favicon probe always 404s. Fixed with the standard minimal suppression pattern (`<link rel="icon"
href="data:,">`), which tells the browser there deliberately is no favicon rather than fabricating a
placeholder icon asset (a design decision out of scope here). Re-verified after rebuild: 0 error-level
console messages. Routed: inline fix, already applied.

## Learning: delivery.md's own Manual UI Verification step names the wrong port (19310, not 19300)

Delivery.md's Manual UI Verification section says to `browser_navigate` to `http://127.0.0.1:19310`
"with the compose stack from the steps above still running", but the production Compose stack
(`infra/dev/beavernest-app/docker-compose.yml`) only ever exposes the single combined-runtime service
on port 19300 — confirmed by `infra/dev/beavernest-app/README.md`: "one `beavernest-app` service...
serves the Vite CSR client and API from one ASP.NET origin on container port `19300`; no separate
frontend or backend host port exists." Port 19310 is exclusively the **local-dev-only** Vite dev
server (`npm run beavernest:dev`, per the same README's "Local Development" section), which is
independent of and not started by the Compose stack at all. Navigated to `127.0.0.1:19300` instead —
confirmed via a successful `browser_navigate` and a DOM snapshot showing the rendered `ReadinessPanel`.
Routed: fold a same-file correction (19310 → 19300) into this Manual UI Verification bullet during a
future plan-quality pass — not urgent enough to block this plan, but a real drift a future executor
would otherwise trip over identically.

## Learning: the screenshot-embed grep acceptance clause double-counts its own instructional text

Phase 3's "Document the three screenshots" step's stated acceptance is `grep -c
'evidence/phase-3-beavernest-app-web-.*px.png)' delivery.md` printing `3`. After embedding exactly
three real screenshot markdown lines, the actual count is `5` — because the step's own instructional
bullet (which spells out the required embed template using placeholder tokens
`<viewport>-<width>px.png)`) and the acceptance bullet's own quoted grep command both incidentally
contain a substring matching the same pattern they describe. This is a self-referential false-count,
not a missing-embed defect: `grep -n` confirms exactly 3 real `![...](./evidence/...)` embeds exist,
one per viewport, and all three referenced files exist on disk. Left the instructional text unedited
(out of this execution's authorized single delivery.md edit — embedding the screenshots only). Routed:
fold a more self-immune acceptance pattern (e.g. anchor on `^!\[` or grep the git diff instead of the
whole file) into this bullet during a future plan-quality pass.

## Learning: Docker Desktop would not start in this sandboxed execution environment; used a rootful podman machine as a Docker-API-compatible substitute

`docker compose`/`docker` commands in this environment normally target Docker Desktop's socket
(`~/.docker/run/docker.sock`), but Docker Desktop's GUI process never fully launched here (`open -a
Docker`, and direct binary invocation, both left only a stale `com.docker.vmnetd` helper running, no
socket) after repeated attempts and a stale-process cleanup — consistent with a sandboxed/headless
execution context lacking a full interactive GUI session Docker Desktop's Electron shell needs. The
machine already had `podman` (with a never-started `podman-machine-default` VM) installed via
Homebrew. Started it (`podman machine start`, then `podman machine set --rootful` after confirming
rootless mode produced identical results to rootful for the SDK-gap failures above, ruling out a
UID-mapping theory) and pointed the **same** `docker`/`docker compose` CLI binaries at it via
`DOCKER_HOST=unix:///var/folders/.../podman-machine-default-api.sock` — confirmed working via `docker
run --rm hello-world` and every build/compose/E2E operation in this execution. This is a real,
Docker-API-compatible substitute (not a mock or fabrication), but any AI agent or human resuming work
in this same sandboxed environment will need to repeat the `podman machine start` +
`DOCKER_HOST=...` sequence, since it doesn't persist across shell invocations or sessions. Routed: not
a plan-doc fix — an environment/tooling note; consider documenting the `DOCKER_HOST` podman-substitute
pattern in a worktree-setup or troubleshooting doc if this sandboxed-Docker-Desktop gap recurs across
future plan executions.
