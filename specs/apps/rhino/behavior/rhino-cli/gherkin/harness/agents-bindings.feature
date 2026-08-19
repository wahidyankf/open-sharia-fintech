Feature: Amazon Q Developer Binding Bridge

  As a repository maintainer
  I want to generate and guard the Amazon Q Developer binding bridge
  So that Amazon Q follows the canonical AGENTS.md instructions without the bridge drifting

  @agents-emit-bindings
  Rule: agents emit-bindings writes the Amazon Q bridge files deterministically

    Scenario: Emitting writes the rules pointer and the agent definition
      Given a repository without an existing .amazonq/ directory
      When the developer runs agents emit-bindings
      Then the command exits successfully
      And the file .amazonq/rules/00-agents-md.md is written as a pointer to AGENTS.md
      And the configured Amazon Q agent definition is written as valid JSON

    Scenario: The agent definition loads AGENTS.md and the rules directory as resources
      Given a repository without an existing .amazonq/ directory
      When the developer runs agents emit-bindings
      Then the command exits successfully
      And the agent definition resources reference file://AGENTS.md and file://.amazonq/rules/**/*.md

    Scenario: Emitting twice is idempotent
      Given a repository where the bridge files already exist
      When the developer runs agents emit-bindings
      Then the command exits successfully
      And the bridge files are byte-for-byte identical to the previous emission

  @harness-name-registry-derived
  Rule: --harness accepts exactly the names the registry declares

    Scenario: A registry-declared harness name is accepted
      Given the repo-config.yml harness registry declares codex
      When the developer runs harness bindings generate for codex
      Then the harness name is not rejected as unknown

    Scenario: A harness name absent from the registry is rejected
      Given the repo-config.yml harness registry does not declare cursor
      When the developer runs harness bindings generate for cursor
      Then the command exits with a failure code
      And the error names the registry-derived accepted set

  @agents-validate-bindings
  Rule: agents validate-bindings enforces parity and catalog coverage

    Scenario: Bridge files that match the generator pass validation
      Given a repository whose bridge files match the generated content
      And the platform-bindings catalog references every present binding directory
      When the developer runs agents validate-bindings
      Then the command exits successfully
      And the output reports all binding checks as passing

    Scenario: A mutated bridge file fails validation
      Given a repository where a bridge file has been hand-edited away from the generated content
      When the developer runs agents validate-bindings
      Then the command exits with a failure code
      And the output identifies the drifted bridge file

    Scenario: A missing bridge file fails validation
      Given a repository where a bridge file has been deleted
      When the developer runs agents validate-bindings
      Then the command exits with a failure code
      And the output reports the missing bridge file

    Scenario: A present binding directory absent from the catalog fails validation
      Given a repository with a known binding directory that the platform-bindings catalog does not reference
      When the developer runs agents validate-bindings
      Then the command exits with a failure code
      And the output identifies the binding directory missing a catalog row

    Scenario: Absent binding directories require no catalog row
      Given a repository where some known binding directories do not exist on disk
      When the developer runs agents validate-bindings
      Then the command exits successfully
      And no catalog row is required for the absent binding directories
