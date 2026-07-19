---
title: "Git Fixture Isolation Convention"
description: Defense-in-depth mandate for any test or fixture that shells out to git to build throwaway repositories -- caps upward discovery, forces explicit repo targeting, blanks identity/config, and asserts a pre-write escape guard so a fixture can never mutate the real repository
category: explanation
subcategory: development
tags:
  - testing
  - git
  - test-fixtures
  - isolation
  - regression
  - safety
  - defense-in-depth
created: 2026-07-19
---

# Git Fixture Isolation Convention

Any automated test or fixture -- in any language, in any repository -- that invokes `git` to
create or mutate a throwaway repository MUST make it structurally impossible for that `git`
invocation to touch the real repository. A single safety check (checking the subprocess exit
status, for example) is **necessary but not sufficient**. This convention mandates
**defense-in-depth**: six independent layers, each catching a different escape mechanism, so that
no single gap can let a fixture corrupt the repository it was supposed to leave untouched.

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Checking a
  `git` subprocess's exit status is a natural, necessary first response to a fixture-escape
  symptom -- but it treats "the command failed" as the only failure mode. The motivating incident's
  `git` commands never failed; they succeeded against the wrong repository, which exit-status
  checking cannot detect even in principle. A fix that only catches command failure, not command
  success-against-the-wrong-target, addresses a symptom, not the cause. This convention names the
  real cause (ambient, CWD-dependent git repository discovery) and closes it structurally.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  Ambient git repository discovery -- walking up from the process's current working directory
  until a `.git` is found -- is the implicit mechanism this convention forbids. Every fixture
  must state explicitly, via environment variables, which repository it targets. Nothing about
  which repository a git fixture touches should ever depend on which directory a process happened
  to be in when the command ran.

- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: A fixture
  whose correctness depends on the process-global current working directory is non-deterministic
  under concurrency -- the exact failure mode this convention exists to prevent. A fixture that
  fully specifies its target repository via `GIT_DIR`/`GIT_WORK_TREE`/`GIT_CEILING_DIRECTORIES`
  behaves identically regardless of how many other tests, threads, or scenarios are running
  concurrently.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**:
  The pre-write escape guard (Standard 4) is an automated, fail-loud check that runs before every
  write operation -- it does not depend on a human noticing that a fixture "looks risky." A
  reviewer or checker agent can grep for the required isolation environment variables and the
  guard call, rather than manually auditing every fixture's control flow for CWD-dependence.

## Conventions Implemented/Respected

This convention implements/respects the following conventions:

- **[Regression Test Mandate](./regression-test-mandate.md)**: Adding an exit-status assertion in
  response to a single observed fixture-escape symptom is exactly the kind of narrowly-scoped fix
  that mandate's spirit calls for -- but on its own it is a check for command _failure_, not for
  command _success against the wrong repository_, which is the actual defect class the motivating
  incident revealed. This convention supplies the durable, defense-in-depth rule that a narrow
  exit-status check is missing. Standard 5 below (exit-status checking) is explicitly retained as
  one of the six required layers, not replaced.

- **[Three-Level Testing Standard](./three-level-testing-standard.md)**: CLI apps in this monorepo
  (`rhino-cli`, `ayokoding-cli`, `ose-cli`) run integration tests against real `/tmp` filesystem
  fixtures per that standard's "CLI App Implementation Pattern." Any such fixture that also shells
  out to `git` (to build a throwaway repository as test data) is squarely inside this convention's
  scope -- the isolation boundary the Three-Level Testing Standard draws around the filesystem must
  extend to the git repository state living inside that filesystem, not stop at the directory
  boundary alone.

- **[Reproducible Environments Convention (Git Identity Guardrail)](../workflow/reproducible-environments.md)**:
  That convention's Git Identity Guardrail prohibits any agent from writing a `[user]` override
  into a repository's `.git/config` at any scope. This convention addresses the same class of
  corruption reached through a different door: an automated fixture, not a human edit or an agent
  command, writing `user.name`/`user.email` into the real repository's local config. Standard 3
  (identity/config hygiene) is this convention's analogue of that guardrail, scoped to fixtures
  rather than to commits or agent actions.

## Purpose

Fixtures and tests that build throwaway git repositories are common across this polyglot
monorepo -- CLI integration tests exercising `git` plumbing, unit tests verifying repository-root
resolution, BDD scenario runners that construct scratch repos as test data. Every one of these
shells out to a real `git` binary. `git` was designed to discover the repository it should
operate on by walking upward from the current working directory (or by following `GIT_DIR`),
which is exactly the right default for a human sitting in a terminal and exactly the wrong
default for a concurrent test process whose current working directory is process-global, shared,
mutable state.

This convention exists so that a bug in test concurrency, a stray `TMPDIR` misconfiguration, or a
forgotten `.env()` call can **never** result in a `git` command executing against the real
repository -- not "usually won't," not "shouldn't," but structurally cannot, because every layer
of ambient repository resolution has been closed off in code, and any residual escape trips a
loud, immediate failure before a single write happens.

## Scope

### What This Convention Covers

- Any test, fixture, or test-support helper -- in Rust, Go, TypeScript, Python, F#/.NET, or any
  other language used in this monorepo or its sibling repos -- that invokes the `git` binary to
  **create or mutate** a throwaway repository (`git init`, `git commit`, `git config`,
  `git worktree add`, `git branch`, `git checkout -b`, `git reset --hard`, and equivalents).
- Fixtures that build throwaway repositories as test data for CLI apps, libraries, or BDD scenario
  runners (including this monorepo's cucumber-style `harness = false` binaries, per the [Rust
  Testing Standards](../../../docs/explanation/software-engineering/programming-languages/rust/testing-standards.md)
  doc's coverage of that pattern).
- Plain exit-status checking on `git` subprocess invocations, wherever it already exists (Standard
  5 below retains and contextualizes it as one of six required layers; it does not replace it).

### What This Convention Does NOT Cover

- **Read-only git commands against the real repository in tests** (e.g. a unit test that calls
  `git rev-parse --show-toplevel` against the actual repo to verify repository-root resolution,
  with nothing written). There is nothing to mutate, so there is no escape to guard against. See
  `find_root_returns_repo_root` in `apps/rhino-cli/src/infrastructure/git/root.rs` for an example
  of an in-scope-adjacent, out-of-scope-by-mutation-boundary test.
- **Production code paths that intentionally operate on the real repository** (e.g. `rhino-cli git
pre-commit`, or any git hook logic that is _supposed_ to read/write the checkout it runs in).
  This convention governs test fixtures building **throwaway** repositories, not application code
  whose job is to touch the real one.
- **Which test level a git-fixture test belongs to** (unit vs. integration) -- that classification
  is governed by the [Three-Level Testing Standard](./three-level-testing-standard.md); this
  convention only governs how such a fixture must isolate itself once its level is decided.
- **General process-global mutable-state hazards unrelated to git** (e.g. environment variable
  leakage between unrelated tests) -- out of scope here; this convention is specific to git
  repository resolution.

## The Motivating Incident

A Rust test fixture in `apps/rhino-cli`
(`find_root_from_worktree_returns_worktree_path`, in
`apps/rhino-cli/src/infrastructure/git/root.rs`) builds a throwaway git repository and a linked
worktree to exercise repository-root resolution. Under parallel `nx affected`/`nx run-many`
invocations (`test:quick` fanning out across roughly two dozen projects), this fixture has
repeatedly corrupted the **real** repository it runs inside rather than staying isolated to its
throwaway sandbox: an unexpected `"init"` commit -- authored by the fixture's hardcoded
`Test <test@test.com>` identity -- landed directly on the real working branch on top of the last
real commit, immediately before or during a `git push`; `git worktree list` additionally showed
`prunable` linked worktrees registered against the real `.git`, checked out to the stray-commit
SHAs; and the real repository's local `git config user.*` was left overwritten to
`Test <test@test.com>`, mis-attributing authorship on several already-pushed commits until a
human restored the local identity by hand (per this repo's Git Identity Guardrail, no AI agent
may set it). Each occurrence was repaired without data loss via `git reflog` plus a non-destructive
`git reset` -- the corruption only ever moved the branch pointer, never altered real working-tree
file contents -- but the exposure was real: an automated fixture, unsupervised, mutated the branch
history and identity config of the repository it ran inside.

**Root-cause confirmation for this specific fixture is the explicit subject of a dedicated plan**,
in progress at `plans/in-progress/rhino-cli-git-root-test-fixture-race/` at the time of this
writing (search the `plans/` tree by that slug if this convention is read after the plan archives
to `plans/done/` -- not hyperlinked directly here because that path moves on archival). As of this
convention's authoring, direct code inspection already rules out the
simplest hypothesis: the fixture already constructs both repositories as `tempfile::TempDir`
instances and passes an explicit `.current_dir(...)` to every `git` invocation -- it does not call
`std::env::set_current_dir` at all. The remaining, still-unconfirmed hypotheses on record are (a) a
subtler CWD- or temp-dir-resolution dependency inside the fixture itself, (b) the OS temp
directory (`TMPDIR`) resolving to a path under the real repository in some environment, or (c) a
cross-process interaction under `nx affected`'s parallel project fanout rather than a
single-process thread race. **This convention does not resolve which hypothesis is correct** --
that is the companion plan's job, scoped to this one fixture. What this convention establishes is
the general rule those findings only confirm the need for: **a fixture's isolation must not depend
on correctly guessing which of several plausible escape mechanisms applies.** Defense-in-depth
closes all of them at once, regardless of which one turns out to be the confirmed cause here.

That is also why exit-status checking, as a first response to a fixture-escape symptom, is
structurally insufficient on its own: whichever of the above mechanisms is eventually confirmed,
the `git` commands involved still exit `0`. They do not fail -- they simply run against the wrong
repository. **A command that succeeds against the wrong target is indistinguishable, by exit code
alone, from a command that succeeds against the right one.** Any fix that stops at "assert the
subprocess exited zero" cannot, even in principle, catch this class of defect; it must be paired
with the other five layers below, each of which closes a specific _targeting_ mechanism rather
than a _failure_ mode.

This hazard class was already partially recognized in this codebase before the incident:
`apps/rhino-cli/src/test_support.rs` documents a `CwdLock` mutex specifically because "the process
current-working-directory (cwd) is global mutable state" and "several unit tests spawn `git` child
processes whose behaviour depends on the cwd." `CwdLock` serializes cwd-sensitive tests **within
one process** so they cannot race each other on `set_current_dir` -- but the fixture at the center
of this incident does not call `set_current_dir` and does not use `CwdLock`, so `CwdLock`'s
existence did not prevent this incident. It is evidence the general hazard class was already
partially visible in this codebase, not evidence that this specific incident was closed by it --
and, by itself, `CwdLock` supplies none of the six layers below (explicit `GIT_DIR`
targeting, capped discovery, blanked identity/config, or a pre-write escape guard).

## The Rule: Six Mandatory Layers

Every test or fixture in scope (see [Scope](#scope) above) MUST implement **all six** of the
following layers. None of the six is optional, and none substitutes for another -- each closes a
distinct escape mechanism (see [Why Defense-in-Depth](#why-defense-in-depth-not-a-single-assertion)
below for the mapping).

### Standard 1: Cap Discovery (`GIT_CEILING_DIRECTORIES`)

Set `GIT_CEILING_DIRECTORIES` to the fixture's temp root so `git` never searches for a `.git`
directory above it, no matter what else goes wrong.

```rust
cmd.env("GIT_CEILING_DIRECTORIES", tempdir.path());
```

**Why**: `git`'s default repository discovery walks upward from the working directory until it
finds a `.git`. If a fixture's temp directory itself lacks a `.git` at the moment a command runs
(a race during setup, an `init` that has not completed, a `TMPDIR` misconfiguration placing the
temp root under the real repository), discovery keeps walking upward -- potentially all the way to
the real repository. Capping the ceiling makes that upward walk terminate at the fixture's own
root, with no repository found beyond it, rather than continuing until it finds one.

### Standard 2: No Ambient Discovery (explicit `GIT_DIR`)

Set explicit `GIT_DIR=<tempdir>/.git` (or the language equivalent) so `git` performs **zero**
upward discovery. Never rely on the process CWD (`Command::current_dir`, `exec.Cmd.Dir`, `cwd:` in
`child_process`, `cwd=` in `subprocess`, `ProcessStartInfo.WorkingDirectory`) to select the
repository.

```rust
cmd.env("GIT_DIR", tempdir.path().join(".git"));
```

**Why**: This is the layer that most directly closes the CWD-race vector from the motivating
incident. When `GIT_DIR` is set, `git` does not consult the current working directory to decide
which repository to operate on at all -- discovery is bypassed entirely, in favor of the explicit
path given. A concurrent `set_current_dir` call racing against this command has no effect on which
repository it targets, because the command never looks at CWD to begin with. This is also the layer
that keeps a plain `git config user.name` (a **local**-scoped write by default) confined to the
fixture's own `.git/config` -- with `GIT_DIR` correct, there is no other local config file for that
write to land in.

**On `GIT_WORK_TREE`**: pinning `GIT_WORK_TREE=<tempdir>` is **optional** and, for two common cases,
must be **omitted**:

- **`git worktree add`** derives the linked worktree's location from its explicit path argument; a
  set `GIT_WORK_TREE` misdirects it, so leave it unset for that subcommand (explicit `GIT_DIR` alone
  still isolates the write).
- **The Standard 4 escape guard** relies on `git rev-parse --show-toplevel` genuinely resolving the
  work tree from `GIT_DIR`. A set `GIT_WORK_TREE` makes `--show-toplevel` merely echo that variable,
  rendering the guard tautological and useless.

For plain write sequences (`init`/`add`/`commit`/`config`) with the fixture's CWD already at the
tempdir root, explicit `GIT_DIR` is sufficient; `GIT_WORK_TREE` adds nothing there either. The
reference fixtures (`apps/rhino-cli/src/infrastructure/git/root.rs`, `apps/rhino-cli/tests/specs_tree.rs`)
therefore set `GIT_DIR` but not `GIT_WORK_TREE`.

### Standard 3: Identity/Config Hygiene (`GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM`)

Set `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_SYSTEM=/dev/null` so the developer's real
identity/config never bleeds **into** the fixture, and the fixture's own throwaway identity never
writes **out** to the developer's real global config.

```rust
cmd.env("GIT_CONFIG_GLOBAL", "/dev/null")
   .env("GIT_CONFIG_SYSTEM", "/dev/null");
```

**Why**: Standard 2 confines _local_-scoped config writes to the fixture's own repository. This
layer covers the two directions Standard 2 does not: (a) a fixture that reads config before it has
set its own values could otherwise pick up the developer's real name/email from `~/.gitconfig`,
silently contaminating throwaway commits with real identity; (b) a fixture (or a future refactor
of one) that issues a `--global` write -- intentionally or by a typo dropping `--local` -- would
otherwise land in the developer's actual `~/.gitconfig`, corrupting it for every other repository
on the machine. Blanking both scopes removes both directions at once.

### Standard 4: Pre-Write Escape Guard

Before **any** write command, assert that `git rev-parse --show-toplevel` resolves to the intended
temp directory (canonicalized); panic/fail-loud if it resolves anywhere else. This catches every
escape mechanism -- CWD race, `TMPDIR`-under-repo, a missed `.env()` call in a future refactor, or
any discovery path not enumerated above -- at the source, before a single write happens, rather
than after the real repository has already been corrupted.

```rust
fn assert_repo_root_is(expected: &Path) -> Result<()> {
    let output = Command::new("git")
        .args(["rev-parse", "--show-toplevel"])
        .current_dir(expected)
        .env("GIT_CEILING_DIRECTORIES", expected)
        .env("GIT_DIR", expected.join(".git"))
        // GIT_WORK_TREE is deliberately NOT set here: it would make
        // `--show-toplevel` merely echo the variable, defeating the guard.
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null")
        .output()
        .context("escape guard: failed to invoke git rev-parse")?;

    let resolved = PathBuf::from(String::from_utf8(output.stdout)?.trim());
    let resolved_canonical = resolved
        .canonicalize()
        .context("escape guard: failed to canonicalize resolved repo root")?;
    let expected_canonical = expected
        .canonicalize()
        .context("escape guard: failed to canonicalize expected repo root")?;

    if resolved_canonical != expected_canonical {
        panic!(
            "git fixture escape guard tripped: expected repo root {expected_canonical:?}, \
             git resolved {resolved_canonical:?} -- refusing to run a write command \
             against the wrong repository"
        );
    }
    Ok(())
}
```

Call this guard immediately before every write subcommand (`commit`, `config`, `worktree add`,
`branch`, `checkout -b`, `reset --hard`, etc.) in the fixture's sequence -- not just once at setup.
A fixture that only checks once, before its first write, still leaves every subsequent write
unguarded against a race that develops mid-sequence.

### Standard 5: Exit-Status Checking

Check the exit status of **every** `git` subprocess the fixture invokes. This is the obvious,
necessary first layer -- it is the layer that catches genuine command failure (missing binary,
malformed arguments, a temp directory that was never created). What it does **not** catch is a
command that succeeds against the wrong repository, which is exactly why Standards 1-4 exist
alongside it, not instead of it.

```rust
let output = cmd.output().context("git subprocess failed to spawn")?;
if !output.status.success() {
    anyhow::bail!(
        "git command failed: {}",
        String::from_utf8_lossy(&output.stderr)
    );
}
```

**Do not use `.output().expect(...)` alone as an exit-status check.** `Command::output()` (Rust),
like most languages' equivalents, returns successfully whenever the child process was spawned and
ran to completion -- it does not itself inspect the child's exit code. Only reading
`output.status.success()` (or the language equivalent) verifies the command actually succeeded;
a bare `.expect("git init")` on the `Output` value only fails if `git` could not be spawned at
all, and silently accepts a `git` command that ran and failed.

### Standard 6: Process Rule -- Never Diagnose in the Primary Worktree

Never diagnose, debug, or manually re-run this class of fixture in the primary/real worktree. Use
a throwaway clone. A fixture that is failing, or whose isolation fix is only partially applied, is
by definition in the exact state where the other five layers have not yet been verified -- running
it directly against the primary checkout during that window is what turns a caught defect into an
unrecoverable incident.

```bash
# Diagnose in a disposable clone, never in the primary checkout
git clone --no-hardlinks /path/to/primary-repo /tmp/scratch-diagnosis
cd /tmp/scratch-diagnosis
cargo test --lib the_failing_fixture_test -- --nocapture
# Discard the clone when done: rm -rf /tmp/scratch-diagnosis
```

This is a process rule, not a code-level check -- it applies to the human or agent operating the
fixture, not to the fixture's own source. It cannot be automated away by the other five layers,
because those layers protect a fixture that is already correctly written; this rule protects the
window during which it is not yet known whether that is true.

## Why Defense-in-Depth (Not a Single Assertion)

Each layer closes a distinct escape mechanism. No single layer covers all of them, which is why
all six are mandatory rather than any one being sufficient on its own -- and why the rule does not
wait on confirming any single mechanism as _the_ cause before applying. The first three rows map
directly onto the three still-unconfirmed hypotheses from
[The Motivating Incident](#the-motivating-incident); the point of defense-in-depth is that a
fixture built to this convention is protected under **any** of them, not just whichever one a
future investigation confirms.

| Escape mechanism                                                                                                                                                               | Layer(s) that catch it                                                               | Why exit-status checking alone misses it                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| A subtler CWD- or temp-dir-resolution dependency inside the fixture itself, including a process-global CWD raced by a concurrent thread/scenario (`set_current_dir` collision) | Standard 2 (explicit `GIT_DIR`) + Standard 4 (guard)                                 | The command still exits `0` -- it ran successfully, just against the real repository                       |
| `TMPDIR` resolves under the real repository (misconfigured env, CI runner quirk)                                                                                               | Standard 1 (`GIT_CEILING_DIRECTORIES`) + Standard 4 (guard)                          | Discovery finds the real `.git` above the fixture path; the command exits `0`                              |
| Cross-process interaction under parallel `nx affected`/`nx run-many` project fanout (multiple test invocations touching the same working tree concurrently)                    | Standard 1 + Standard 2 + Standard 4 (guard)                                         | Each individual process's commands can exit `0` even while colliding with another concurrently running one |
| Fixture omits `git init`, or runs it against the wrong directory, so ambient discovery walks up to the real repo                                                               | Standard 2 + Standard 4                                                              | Same as above -- success against the wrong repository, exit code `0`                                       |
| Fixture's `git config user.name`/`user.email` write escapes to the developer's real identity or the real repo's local config                                                   | Standard 2 (local writes stay inside `GIT_DIR`) + Standard 3 (global/system blanked) | The config write succeeds; nothing about exit status reveals which file it targeted                        |
| `git` binary missing, malformed arguments, or the fixture's temp directory was never created                                                                                   | Standard 5 (exit-status check)                                                       | This is the one class Standard 5 alone genuinely catches -- it remains necessary                           |
| A future code review misses a partially-applied isolation fix in a fixture under active debugging                                                                              | Standard 6 (process rule: throwaway clone only)                                      | None of the code-level layers protect the primary worktree while a fix is incomplete                       |

## Language-Agnostic Equivalents

This convention is deliberately language-agnostic: any language in this polyglot monorepo that
shells out to `git` in a test fixture must implement the same six layers using its own subprocess
API's environment-variable and working-directory controls.

| Language / stack  | Env-var injection API                                                  | Notes                                                                                                                   |
| ----------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Rust              | `std::process::Command::env(...)`                                      | Pattern used throughout this document; matches `rhino-cli`, `ayokoding-cli`, `ose-cli`                                  |
| Go                | `exec.Cmd.Env` (append to `os.Environ()`, do not replace it wholesale) | Must append, not overwrite -- a fully replaced `Env` drops `PATH`, breaking `git` resolution                            |
| TypeScript / Node | `child_process.spawn(cmd, args, { env: { ...process.env, ... } })`     | Same append-not-replace rule as Go                                                                                      |
| Python            | `subprocess.run([...], env={**os.environ, ...})`                       | Same append-not-replace rule                                                                                            |
| F# / .NET         | `ProcessStartInfo.EnvironmentVariables[...]`                           | `ProcessStartInfo` inherits the parent environment by default; only add the isolation keys, do not clear the collection |

The pre-write escape guard (Standard 4) and the process rule (Standard 6) translate directly --
every language can shell out to `git rev-parse --show-toplevel` with the same isolation env vars
and canonicalize-and-compare the result before any write.

## Examples

### FAIL: The fixture at the center of the motivating incident

`apps/rhino-cli/src/infrastructure/git/root.rs`'s
`find_root_from_worktree_returns_worktree_path` test builds a throwaway repository and a linked
worktree using raw `git` invocations with none of the six layers applied:

```rust
// Excerpt as of this convention's authoring -- none of the six layers applied
Cmd::new("git")
    .args(["init"])
    .current_dir(main)
    .output()
    .expect("git init"); // does NOT check output.status.success()

Cmd::new("git")
    .args(["config", "user.email", "test@test.com"])
    .current_dir(main)
    .output()
    .expect("git config email"); // same gap
```

This is not a hypothetical -- it is the actual fixture behind the repeated real-repository
corruption described in [The Motivating Incident](#the-motivating-incident) above. It has **zero**
structural defense against any of the six layers: no `GIT_CEILING_DIRECTORIES`, no
`GIT_DIR`/`GIT_WORK_TREE`, no `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`, no pre-write escape guard,
and `.output().expect(...)` does not actually check exit status for the `init`/`config`/`add`/
`commit` calls (only the later `git worktree add` call in the same test checks
`status.success()`). Its dedicated companion plan (see the Motivating Incident section) owns
confirming the exact interacting mechanism and landing the fix in this file; this convention
supplies the durable rule that fix -- and every other git fixture in this monorepo and its
siblings, present and future -- must satisfy. This document does not itself remediate this file.

### PASS: All six layers applied

```rust
fn init_throwaway_repo(tempdir: &Path) -> Result<()> {
    let run_git = |args: &[&str]| -> Result<()> {
        let output = Command::new("git")
            .args(args)
            .current_dir(tempdir)
            .env("GIT_CEILING_DIRECTORIES", tempdir)                 // Standard 1
            .env("GIT_DIR", tempdir.join(".git"))                    // Standard 2 (explicit GIT_DIR)
            .env("GIT_CONFIG_GLOBAL", "/dev/null")                   // Standard 3
            .env("GIT_CONFIG_SYSTEM", "/dev/null")                   // Standard 3
            .output()
            .context("git subprocess failed to spawn")?;
        if !output.status.success() {                                // Standard 5
            anyhow::bail!("git {:?} failed: {}", args, String::from_utf8_lossy(&output.stderr));
        }
        assert_repo_root_is(tempdir)?;                                // Standard 4, after every write
        Ok(())
    };

    run_git(&["init"])?;
    run_git(&["config", "user.email", "fixture@test.local"])?;
    run_git(&["config", "user.name", "Fixture"])?;
    run_git(&["commit", "--allow-empty", "-m", "init"])?;
    Ok(())
}
```

`GIT_WORK_TREE` is intentionally absent (see Standard 2): explicit `GIT_DIR` alone isolates these
writes, and omitting `GIT_WORK_TREE` keeps the same helper usable for a subsequent `git worktree
add <path> HEAD` (which derives the linked worktree from its path argument). Standard 6 -- never
diagnosing this fixture in the primary worktree -- is a process rule and does not appear in the code
sample; see Standard 6 above.

## Enforcement

- **`swe-code-checker`**: Locates test/fixture files that shell out to a raw `git` invocation
  (`Command::new("git")` in Rust, `exec.Command("git"` in Go, `child_process.spawn/exec("git"` in
  TypeScript, `subprocess.run/Popen([...,"git"` in Python, `ProcessStartInfo` targeting `git` in
  F#/.NET) and verifies all six layers are present -- the four mandatory isolation env vars
  (`GIT_CEILING_DIRECTORIES`, `GIT_DIR`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`) set on or near the
  invocation, a pre-write escape-guard call before write subcommands, and an exit-status check that
  actually inspects `status.success()` (not a bare `.expect()` on the `Output` value).
  `GIT_WORK_TREE` is context-dependent, not mandatory: it must be **absent** for `git worktree add`
  and for the escape guard (see Standard 2), so its absence is never on its own a finding. A fixture
  missing any of the four mandatory env vars, the escape guard, or the exit-status check is a finding.

  **Criticality**: **CRITICAL** -- per the
  [Criticality Levels Convention](./criticality-levels.md), this maps to "data loss risks" and
  "violations of MUST requirements in conventions." A missing layer here is not a style deviation;
  it is the exact gap that let a real incident corrupt the primary repository.

  A grep-based heuristic for locating candidates:

  ```bash
  rg -l 'Command::new\("git"\)|exec\.Command\("git"|child_process\.(spawn|exec(File)?)\("git"|subprocess\.(run|Popen)\(\s*\[?"git"|ProcessStartInfo\(.*"git"' \
    -g '*test*' -g '*fixture*' -g '*spec*'
  ```

  For each match, verify the five isolation env vars, the escape-guard call, and a real
  `status.success()`-style check all appear in the same function or in a shared helper the
  function calls.

- **`repo-rules-checker`**: May additionally audit that this convention itself stays cross-referenced
  from [Regression Test Mandate](./regression-test-mandate.md),
  [Three-Level Testing Standard](./three-level-testing-standard.md), and
  [Reproducible Environments Convention](../workflow/reproducible-environments.md), per
  the standard convention-integration checklist.

## Completeness Checklist

Before landing a test fixture that shells out to `git` to build a throwaway repository, verify:

- [ ] `GIT_CEILING_DIRECTORIES` is set to the fixture's temp root (Standard 1)
- [ ] `GIT_DIR` is set explicitly; no `git` invocation in the fixture relies on
      `current_dir()`/process CWD to select the repository (Standard 2). `GIT_WORK_TREE` is optional
      and must be **absent** for `git worktree add` and the escape guard.
- [ ] `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_SYSTEM=/dev/null` are set (Standard 3)
- [ ] A pre-write escape guard runs before every write command, comparing canonicalized
      `git rev-parse --show-toplevel` output against the intended tempdir, panicking/failing loud
      on mismatch (Standard 4)
- [ ] Every `git` subprocess's exit status is checked via `status.success()` or the language
      equivalent -- not inferred from a bare `.expect()`/try-catch around the spawn call alone
      (Standard 5)
- [ ] Anyone diagnosing a failing instance of this fixture does so in a throwaway clone, never the
      primary/real worktree (Standard 6 -- a process discipline, not a code check)

## Related Documentation

- [Regression Test Mandate](./regression-test-mandate.md) -- The bug-driven-fix convention this
  document extends: an exit-status assertion alone is a regression-test-style patch that is
  necessary but not sufficient for this defect class; this convention supplies the durable
  defense-in-depth a narrow exit-status check lacks.
- [Three-Level Testing Standard](./three-level-testing-standard.md) -- CLI-app integration tests
  that use real `/tmp` filesystem fixtures are the primary home for git-fixture tests in this
  monorepo; this convention governs their isolation once their test level is chosen.
- [Reproducible Environments Convention (Git Identity Guardrail)](../workflow/reproducible-environments.md) --
  The repository-wide policy that no AI agent sets or modifies git identity at any scope, protecting
  the real repository's identity config from **manual** edits and direct agent commands. The
  motivating incident for this convention is a concrete illustration of how that guardrail can be
  violated **by automation** rather than by direct agent action: a fixture bug, not an agent
  editing `.git/config` directly, produced the identity corruption. This convention is the
  test-fixture-specific defense that keeps automated code from becoming the guardrail's blind spot.
- [CI Blocker Resolution Convention](./ci-blocker-resolution.md) -- Shares this convention's stance
  that a discovered defect must be fixed at the root cause, not bypassed with a partial patch.
- [Criticality Levels Convention](./criticality-levels.md) -- Defines the CRITICAL severity this
  convention's enforcement findings use.
