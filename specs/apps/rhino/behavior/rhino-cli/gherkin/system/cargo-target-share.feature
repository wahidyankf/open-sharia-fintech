@cargo-target-share
Feature: Shared Cargo Target Directories via Doctor

  As a local developer working across many git worktrees
  I want each Rust crate's target/ directory to point at a shared, persistent cache
  So that ten worktrees do not store ten copies of the same build artifacts

  Scenario: doctor --fix symlinks a crate's target into the shared cache
    Given a Rust crate with a plain target directory exists in a repo checkout outside CI
    When the developer runs the doctor command with the fix flag
    Then the crate's target becomes a symlink into the shared cargo-target cache
    And the symlink resolves under the repo's own shared-cache namespace

  Scenario: the doctor fix step is idempotent
    Given a crate's target is already the correct symlink into the shared cache
    When the developer runs the doctor command with the fix flag a second time
    Then the command exits successfully without recreating or altering the symlink

  Scenario: doctor --fix replaces an existing plain target directory with a symlink
    Given a crate's target is a plain rebuildable directory containing stale artifacts
    When the developer runs the doctor command with the fix flag outside CI
    Then the plain directory is discarded and the target becomes a symlink into the shared cache

  Scenario: doctor check reports a crate whose target is not yet shared
    Given a crate's target is a plain directory not yet symlinked into the shared cache
    When the developer runs the doctor command without the fix flag
    Then the output reports that crate's target as needing to be shared
    And the plain target directory is left unchanged

  Scenario: the doctor symlink step no-ops under CI
    Given the environment variable CI is set
    When the developer runs the doctor command with the fix flag
    Then no target symlink is created for any crate
    And the command exits successfully with a message that CI was detected

  Scenario: dynamic discovery covers every crate under apps and libs
    Given a repo checkout contains multiple Rust crates under apps and libs outside CI
    When the developer runs the doctor command with the fix flag
    Then every discovered crate's target is a symlink into the shared cache
    And no crate is skipped due to a hardcoded crate list

  Scenario: two worktrees of the same repo share one physical target
    Given two worktrees of the same repo each have a crate's target symlinked by the doctor
    When both symlinks are resolved
    Then both point at the same shared-cache directory for that repo and crate
    And a disk usage measurement across the worktrees counts that directory only once

  Scenario: builds and tests resolve through the symlink
    Given a crate's target is a symlink into the shared cache
    When the developer builds and tests that crate through Nx
    Then the build emits the expected dist binary
    And the tests pass without reference to a per-worktree target directory

  Scenario: the doctor change is byte-identical across the three repos
    Given the doctor target-share change is delivered to ose-public, ose-primer, and ose-infra
    When the rhino-cli source and its Gherkin specs are diffed pairwise across the three repos
    Then the diff is empty for every apps/rhino-cli source file and every specs/apps/rhino feature file

  Scenario: Nx build caching is unaffected for crates that emit only dist
    Given the ose-public CLIs no longer list the whole target directory in build outputs
    When one of those crates is built twice with no source change
    Then the second run is served from the Nx cache
    And its dist binary is present after both runs

  Scenario: prune removes an orphaned shared-cache entry
    Given the shared cache holds an entry for a crate that no longer exists in the repo outside CI
    When the developer runs the doctor command with the prune flag
    Then the orphaned cache entry is deleted
    And every entry still referenced by a live worktree or checkout is preserved

  Scenario: prune preserves a cache entry referenced by a live worktree
    Given a shared-cache entry is the symlink target of a crate in a live worktree
    When the developer runs the doctor command with the prune flag
    Then that referenced cache entry is left in place
    And only entries with no live referrer are removed

  Scenario: prune from the main worktree preserves an entry referenced only by a linked worktree
    Given a shared-cache entry is referenced only by a crate in a separate linked worktree
    When the developer runs the doctor command with the prune flag
    Then the entry referenced only by the linked worktree is left in place
    And the orphaned cache entry is deleted

  Scenario: the prune step no-ops under CI
    Given the environment variable CI is set
    When the developer runs the doctor command with the prune flag
    Then no cache entry is deleted
    And the command exits successfully with a message that CI was detected

  Scenario: prune dry-run previews deletions without removing anything
    Given the shared cache holds at least one orphaned entry outside CI
    When the developer runs the doctor command with the prune and dry-run flags
    Then the orphaned entry is reported as a candidate for deletion
    And no cache entry is actually removed

  Scenario: stale-artifact sweep degrades gracefully when cargo-sweep is absent
    Given cargo-sweep is not installed on the developer's PATH
    When the developer runs the doctor command with the prune flag
    Then the sweep step is reported as skipped rather than failing the command
    And the command exits successfully
