<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: rhino-cli-git-root-test-fixture-race

<!--
Entry shape:

## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — real $HOME paths reduced to $HOME)
- **Why it might generalize**: the litmus reasoning
-->

## Learning: exit-status blindness in test git fixtures redirects git to the real repo

- **Context**: Root-causing `find_root_from_worktree` flakiness under cucumber-rs 64-way
  concurrency (`root.rs`, `specs_tree.rs`).
- **Observation**: the fixture ran git commands with `.output().expect(...)`, which only checks that
  the child process _spawned_ — never `status.success()`. When a `git init` failed (transient,
  under concurrency), git's upward `.git`-discovery walked out of the temp dir and bound to the
  nearest ancestor repo (the real working tree), so subsequent commands mutated the real repo's HEAD
  and local `git config user.*`. Fix: assert `output.status.success()` on every fixture git call
  (`run_checked` closure).
- **Why it might generalize**: any test that shells out to a discovery-based tool (git, npm, cargo,
  nx) inside a temp dir must assert exit status, not just spawn success — otherwise a failed setup
  silently escapes the sandbox and corrupts the host. Litmus: passes (recurring class, not one-off).

## Learning: the local `[user] Test <test@test.com>` corruption is the above bug's live footprint

- **Context**: Committing across the 3 repos; a P2 agent surfaced that ose-public + ose-primer local
  `.git/config` carried a stray `[user] name=Test email=test@test.com`.
- **Observation**: that identity is exactly what the git fixtures set on their throwaway repos; its
  presence in the _real_ repos' local config is direct evidence the exit-status-blind fixture had
  previously escaped and written host config. Per the Git Identity Guardrail an AI agent cannot
  unset it — the human ran `git config --local --unset user.name/user.email`. Always verify identity
  is the developer's own (`wahidyankf`) before committing.
- **Why it might generalize**: passes — captured durably as memory
  `project_git_identity_test_override_live_incident`. The fixture fix (above) prevents recurrence.

## Learning: the rhino-cli byte-identity gate must diff tracked content, not just changed files

- **Context**: Phase 6a/6b gate — verifying byte-identity across the 3 repos before P7.
- **Observation**: the two files this plan changed (`root.rs`, `specs_tree.rs`) were identical across
  all 3, but a full `git ls-tree` subtree-hash comparison of `apps/rhino-cli/**` revealed a
  _pre-existing_ drift: `apps/rhino-cli/README.md` in primer+infra predated the absent-scenario /
  zero-data-row `Examples:` prose that ose-public carries (and that the shared
  `specs_e2e_coverage.rs::is_unbound_or_absent` code already implements byte-identically). ose-public
  is the source of truth and its README was the accurate one, so primer+infra were synced up.
- **Why it might generalize**: passes. Verifying a byte-identity boundary by diffing only the files a
  change touched is insufficient — it misses ambient drift. The gate should compare the whole tracked
  subtree hash (`git ls-tree -r HEAD -- apps/rhino-cli specs/apps/rhino/.../gherkin`) across repos.
  Candidate hardening for the SDLC Gate Standard / a rhino-cli CI cross-repo check.

## Learning: exit-status checking is NECESSARY BUT NOT SUFFICIENT — git fixtures still escaped

- **Context**: During P7 (review cycles), running the git-root fixtures in the real worktrees
  (flaky pre-push `nx test:quick` in primer/infra + a neutered RED-proof `cargo test` in public)
  corrupted all 3 real repos: fixture commits (`init`/`Test`, `ancestor init`/`Ancestor Real Repo`)
  landed on the real branch, HEAD tree collapsed to a single `README.md`, local `user.*` overwritten,
  and the corrupted HEAD was pushed to all 3 PR branches. This happened in primer/infra WITH the
  exit-status-checked fixture in place.
- **Observation**: the tempdirs live under `$TMPDIR` (`/var/folders/...`), a different tree from the
  real repo (`~/ose-projects/...`), so git's upward `.git` discovery from a _correct_ tempdir path
  cannot reach the real repo. The escape therefore is NOT unchecked-init upward-discovery (the plan's
  confirmed mechanism) — it is a git command resolving against the wrong working directory: process-
  global `std::env::set_current_dir` (the reason `CwdLock` exists) racing under concurrency
  (cucumber-rs runs up to 64 scenarios in parallel; the unit test spawns a fixture thread alongside a
  `find_root()` call), so a command resolves via inherited CWD = real worktree instead of its tempdir.
  Exit-status checking does nothing for this vector.
- **Why it generalizes**: passes, strongly. ANY test that shells out to git is one CWD race or one
  missing `.current_dir()` away from mutating the real repo. The robust, mechanism-agnostic fix is
  defense-in-depth ISOLATION, not more assertions on one vector:
  1. `GIT_CEILING_DIRECTORIES=<tempdir>` — git will not search for `.git` above the tempdir.
  2. explicit `GIT_DIR=<tempdir>/.git` — git performs no upward discovery at all (it ignores CWD for
     locating the repo). Do NOT also set `GIT_WORK_TREE`: it misdirects `git worktree add` and makes
     the Standard-4 escape guard tautological (`git rev-parse --show-toplevel` would just echo the
     variable). The work tree is inferred from the command's CWD, which the escape guard then verifies.
  3. `GIT_CONFIG_GLOBAL=/dev/null` + `GIT_CONFIG_SYSTEM=/dev/null` — no dev-identity bleed, deterministic.
  4. a pre-write escape-guard: assert `git rev-parse --show-toplevel` == the intended tempdir (canonical)
     before ANY write; panic (fail loud) if git would resolve anywhere else.
     This is the deeper git-root fix (reopens the plan) AND a cross-repo governance convention (any
     git-touching fixture, any language). Corollary process lesson: NEVER run git-fixture tests in the
     primary/real worktree while diagnosing this class — run them in a throwaway clone, or the diagnosis
     itself corrupts the repo (as it did here).

## Triage (Phase 8 Knowledge Capture)

Litmus applied to every entry; both safety gates pass (no secrets — the `test@test.com` identity is a
synthetic fixture value, not a credential; no infra-private content, so nothing is cross-repo-gated).
Each surviving entry is routed to exactly one durable home:

- **Entries 1 + 4 (exit-status blindness; exit-status necessary-but-not-sufficient → defense-in-depth
  isolation)** → durable home: the new
  [Git Fixture Isolation Convention](../../../repo-governance/development/quality/git-fixture-isolation.md)
  (six mandatory layers), landed in this plan's own PR as its governance deliverable. `GIT_WORK_TREE`
  is documented there (and corrected above at step 2) as deliberately-unset.
- **Entry 2 (`[user] Test <test@test.com>` local-config corruption is the bug's live footprint)** →
  durable home: memory `project_git_identity_test_override_live_incident` (already captured). No repo
  change — the fixture fix prevents recurrence and the Git Identity Guardrail keeps remediation human-only.
- **Entry 3 (byte-identity gate must diff the whole tracked subtree, not just changed files)** →
  code-routing learning → durable home: `plans/ideas.md` standing-idea for a tri-repo `apps/rhino-cli`
  subtree-hash CI gate (the `rhino-cli-source-drift-reconciliation` after-action, added 2026-07-17).
  Per the code-routing rule it is NOT landed inline here; it lives as a future backlog candidate. This
  plan's Phase 6a/6b gate already adopted the full-subtree-hash comparison manually.

No un-homed generalizable learning remains.
