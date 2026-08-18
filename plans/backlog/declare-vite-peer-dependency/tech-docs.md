# Technical Documentation — Declare the `vite` Every Vitest Config Already Imports

## How `vite` Reaches Code That Never Asked For It

No `package.json` in either repository declares `vite`. Verified by command:

```bash
git ls-files '*package.json' \
  | xargs jq -r 'select((.devDependencies.vite // .dependencies.vite) != null) | .name'
# ose-public: no output
```

`vite` is a **peer dependency of `vitest`**:

```bash
jq -r '.packages["node_modules/vitest"].dependencies | to_entries[] | select(.key == "vite")' \
  package-lock.json
# "vite": "^6.0.0 || ^7.0.0 || ^8.0.0-0"
```

npm 7+ auto-installs peer dependencies. `vite` is therefore installed at the root — `ose-public`
resolves 8.0.13, `ose-private` resolves 7.3.x — and Node's module resolution walks up from any
workspace package into the root `node_modules` and finds it.

Eleven other packages import `vite` in their config files. All eleven resolve it through that upward
walk. None of them declared it, and until PR #51 none of them ever needed to.

## Why It Broke Exactly Once, and There

Hoisting resolves `vite` for every package while the ancestor walk can reach the root. `ose-private`'s
self-hosted runner broke that walk.

`.github/actions/setup-node` persisted each `node_modules` tree by moving it to
`$HOME/.cache/ose-node-modules/<repo>/store/<key>/node_modules` and leaving a symlink in the repo.
Node's CommonJS resolver realpaths what it resolves, so from `libs/ts-ui/` the walk entered the
symlink, resolved to the store path, and continued up **`$HOME`'s** ancestors — never reaching the
repository root where `vite` was hoisted:

```
libs/ts-ui/node_modules            -> $HOME/.cache/ose-node-modules/ose-private/store/libs_ts-ui/node_modules
                                        ^ walk continues from HERE: store/, ose-private/, .cache/, $HOME
<repo>/node_modules/vite                ^ never visited
```

Confirmed by controlled experiment, with the tree contents held constant and only the layout varied:

| `libs/ts-ui/node_modules`      | `nx run ts-ui:test:unit`            |
| ------------------------------ | ----------------------------------- |
| symlink into the store         | `Cannot find module 'vite'`, exit 1 |
| identical tree copied in place | 12 files, 102 tests passed, exit 0  |

**Declaring `vite` does not fix this, and was tried.** npm hoists it to the root either way — after the
declaration, `libs/ts-ui/node_modules/` still held only `@rolldown`, `@vitejs`, and `react-refresh`.
The declaration is correct hygiene and is retained; it was not the fix.

The fix was in the action (`a34d0f15e`): workspace trees are copied rather than symlinked, so they
remain real directories inside the repository and the walk reaches the root. The root tree stays a
symlink — its realpath'd ancestors contain the store's own `node_modules`, the directory it was
already resolving from, so it never needed the copy.

`ose-public` never had this scheme; its `setup-node` differs and contains none of that logic. That is
why its nine undeclared packages were green throughout.

**What this leaves for the present plan.** Three properties made the incident expensive, and only the
third is still open:

1. It could not reproduce locally — a local `npm install` always hoists. _(Addressed by the action fix.)_
2. It was not attributable to the branch that surfaced it. _(Addressed by the action fix.)_
3. **The manifests gave no way to tell "missing" from "unreachable."** Ten packages still import a
   module they do not declare, so the next ambiguous failure is read the same slow way.

## WS-V1 — Declaration Mechanics

For each of the ten packages:

1. Read the version that repository's lockfile already resolved for `node_modules/vite`.
2. Add `"vite": "^<that version>"` to `devDependencies`, keeping the map sorted.
3. Run `npm install`.
4. **Inspect the lockfile diff and require it to be declaration-only.**

Step 4 is the acceptance test for the whole workstream, not a formality. The expected diff for one
package is a single added line under that package's workspace entry:

```diff
         "vitest": "^4.1.0",
+        "vite": "^7.3.5",
```

Any changed `"version"`, `"resolved"`, or `"integrity"` field means the declared range did not match
what was already installed, and the declaration has become an upgrade. Revert and re-derive the range.

**The two repositories must be pinned independently.** `ose-public` is on `vite` 8.x and `ose-private`
on 7.x. Copying one repository's range into the other would force a resolution change — exactly what
step 4 exists to prevent. Converging the two majors is deliberately out of scope.

## WS-V2 — Gate Design

A `rhino-cli` gate, so it carries the full obligation set: TDD cycle, companion Gherkin under
`specs/apps/rhino/`, registration in `repo-config.yml`, and a regenerated parity manifest staged in
the same commit.

**Input.** Every workspace package directory, from the root `package.json` `workspaces` globs.

**For each package**: find its config files (`*.config.{ts,js,mts,mjs,cts,cjs}`), extract every
`import`/`require` specifier, and classify each:

| Specifier shape                   | Verdict                                  |
| --------------------------------- | ---------------------------------------- |
| `./x`, `../x`, absolute           | ignore — relative, not a package         |
| `node:fs`, `fs`, `path`           | ignore — Node builtin                    |
| `@scope/name`, `name`, `name/sub` | check — resolve to the bare package name |

For each checked specifier, the package name must appear in that package's own `dependencies`,
`devDependencies`, `peerDependencies`, or `optionalDependencies`. If it does not, emit a finding
naming the package, the config file, and the specifier. Exit non-zero if any finding exists.

**Deliberately narrow.** Config files only — not application source. A config file's imports are
resolved by the test runner before any of the package's own code loads, so a gap there fails the whole
target rather than one test, and it is the case this repository has actually been bitten by. Keeping
scope tight is also what makes the gate cheap enough to land. Extending to source is separate work.

**A subpath import maps to its package.** `vite/client` is a `vite` requirement. Scoped packages take
the first two segments (`@vitejs/plugin-react`); unscoped take the first (`vite`).

**Ordering with WS-V1.** Written before WS-V1 lands, the gate's RED state is the real repository:
ten genuine findings. That is the strongest possible failing test, and it costs nothing to sequence
that way. If WS-V1 lands first, WS-V2's RED must instead be a fixture repository, which is weaker
evidence.

## Risks

| Risk                                              | Mitigation                                                    |
| ------------------------------------------------- | ------------------------------------------------------------- |
| A declaration silently upgrades a package         | AC-2 requires a declaration-only lockfile diff; revert if not |
| The gate false-positives on a Node builtin        | AC-3 pins `node:path` and bare builtins as non-findings       |
| The gate false-positives on a subpath import      | Name extraction is specified and unit-tested both ways        |
| The two repositories drift on gate config         | AC-4 compares `repo-config.yml` args and the parity manifest  |
| `vite` 7-vs-8 divergence is mistaken for a defect | README and this document both record it as intentional        |
