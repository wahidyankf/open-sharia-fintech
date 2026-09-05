@gate @unit
Feature: Gate execution

  Scenario: A configured surface guard re-executes the complete gate run exactly once
    Given pre-push has a configured execution guard and a recording gate
    When the guarded gate runs with an only selector
    Then the guard receives the complete gate run arguments
    And the guard runs exactly once
    And the selected gate still runs

  Scenario: An active surface guard marker prevents recursive re-execution
    Given pre-push has a configured execution guard and a recording gate
    When the gate runs with the configured guard marker active
    Then the guard is bypassed
    And the selected gate still runs

  Scenario: A surface guard child exit code is preserved
    Given pre-push has a configured execution guard that exits with code 23
    When the guarded pre-push surface runs
    Then gate run exits with code 23

  Scenario: A configured surface guard fails closed when it cannot start
    Given pre-push has a missing configured execution guard and a recording gate
    When the guarded pre-push surface runs
    Then gate run fails without running the selected gate

  Scenario: An unconfigured surface executes gates directly
    Given pre-push has no execution guard and has a recording gate
    When the guarded pre-push surface runs
    Then the selected gate runs without a guard invocation

  Scenario: Rhino CLI kind receives derived files
    Given a rhino-cli gate matches staged files "a.md" and "b.md"
    When "rhino-cli gate run --surface=pre-commit --only=md-naming" runs
    Then the local rhino-cli leaf receives only "a.md" and "b.md"

  Scenario: External kind preserves fixed argv before files
    Given an external gate declares fixed arguments and matches a shell file
    When the selected gate runs
    Then its fixed arguments precede its derived files

  Scenario: CI affected-file-type gates use the supplied event base
    Given a CI event supplies its preceding commit as the changed base
    When an affected-file-type CI gate runs after main advances
    Then the gate receives the files changed from the supplied base

  Scenario: Affected-file-type gates exclude deleted paths on both CI and pre-commit surfaces
    Given a changed-path set contains a deleted file alongside a modified file
    When an affected-file-type gate resolves its candidate files
    Then the deleted file is excluded because it no longer exists on disk
    And the modified file is still passed to the gate command

  Scenario: Path-gated gates still fire when a trigger path is only deleted
    Given a path-gated gate's trigger directory contains only a deleted file
    When the path-gated gate evaluates its trigger
    Then the gate still runs because trigger matching is unaffected by on-disk existence

  Scenario: External kind resolves a repository-local binary
    Given an external gate command exists only in the repository node_modules bin directory
    When its repository-local external gate runs
    Then the repository-local external gate succeeds

  Scenario: Nx kind delegates the affected project graph
    Given an nx gate declares scope "affected-projects"
    When the selected gate runs
    Then npm invokes the affected project graph target

  Scenario: All supported scopes derive their specified inputs
    Given one registry fixture covers every declared scope
    When each selected gate runs
    Then each leaf receives its declared input contract

  Scenario: Glob lists and excludes are applied before invocation
    Given a file gate declares globs and excluded paths
    When its candidate set contains matching and excluded paths
    Then the leaf receives only matching non-excluded repository-relative paths

  Scenario: A registered Rhino CLI gate forwards and enforces configured exclusions
    Given the frontmatter-date gate declares an excluded violating website path
    When its CI gate runs by id
    Then the frontmatter-date gate suppresses the excluded finding

  Scenario: An empty scoped match is a successful skip
    Given a file-scoped gate has no eligible paths
    When that gate runs
    Then it succeeds without invoking its leaf and reports the skip

  Scenario: Only executes exactly one direct leaf
    Given pre-commit declares batch entries and a direct mutation
    When a valid --only selector runs
    Then only the selected leaf runs directly

  Scenario: Unknown or duplicate only ids fail before execution
    Given an --only selector is absent or duplicated
    When gate run executes
    Then it fails before any leaf invocation

  Scenario: An unknown group id fails before execution
    Given a --group selector names a CI group id absent from the registry
    When "rhino-cli gate run --surface=ci --group=<id>" runs
    Then it fails before any leaf invocation and names the unknown group id

  Scenario: A re-staging mutation stages only its outputs
    Given a successful restaging mutation changes generated output
    When it runs with unrelated worktree edits
    Then only the mutation output is staged

  Scenario: A failed mutation never re-stages output
    Given a restaging mutation changes output then fails
    When it runs
    Then it returns non-zero without staging that output

  Scenario: Two consecutive re-staging mutations each attribute only their own output
    Given two successful restaging mutations each change a distinct output file
    When they run back to back
    Then each mutation's own output is staged and neither is attributed to the other

  Scenario: A second re-staging mutation that re-touches the first mutation's output is still staged
    Given two successful restaging mutations, the second of which also re-touches the first mutation's output file
    When they run back to back
    Then the second mutation's re-touch of that shared file is staged, not silently dropped by the threaded snapshot

  Scenario: Pre-commit has one declaration-positioned batch
    Given pre-commit contains eligible file gates and direct mutations
    When gate run executes
    Then one lint-staged batch runs at its declaration position

  Scenario: A restaging gate after the lint-staged batch never re-stages the batch's own leftover mutation
    Given a restaging mutation, then a batch-eligible entry that leaves its file modified, then another restaging mutation
    When they run in that order
    Then the second restaging gate stages only its own output and leaves the batch's leftover mutation unstaged

  Scenario: gofmt is wrapped because it cannot fail on its own
    Given a tracked ".go" file is not formatted
    When the gate with id "format-verify-gofmt" runs
    Then it exits non-zero
    And the wrapper treats non-empty "gofmt -l" output as failure

  Scenario: The Elixir formatter script gains a check mode that fails
    Given a tracked ".ex" file is not formatted
    When the gate with id "format-verify-elixir" runs
    Then it exits non-zero
    And no tracked file is rewritten

  Scenario: The Elixir check mode passes on formatted sources
    Given every tracked ".ex" and ".exs" file is formatted
    When the gate with id "format-verify-elixir" runs
    Then it exits zero
    And no tracked file is rewritten

  Scenario: A failing gate inside a group is named in the output
    Given a CI group containing several gates where exactly one fails
    When "rhino-cli gate run --surface=ci --group=<id>" runs
    Then it exits non-zero
    And its output contains a per-gate summary line for every gate in the group
    And the failing gate id appears on a line marked FAIL

  Scenario: A hand-wired gate never runs a second time inside its CI group
    Given a CI group contains both an auto-dispatched gate and a hand-wired gate
    When "rhino-cli gate run --surface=ci --group=<id>" runs
    Then only the auto-dispatched gate executes
    And the hand-wired gate is absent from the group's summary

  Scenario: Gate group jobs consume a prebuilt binary
    Given the build-rhino job has published the rhino-cli artifact for the run
    When a gate group job executes
    Then it downloads the artifact rather than building from source
    And it runs no cargo install command
    And its step list contains no Rust toolchain setup

  Scenario: A gate group with no node tooling skips npm ci
    Given a CI gate group whose gates require no node-resolved tool
    When that group's job executes
    Then its step list contains no npm ci invocation
    And every gate in the group still reports its baseline result

  Scenario: An unnamed npm ci action step is detected
    Given a composite action with an unnamed unguarded npm ci step
    When its npm ci steps are inspected
    Then the unnamed npm ci step is reported unguarded
