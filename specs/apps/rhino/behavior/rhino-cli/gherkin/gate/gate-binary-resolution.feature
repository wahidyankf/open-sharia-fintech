@gate @unit
Feature: Resolver shim binary resolution

  Scenario: A swept target directory produces a slow run, not a failure
    Given the rhino-cli binary is absent because the ambient sweeper removed target/
    When a generated gate command runs through the resolver shim
    Then the shim builds the binary and then executes the requested gate
    And the gate reports the same result it would have reported with the binary present
    And a subsequent invocation reuses the built binary without rebuilding

  Scenario: RHINO_CLI_BIN takes precedence over discovery
    Given the environment variable RHINO_CLI_BIN points at an executable rhino-cli binary
    When a generated gate command runs through the resolver shim
    Then the shim executes the binary at that path
    And it performs no cargo build

  Scenario: A stale prebuilt binary is rebuilt, not silently reused
    Given the prebuilt gate-profile binary in target/ is older than the source tree it was built from
    When a generated gate command runs through the resolver shim
    Then the shim rebuilds the binary before executing the requested gate
    And the gate reports the same result it would have reported with the binary present

  Scenario: An invalid RHINO_CLI_BIN override falls through to discovery
    Given the environment variable RHINO_CLI_BIN points at a path that does not exist
    When a generated gate command runs through the resolver shim
    Then the shim falls back to discovery instead of the invalid override
    And the gate reports the same result it would have reported with the binary present
