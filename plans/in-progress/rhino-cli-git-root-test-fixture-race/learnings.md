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
