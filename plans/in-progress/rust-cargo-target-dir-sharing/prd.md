# Product Requirements — Rust `target/` Directory Sharing

## Product overview

A `rhino-cli doctor` check/fix step that redirects each Rust crate's `target/` directory to a shared,
persistent cache via a symlink, so multiple git worktrees of the same repo share one physical build
directory per crate. In **check** mode the doctor reports any crate whose `target/` is missing its
shared-cache symlink; in **`--fix`** mode it creates or repairs the symlinks. The step is local-dev
only and no-ops under CI.

This is not a UI-bearing or API-bearing change — it touches the Rust doctor command
(`apps/rhino-cli/src/**`), its companion Gherkin (`specs/apps/rhino/**`), non-behavioral Nx
`build.outputs` config, and governance docs. No web screens, no HTTP endpoints.

Because the doctor command is inside the `apps/rhino-cli/**` byte-identity boundary, the same source
change lands byte-identically in `ose-public`, `ose-primer`, and `ose-infra`.

## Personas

- **Local developer (maintainer)** — runs many worktrees; wants disk reclaimed and builds intact.
- **`repo-setup-manager` / `swe-rust-dev` agents** — execute Phase 0 and the Rust change; need the
  doctor step to be idempotent and side-effect-safe.
- **CI custodian** — needs an ironclad guarantee the mechanism never activates on the runner.
- **rhino-cli maintainer** — needs the change to satisfy specs coverage and byte-identity.

## User stories

- **US-1** — As a local developer, I want each crate's `target/` to point at a shared cache, so that
  ten worktrees do not store ten copies of the same build artifacts.
- **US-2** — As a repo/toolchain owner, I want `npm run doctor -- --fix` to create the symlinks
  idempotently, so that any worktree I provision is set up correctly with no manual step and no
  extra wiring.
- **US-3** — As a CI custodian, I want the doctor symlink step to no-op under CI, so that the shared
  target never worsens the self-hosted rustup/cargo concurrency race.
- **US-4** — As a maintainer, I want builds and tests to work unchanged through the symlink, so that
  the dedup carries zero functional cost.
- **US-5** — As a maintainer of three sibling repos, I want one byte-identical `doctor`
  implementation in all three, so that every machine's worktrees benefit uniformly with no per-repo
  script to maintain.
- **US-6** — As a maintainer, I want a documented cleanup path, so that the shared cache does not
  silently regrow to fill the disk.
- **US-7** — As a maintainer, I want `doctor --prune-cargo-cache` to remove only shared-cache entries
  that no live worktree or checkout references, so that I reclaim disk safely without forcing any
  sibling worktree to full-rebuild or deleting a cache entry out from under a running build.

## Acceptance criteria

> Every scenario uses exactly one primary `Given`, one `When`, and one `Then`; extras chain with
> `And`/`But` per the step-keyword cardinality HARD rule. These scenarios are the source for the
> companion `.feature` file under `specs/apps/rhino/behavior/rhino-cli/gherkin/system/`.

### Scenario: doctor --fix symlinks a crate's target into the shared cache

```gherkin
Given a Rust crate with a plain target directory exists in a repo checkout outside CI
When the developer runs the doctor command with the fix flag
Then the crate's target becomes a symlink into the shared cargo-target cache
And the symlink resolves under the repo's own shared-cache namespace
```

### Scenario: the doctor fix step is idempotent

```gherkin
Given a crate's target is already the correct symlink into the shared cache
When the developer runs the doctor command with the fix flag a second time
Then the command exits successfully without recreating or altering the symlink
```

### Scenario: doctor --fix replaces an existing plain target directory with a symlink

```gherkin
Given a crate's target is a plain rebuildable directory containing stale artifacts
When the developer runs the doctor command with the fix flag outside CI
Then the plain directory is discarded and the target becomes a symlink into the shared cache
```

### Scenario: doctor check reports a crate whose target is not yet shared

```gherkin
Given a crate's target is a plain directory not yet symlinked into the shared cache
When the developer runs the doctor command without the fix flag
Then the output reports that crate's target as needing to be shared
And the plain target directory is left unchanged
```

### Scenario: the doctor symlink step no-ops under CI

```gherkin
Given the environment variable CI is set
When the developer runs the doctor command with the fix flag
Then no target symlink is created for any crate
And the command exits successfully with a message that CI was detected
```

### Scenario: dynamic discovery covers every crate under apps and libs

```gherkin
Given a repo checkout contains multiple Rust crates under apps and libs outside CI
When the developer runs the doctor command with the fix flag
Then every discovered crate's target is a symlink into the shared cache
And no crate is skipped due to a hardcoded crate list
```

### Scenario: two worktrees of the same repo share one physical target

```gherkin
Given two worktrees of the same repo each have a crate's target symlinked by the doctor
When both symlinks are resolved
Then both point at the same shared-cache directory for that repo and crate
And a disk usage measurement across the worktrees counts that directory only once
```

### Scenario: builds and tests resolve through the symlink

```gherkin
Given a crate's target is a symlink into the shared cache
When the developer builds and tests that crate through Nx
Then the build emits the expected dist binary
And the tests pass without reference to a per-worktree target directory
```

### Scenario: the doctor change is byte-identical across the three repos

```gherkin
Given the doctor target-share change is delivered to ose-public, ose-primer, and ose-infra
When the rhino-cli source and its Gherkin specs are diffed pairwise across the three repos
Then the diff is empty for every apps/rhino-cli source file and every specs/apps/rhino feature file
```

### Scenario: Nx build caching is unaffected for crates that emit only dist

```gherkin
Given the ose-public CLIs no longer list the whole target directory in build outputs
When one of those crates is built twice with no source change
Then the second run is served from the Nx cache
And its dist binary is present after both runs
```

### Scenario: prune removes an orphaned shared-cache entry

```gherkin
Given the shared cache holds an entry for a crate that no longer exists in the repo outside CI
When the developer runs the doctor command with the prune flag
Then the orphaned cache entry is deleted
And every entry still referenced by a live worktree or checkout is preserved
```

### Scenario: prune preserves a cache entry referenced by a live worktree

```gherkin
Given a shared-cache entry is the symlink target of a crate in a live worktree
When the developer runs the doctor command with the prune flag
Then that referenced cache entry is left in place
And only entries with no live referrer are removed
```

### Scenario: the prune step no-ops under CI

```gherkin
Given the environment variable CI is set
When the developer runs the doctor command with the prune flag
Then no cache entry is deleted
And the command exits successfully with a message that CI was detected
```

### Scenario: prune dry-run previews deletions without removing anything

```gherkin
Given the shared cache holds at least one orphaned entry outside CI
When the developer runs the doctor command with the prune and dry-run flags
Then the orphaned entry is reported as a candidate for deletion
And no cache entry is actually removed
```

### Scenario: stale-artifact sweep degrades gracefully when cargo-sweep is absent

```gherkin
Given cargo-sweep is not installed on the developer's PATH
When the developer runs the doctor command with the prune flag
Then the sweep step is reported as skipped rather than failing the command
And the command exits successfully
```

## Product scope

**In scope (features)**

- The `rhino-cli doctor` target-share check/fix step (Rust), with CI guard, dynamic crate discovery,
  and idempotency.
- The `rhino-cli doctor --prune-cargo-cache` worktree-aware GC step (Rust), reusing the same crate
  discovery + CI guard: it deletes only shared-cache entries no live worktree/checkout references,
  honors `--dry-run` for preview, and runs an optional `cargo sweep` stale-artifact reclamation that
  degrades gracefully when `cargo-sweep` is absent.
- Companion Gherkin scenarios + cucumber-rs step definitions covering both the target-share and the
  prune behavior.
- Removing `{projectRoot}/target` from the three ose-public crates' `build.outputs`.
- Governance-doc updates (worktree setup, reproducible environments, cleanup guidance).
- Byte-identical propagation to `ose-primer` and `ose-infra`.

**Out of scope (features)**

- A `scripts/cargo-target-share.sh` helper or any `package.json` edit (rejected — see `tech-docs.md`
  RA-1).
- Installing `cargo-sweep` via `rhino-cli doctor` (documented/manual cleanup instead).
- Any CI runner or workflow change.
- Optional Phase 7 (`[profile.dev]` debuginfo trim) is delivered separately and may be dropped
  wholesale by the maintainer.

## Product-level risks

- **False CI detection locally** — if a developer's shell exports `CI`, the symlink step silently
  no-ops. Mitigated by the guard message ("CI detected") and documentation.
- **Cross-repo cache-name collision** — two repos with the same directory basename would share a
  cache namespace. Low risk (the three repos have distinct directory names); documented in
  `tech-docs.md`.
