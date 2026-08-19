# Next.js image builds cannot resolve the `ts-env-loader` workspace lib

One-line summary: all six Next.js app images fail to build because every `next.config.ts` imports
`@open-sharia-enterprise/ts-env-loader` but no `Dockerfile` makes that workspace package resolvable
— and four scheduled CI workflows have been reporting exactly this failure twice a day, unread.

> Surfaced 2026-08-19 during the runtime-port-override delivery (PR #230), confirmed pre-existing on
> `main`, and deliberately left out of that PR's scope.

## Problem / context

`docker build -f apps/ose-www/Dockerfile .` fails with
`Cannot find module '@open-sharia-enterprise/ts-env-loader'`, and CI reproduces it verbatim. Run
`32196421664` (2026-08-18, `ose-www-test-local-deploy-prod`) fails with:

```text
⨯ Failed to load next.config.ts
Error: Cannot find module '@open-sharia-enterprise/ts-env-loader'
ERROR: process "/bin/sh -c npm run build" did not complete successfully: exit code: 1
```

The chain is the same in all six apps:
`next.config.ts` line 1 is `import "./src/env-loader.ts"`, and that file's only job is
`import { loadTierEnv } from "@open-sharia-enterprise/ts-env-loader"`. All 6 of 6 app
`package.json` files declare the dependency, and the root `package.json` declares
`"workspaces": ["apps/*", "libs/*"]` — so the package is real and correctly wired for local
development. It is only the container builds that cannot see it.

Each Dockerfile already solves this exact problem for two other workspace libs and simply omits the
third. All 6 carry 4 `node_modules/@open-sharia-enterprise` graft lines apiece — `web-ui/src/`,
`web-ui/package.json`, `web-ui-token/src/`, `web-ui-token/package.json` — copied straight into
`node_modules` so the build can resolve them. `ts-env-loader` gets no such treatment. The two
`npm ci` variants (`ose-www`, `ayokoding-www`) never copy `libs/ts-env-loader/package.json` into the
`deps` stage, so the workspace link is never created. The four `npm install` variants
(`organiclever-www`, `wahidyankf-www`, `organiclever-app-web`, `ose-app-web`) run a `node -e` snippet
that deletes `@open-sharia-enterprise/web-ui` and `@open-sharia-enterprise/web-ui-token` from
`dependencies` before installing — but not `ts-env-loader`, leaving a private, unpublished package
name in the manifest handed to `npm install`.

The six `COPY libs/ts-env-loader/src/port-resolver.ts` lines added by PR #230 do not address this:
they land in the **runner** stage for the port wrapper's type-stripped import, long after the
**builder** stage has already failed.

## Why now

Four of the six images **are** built by CI, and every one of those builds has been failing. The
reusable workflow `_reusable-www-test-local-deploy.yml` runs
`docker compose -f infra/dev/<app>/docker-compose.yml up --build -d`, and each of those compose files
names the app's own `Dockerfile` as its build target. Four callers pass an app name into it —
`ose-www`, `ayokoding-www`, `organiclever-www`, and `wahidyankf-www` — each on two `schedule` crons a
day. All four have been red on every recent run (checked 2026-08-17 through 2026-08-18, eight runs,
zero passes).

So this is not an unwatched corner: it is a signal being emitted twice daily by four workflows and
read by nobody. They are `schedule` + `workflow_dispatch` only — there is no `pull_request` trigger —
so nothing about the failure blocks a merge, and the red runs sit outside the PR checks anyone
actually looks at. Each of those workflows also force-pushes a `prod-*` branch on success, so the
production deploy path for four sites has been dead for the whole period.

The remaining two images (`organiclever-app-web`, `ose-app-web`) have no such workflow, so for those
the breakage really is unobserved.

## Prior art / precedents

- **Turborepo `turbo prune`** — the canonical answer to "build one workspace package in Docker":
  emit a pruned lockfile plus only the workspaces that package needs.
  [turbo prune](https://turborepo.com/docs/reference/prune)
- **npm workspaces** — defines the symlink-into-`node_modules` behaviour these Dockerfiles are
  hand-simulating. [npm workspaces](https://docs.npmjs.com/cli/using-npm/workspaces)
- **Next.js `output: "standalone"`** — file-tracing that already bundles server dependencies, and
  which four of the six apps rely on. [next output](https://nextjs.org/docs/app/api-reference/config/next-config-js/output)
- **The repo's own `web-ui` graft** — the working precedent, four `COPY` lines per Dockerfile, in
  the very files that need the same treatment for `ts-env-loader`.

## Proposed direction (sketch)

- Extend each Dockerfile's existing workspace-lib treatment to `ts-env-loader`: copy its
  `package.json` into the `deps` stage and graft `src/` + `package.json` into `node_modules`, exactly
  as `web-ui` is handled today. For the four `npm install` variants, decide between grafting and
  adding `ts-env-loader` to the strip list.
- Give the images a gate, so a broken Dockerfile fails something. A build-only CI job for the six
  Next.js images is the cheap version; wiring them into the existing publish path is the thorough one.
- Consider whether six hand-maintained near-identical Dockerfiles should converge on one shared
  base or a pruning tool, rather than six copies of the same graft block.

## Rough scope & non-goals

In scope: making all six Next.js images build again, and adding whatever gate keeps them building.

Out of scope (for now): the two-app resident-process doubling covered by its own brief; changing the
runtime port contract PR #230 established; publishing these images anywhere new; the F#/`beavernest`
Dockerfiles, which do no workspace grafting and are unaffected.

## Risks & open questions

- Does the failure mode actually differ between the `npm ci` and `npm install` variants? Only
  `ose-www` was built and observed; the other five are inferred from reading their Dockerfiles.
  (open — needs five more builds before the fix is designed)
- Is `npm ci` at the workspace root silently tolerating the missing workspace directory rather than
  erroring, and if so does the fix need a lockfile change too? (open)
- Four of the six are consumed by a scheduled deploy workflow, so "delete them" is not available for
  those. It may still be right for `organiclever-app-web` and `ose-app-web`, which no workflow builds.
  (open, but now narrowed to two apps)
- Why did four workflows fail twice daily for days without anyone noticing? That is a monitoring gap
  independent of this bug, and arguably the more valuable thing to fix. (open — and it may deserve
  its own brief)
- Adding a six-image build job lengthens CI noticeably for a repo whose gates are already long.

## What success looks like + promotion signal

Success: `docker build` succeeds for all six Next.js apps from a clean checkout, the four scheduled
workflows go green, and the failure is visible on a surface someone reads — a `pull_request` trigger
on the paths involved, or an alert on scheduled-workflow failure. Ready to promote now: the defect is
confirmed in CI logs, the fix pattern already exists four lines up in each affected file, and only
the two unbuilt apps carry an open fix-or-delete question.
