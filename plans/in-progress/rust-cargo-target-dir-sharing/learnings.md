<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: rust-cargo-target-dir-sharing

## Baseline measurements (filled in during Phase 0 / Phase 3)

- **Disk "before"** (Phase 0): the explicit per-worktree `du -sh` table was not captured at Phase 0
  (baseline left as a placeholder). The pre-change topology is unambiguous regardless: every rust
  crate carried its own in-tree `target/` directory, and every git worktree of the repo held its own
  independent copy — so the same four crates' build artifacts were duplicated once per worktree
  (`apps/rhino-cli/target`, `apps/ayokoding-cli/target`, `apps/ose-cli/target`, `libs/rust-commons/target`
  × N worktrees).
- **Crate `build.outputs` snapshot** (Phase 0 → Phase 3): ayokoding-cli `["{projectRoot}/dist","{projectRoot}/target"]`
  → `["{projectRoot}/dist"]`; ose-cli `["{projectRoot}/dist","{projectRoot}/target"]` → `["{projectRoot}/dist"]`;
  rust-commons `["{projectRoot}/target"]` → `[]`; rhino-cli `["{projectRoot}/dist"]` (unchanged — already
  target-free). `target/` is dropped from Nx `build.outputs` because it is now a symlink into the shared
  cache and Nx must not attempt to cache/restore a symlinked directory.
- **Disk "after"** (Phase 3): after `rhino-cli doctor --fix` replaced the four in-tree `target/` dirs with
  symlinks into `$HOME/.cache/ose-cargo-target/ose-public/<crate-leaf>`, the shared cache holds exactly one
  namespace per repo, each crate counted once:

  ```text
    0B  ~/.cache/ose-cargo-target/ose-public/rhino-cli    (built via cache-hit; no fresh artifacts)
   72M  ~/.cache/ose-cargo-target/ose-public/rust-commons
   90M  ~/.cache/ose-cargo-target/ose-public/ayokoding-cli
   90M  ~/.cache/ose-cargo-target/ose-public/ose-cli
  ```

  Dedup confirmed: the per-worktree duplication in the "before" topology is gone — all worktrees of
  `ose-public` now resolve their `target/` to this single shared `ose-public/` namespace. Nx build caching
  still hits through the symlinks (rhino-cli 1/1 from cache; ayokoding-cli 2/2 on the no-change re-run);
  `rhino-cli:test:unit`/`test:quick` pass through the symlink.

- **Three-way byte-identity `diff`** (Phase 6): _record the `diff -rq` result (expect 0) here._

<!--
Entry shape:

## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — real $HOME paths reduced to $HOME)
- **Why it might generalize**: the litmus reasoning
-->
