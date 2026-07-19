# Business Requirements — Rust `target/` Directory Sharing

## Business goal

Reclaim disk consumed by duplicated Rust `target/` directories across git worktrees, and keep it
reclaimed, without slowing local builds or destabilizing CI — delivered as a single, byte-identical
`rhino-cli doctor` behavior shared across all three repos.

## Business rationale

The monorepo's Rust crates produce large `target/` directories, and the repo's worktree-heavy
workflow (each plan gets its own worktree + PR to maximize parallelization) multiplies that cost:
every worktree recompiles and stores its own copy of essentially identical artifacts. The observed
result is tens of gigabytes of largely-redundant build output on the maintainer's machine.
[Judgment call: based on the maintainer's local `du` observation, not an instrumented benchmark.]

A per-crate symlink into a shared cache collapses N per-worktree copies into 1 physical directory
per repo+crate. Because `target/` is already gitignored [Repo-grounded — `.gitignore:114` `target/`],
the mechanism touches **zero tracked build configuration** in the core design.

Folding the logic into `rhino-cli doctor` — rather than a per-repo `scripts/` shell helper — makes
this a **single source of truth**. The doctor command is inside the `apps/rhino-cli/**` byte-identity
boundary [Repo-grounded — [SDLC Gate Standard](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary)],
so one Rust implementation lands byte-identically in `ose-public`, `ose-primer`, and `ose-infra`, and
the byte-identity guard actively **enforces** that they stay identical. This is simpler and more
robust than maintaining three copies of a shell script; the cost — companion Gherkin and a
byte-identical three-repo change — is exactly the discipline the boundary already imposes on every
rhino-cli change.

## Business impact

**Pain points addressed**

- **Disk exhaustion**: worktree proliferation drives `target/` duplication that can fill the disk.
- **Wasted recompilation**: identical crates rebuilt per worktree burn CPU and time.
- **Cache never GC'd**: `target/*/incremental/` grows unbounded with no maintenance path.

**Expected benefits**

- One shared `target/` per repo+crate instead of one per worktree → cross-worktree duplication
  eliminated. [Judgment call — mechanism-implied, to be confirmed by the before/after `du` gate.]
- Warm shared cache means a crate already built in one worktree is not rebuilt from scratch in
  another. [Judgment call]
- **One implementation, three repos, guaranteed identical** — no per-repo script drift; a future
  crate added to any repo is picked up automatically by the doctor's dynamic discovery. [Observable
  fact — dynamic `find`-based discovery + byte-identity guard.]
- **Safe, worktree-aware reclamation** — a repo-level GC via `rhino-cli doctor --prune-cargo-cache`
  removes only cache entries no live worktree/checkout references, so disk is reclaimed without ever
  forcing a sibling worktree to full-rebuild. [Observable fact — the GC computes the live-referenced
  set before deleting anything.]
- A documented cleanup path (`cargo clean` / `cargo sweep`) gives an explicit lever against regrowth.

## Affected roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears these hats:

- **Local developer** — the primary beneficiary; faster, lighter multi-worktree development.
- **Repo/toolchain owner** — owns `npm run doctor -- --fix`, which now creates the symlinks with no
  extra wiring.
- **rhino-cli maintainer** — owns the byte-identity boundary; must land the change identically across
  three repos with companion Gherkin.
- **CI custodian** — must ensure the mechanism never runs on the self-hosted runner (see risks).

Consuming agents: `repo-setup-manager` (runs Phase 0 + doctor), `swe-rust-dev` (implements the Rust
change), the `plan-execution` workflow (worktree provisioning), and any agent that runs
`npm run doctor -- --fix`.

## Business-level success metrics

- **Disk dedup observed**: after the mechanism is applied, a before/after `du -sh` across worktrees
  shows the shared cache is counted once rather than per worktree. [Observable fact — verified by the
  disk-verification gate in `delivery.md`.]
- **Zero build regressions**: `nx run <crate>:build` still emits the expected `dist/<bin>`, and
  `test:unit` / `test:quick` still pass through the symlinked target. [Observable fact — gated.]
- **CI unaffected**: the doctor symlink step no-ops under CI, so the known rustup/cargo concurrency
  race is not worsened. [Observable fact — gated by the CI-guard unit test + behavior scenario.]
- **Byte-identity preserved**: `apps/rhino-cli/**` (source + `specs/apps/rhino/**`) is byte-identical
  across all three repos after delivery (`diff = 0`). [Observable fact — cross-repo `diff` gate.]

## Business-scope non-goals

- Not a general build-performance optimization program; the aim is disk dedup with no regressions.
- Not a change to how CI builds or caches Rust — CI is explicitly excluded.
- Not a `scripts/`-based mechanism — the logic lives inside the doctor command (see `tech-docs.md`
  RA-1 for why the shell-helper alternative was rejected).
- **NO per-worktree target-delete hook (explicit anti-pattern).** Because the shared cache is keyed
  by `<repo>/<crate>` and NOT by worktree/branch, every worktree's per-crate `target/` symlink points
  at a cache entry **shared** by all worktrees + the main checkout of that repo. Deleting a worktree
  must therefore NEVER delete its Rust cache entry — doing so would force all sibling worktrees to
  full-rebuild and could race a live build. The correct disk-reclamation lever is the repo-level GC
  (`doctor --prune-cargo-cache`), which deletes only entries no live checkout references — never a
  hook wired to worktree teardown.

## Business risks and mitigations

| Risk                                                                                                                                               | Likelihood        | Mitigation                                                                                                                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shared target on CI worsens the self-hosted rustup/cargo `.partial` concurrency race                                                               | High if unguarded | Hard CI guard (`$CI` / `$GITHUB_ACTIONS`) no-ops the doctor symlink step; first-class acceptance criterion + dedicated unit test + behavior scenario. [Judgment call — recalled from a prior session, not documented in-repo]                                                                                                                             |
| Byte-identity drift: the rhino-cli source/specs change diverges between the three repos                                                            | Medium            | The change is authored byte-identically and verified `diff = 0` across all three repos before archival; the CI byte-identity guard blocks divergence permanently. [Repo-grounded — byte-identity boundary + guard]                                                                                                                                        |
| Concurrent local builds of the SAME crate in two worktrees contend on the cargo lock                                                               | Low               | Cargo serializes on its own `target` lock (blocks, does not corrupt); documented as an accepted local trade-off in `tech-docs.md` §Accepted trade-off: concurrent local builds of the same crate across worktrees [Web-cited there].                                                                                                                      |
| Cross-branch rebuild churn: alternating worktree branches sharing the symlinked target re-fingerprint/recompile the leaf crate + changed path-deps | Medium            | Accepted; churn confined to the leaf crate (shared deps stay cached), bounded by periodic `cargo sweep`; documented in tech-docs.md §Accepted trade-off: cross-branch rebuild churn across worktrees on different branches. [Judgment call]                                                                                                               |
| Nx caches/restores a symlinked `target` for crates that list it as an output                                                                       | Medium            | Remove `{projectRoot}/target` from the three ose-public crates' `build.outputs` (rhino-cli already excludes it). [Repo-grounded — `project.json`]                                                                                                                                                                                                         |
| GC prunes a cache entry still referenced by a live worktree/checkout, forcing a sibling full-rebuild or racing a live build                        | High if unguarded | The GC computes the live-referenced set from `git worktree list` + the main checkout BEFORE deleting; it removes only orphaned entries (crate no longer in the repo, or a `<repo>` with no known checkout) and CI-guards the whole step; `--dry-run` previews. [Repo-grounded — live-set-difference algorithm; `git worktree list --porcelain` supported] |
| Optional debuginfo-trim edit to `apps/rhino-cli/Cargo.toml` breaks byte-identity                                                                   | Medium            | The optional phase is applied byte-identically across all three repos in the same cycle; core phases never depend on it.                                                                                                                                                                                                                                  |

## Cross-references

- Testable scenarios for each success metric: [`prd.md` §Acceptance Criteria](./prd.md#acceptance-criteria).
- Design rationale and rejected alternatives: [`tech-docs.md`](./tech-docs.md).
