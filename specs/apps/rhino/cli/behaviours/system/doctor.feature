@doctor
Feature: Development Environment Health Check

  As a developer
  I want to verify that my local environment has all required tools installed
  So that development and build tasks run reliably

  Scenario: All required tools are installed and versions match
    Given all required development tools are present with matching versions
    When the developer runs the doctor command
    Then the command exits successfully
    And the output reports each tool as passing

  Scenario: A required tool is missing from the environment
    Given a required development tool is not found in the system PATH
    When the developer runs the doctor command
    Then the command exits with a failure code
    And the output identifies the missing tool

  Scenario: A tool is installed but its version does not match the requirement
    Given a required development tool is installed with a non-matching version
    When the developer runs the doctor command
    Then the command exits successfully
    And the output reports the tool as a warning rather than a failure

  Scenario: JSON output lists all tool check results
    Given all required development tools are present with matching versions
    When the developer runs the doctor command with JSON output
    Then the command exits successfully
    And the output is valid JSON
    And the JSON lists every checked tool with its status

  Scenario: Minimal scope checks only core tools
    Given all required development tools are present with matching versions
    When the developer runs the doctor command with minimal scope
    Then the command exits successfully
    And the output checks only the minimal tool set

  Scenario: Full scope is the default behaviour
    Given all required development tools are present with matching versions
    When the developer runs the doctor command
    Then the command exits successfully
    And the output reports each tool as passing

  Scenario: An explicit tool selection probes and reports only that tool
    Given all required development tools are present with matching versions
    And the unselected shellcheck tool is not found in the system PATH
    And only the tofu tool is selected
    When the developer runs the doctor command
    Then the command exits successfully
    And the output reports only the selected tofu tool

  Scenario: A selected missing tool has only its remediation previewed
    Given the tofu tool is not found in the system PATH
    And only the tofu tool is selected
    When the developer runs the doctor command with fix and dry-run flags
    Then the command exits with a failure code
    And the selected tofu dry run previews only its remediation

  Scenario: An unknown selected tool is rejected before environment checks
    Given an unknown Doctor tool is selected
    When the developer runs the doctor command
    Then the command exits with a failure code
    And the invalid selection is rejected before any tool is probed

  # Exemption(e2e): installing a host tool crosses privileged third-party package-manager and network boundaries; alternative-proof: rhino-cli:test:integration / Fix installs missing tools
  @e2e-exempt
  Scenario: Fix installs missing tools
    Given a required development tool is not found in the system PATH
    When the developer runs the doctor command with the fix flag
    Then the output contains fix progress

  Scenario: Fix with dry-run previews without executing
    Given a required development tool is not found in the system PATH
    When the developer runs the doctor command with fix and dry-run flags
    Then the command exits with a failure code
    And the output contains a dry-run preview

  Scenario: Fix dry-run previews a verified, platform-safe OpenTofu release archive
    Given the tofu tool is not found in the system PATH
    When the developer runs the doctor command with fix and dry-run flags
    Then the command exits with a failure code
    And the output handles verified OpenTofu remediation safely

  Scenario: Fix reports nothing to fix when all tools are present
    Given all required development tools are present with matching versions
    When the developer runs the doctor command with the fix flag
    Then the command exits successfully
    And the output reports nothing to fix

  Scenario: A repo-config-declared tool is skipped from the check
    Given a tool is listed under the doctor skip-tools section of repo-config.yml
    When the developer runs the doctor command
    Then the command exits successfully
    And the output does not include the skipped tool

  Scenario: A repo-config-declared extra tool is probed like a built-in tool
    Given a tool is listed under the doctor extra-tools section of repo-config.yml
    When the developer runs the doctor command
    Then the command exits successfully
    And the output includes the configured extra tool

  Scenario: A tool absent from both the built-in and configured inventories is rejected
    Given an unknown Doctor tool is selected
    When the developer runs the doctor command
    Then the command exits with a failure code
    And the invalid selection is rejected before any tool is probed

  Scenario: A pinned Rust toolchain without lint components is reported as a warning
    Given a rust-toolchain.toml pins a channel and declares no lint components
    When "npm run doctor" runs
    Then the command exits successfully
    And it reports the toolchain component check as a warning naming rustfmt and clippy

  Scenario: A pinned Rust toolchain declaring only one lint component names just the missing one
    Given a rust-toolchain.toml declares only the clippy lint component
    When "npm run doctor" runs
    Then the command exits successfully
    And it reports the toolchain component check as a warning naming only rustfmt
