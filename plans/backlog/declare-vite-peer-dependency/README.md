# 📦 Declare the `vite` Every Vitest Config Already Imports

## Context

`repo-rules-sweep` was blocked at merge time when ose-private PR #51's TypeScript quality gate failed
with `Cannot find module 'vite'` on `ts-ui:test:unit` — a target the PR never touched.

**That failure has been fixed, and not by a declaration.** Its cause was ose-private's self-hosted
runner cache: `.github/actions/setup-node` persisted each `node_modules` tree by moving it into
`$HOME/.cache/ose-node-modules/<repo>/store/<key>/node_modules` and leaving a symlink behind. Node
realpaths that symlink, so the ancestor walk from a workspace package continued under `$HOME` instead
of the repository, and the repo-root `node_modules` was unreachable. Every **root-hoisted** dependency
was invisible to any workspace package with a persisted tree; `vite` was simply the first one a gate
ever exercised. Fixed in `a34d0f15e` by copying workspace trees instead of symlinking them.

**This plan is what remains after that fix: manifest hygiene, and the gate that would have caught it.**

## What This Plan Is Not

It is not a fix for the CI failure. That is done. Nor would declaring have fixed it — verified, not
assumed: after `vite` was declared in `libs/ts-ui/package.json`, `libs/ts-ui/node_modules/` still
contained only `@rolldown`, `@vitejs`, and `react-refresh`. **npm hoists `vite` to the root regardless
of the declaration.** A declaration records intent; it does not relocate a package.

Stating this plainly matters, because the obvious reading of "package imports X, so declare X" is that
declaring makes X locally resolvable. It does not.

## The Class

Search rule: every `package.json` sitting beside a `vite*.config.*` that declares `vitest`, checked for
a `vite` declaration. Eleven packages match. One is now declared; ten are not.

| Package                                 | Repository    | `vite` declared |
| --------------------------------------- | ------------- | --------------- |
| `@open-sharia-enterprise/ts-ui`         | `ose-private` | ✅ `^7.3.5`     |
| `@open-sharia-enterprise/ts-ui-tokens`  | `ose-private` | ❌ MISSING      |
| `@open-sharia-enterprise/web-ui`        | `ose-public`  | ❌ MISSING      |
| `@open-sharia-enterprise/web-ui-token`  | `ose-public`  | ❌ MISSING      |
| `@open-sharia-enterprise/ts-env-loader` | `ose-public`  | ❌ MISSING      |
| `ayokoding-www`                         | `ose-public`  | ❌ MISSING      |
| `ose-www`                               | `ose-public`  | ❌ MISSING      |
| `ose-app-web`                           | `ose-public`  | ❌ MISSING      |
| `organiclever-www`                      | `ose-public`  | ❌ MISSING      |
| `organiclever-app-web`                  | `ose-public`  | ❌ MISSING      |
| `wahidyankf-www`                        | `ose-public`  | ❌ MISSING      |

**Honest risk statement.** None of the ten is currently at risk of the `ts-ui` failure. `ose-public`
never had the persisted-symlink cache at all — its `setup-node` differs and contains none of that
logic, which is why PR #227 was green throughout with nine undeclared packages. `ose-private`'s copy
is now fixed. This is a correctness-of-manifests plan, not an outage waiting to happen.

**The two repositories resolve different majors** — `ose-public` hoists `vite` 8.0.13, `ose-private`
resolves 7.3.5. A single shared version string across both would force a resolution change in one of
them. Each declaration must match what its own lockfile already resolves.

## Workstreams

| ID    | Workstream                                                         | Status    |
| ----- | ------------------------------------------------------------------ | --------- |
| WS-V1 | Declare `vite` in the ten remaining packages, per repo             | Specified |
| WS-V2 | Prevent the class: fail CI when a config imports an undeclared dep | Specified |

### WS-V1 — Declare what is already imported

Mechanical, and required to be **inert**: each declaration is pinned to the version that repository's
lockfile already resolves, verified by confirming the lockfile gained only the declaration line and no
version change. A lockfile that re-resolves means the range was wrong.

The value is that a reader of `package.json` learns what the package needs. Today they cannot: the
manifest is silent and the truth lives in npm's hoisting.

### WS-V2 — The gate that would have caught it

`vite` is not special. Any package whose config imports a module it does not declare is invisible to
every manifest reader and to every existing gate. WS-V2 walks each workspace package's config files,
extracts their imports, and fails when one is not declared by that package.

This is the workstream with real value. WS-V1 closes today's ten instances; WS-V2 is why there is not
an eleventh — and it is the check that would have named `libs/ts-ui` months before a runner-cache
change turned a silent gap into a red gate.

## Scope

**Repositories**: `ose-public` (9 packages) and `ose-private` (1 package). WS-V2 must land in both or
they diverge.

**Trees in scope**: the ten `package.json` files, both `package-lock.json` files, and — for WS-V2
only — `apps/rhino-cli/` and `repo-config.yml`.

**Out of scope**: upgrading `vite`; reconciling the 7.x/8.x split between the repositories; changing
any `vite*.config.*` file's contents; and any further work on the runner cache, which is fixed.

## Approach Summary

WS-V1 must be provably inert: same resolved versions before and after, same test counts, in both
repositories. WS-V2 is a `rhino-cli` gate and therefore carries a TDD cycle, companion Gherkin under
`specs/apps/rhino/`, and a four-repo parity-manifest obligation — see
[the parity boundary](../../../docs/reference/related-repositories.md).

Sequence WS-V2 first where practical: while the ten are still undeclared, its RED state is the real
repository rather than a fixture.

## Documents

- [brd.md](./brd.md) — why an undeclared dependency graph is worth paying to fix.
- [prd.md](./prd.md) — user stories and Gherkin acceptance criteria.
- [tech-docs.md](./tech-docs.md) — the resolution mechanics and the gate design.
- [delivery.md](./delivery.md) — the phase-by-phase execution checklist.
