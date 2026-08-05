@gate @unit
Feature: Gate execution

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

  Scenario: A re-staging mutation stages only its outputs
    Given a successful restaging mutation changes generated output
    When it runs with unrelated worktree edits
    Then only the mutation output is staged

  Scenario: A failed mutation never re-stages output
    Given a restaging mutation changes output then fails
    When it runs
    Then it returns non-zero without staging that output

  Scenario: Pre-commit has one declaration-positioned batch
    Given pre-commit contains eligible file gates and direct mutations
    When gate run executes
    Then one lint-staged batch runs at its declaration position

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
