@gate @unit
Feature: Generated lint-staged block

  Scenario: The emitter reproduces the registry's per-file entries
    Given the registry declares per-file gates on surface "pre-commit"
    When "rhino-cli gate emit --surface=pre-commit" runs
    Then the "lint-staged" block in package.json contains one glob key per declared glob in registry declaration order
    And each key lists that glob's commands in declaration order

  Scenario: Re-running the emitter is idempotent
    Given "rhino-cli gate emit --surface=pre-commit" has already run
    When it runs a second time
    Then package.json is byte-identical to the first result
    And the block appears exactly once

  Scenario: Generated lint-staged commands may use a declared shell wrapper
    Given a pre-commit gate declares an affected-file-type glob and a lint-staged shell template
    When "rhino-cli gate emit --surface=pre-commit" runs
    Then the generated lint-staged command uses the declared wrapper
    And a {{command}} placeholder expands to the gate's kind-derived command exactly once

  Scenario: Rhino CLI kind renders a resolver shim invocation
    Given the registry declares a gate of kind "rhino-cli" on surface "pre-commit"
    When "rhino-cli gate emit --surface=pre-commit" runs
    Then the generated command invokes the resolver shim at "apps/rhino-cli/scripts/rhino-bin.sh"
    And the generated command contains no "cargo run" substring

  Scenario: Node-resolved external tools render a repository-local bin path
    Given the registry declares an external gate whose tool resolves from node_modules
    When "rhino-cli gate emit --surface=pre-commit" runs
    Then the generated command invokes that tool through "node_modules/.bin"
    And the generated command contains no "npx" substring
