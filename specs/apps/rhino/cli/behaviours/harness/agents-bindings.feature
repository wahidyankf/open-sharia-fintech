Feature: Generated Harness Binding Files

  As a repository maintainer
  I want to generate and guard the binding files of every generated-tier harness
  So that each supported harness follows the canonical AGENTS.md instructions without drifting

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
  Rule: harness bindings validate enforces mirror parity and catalog coverage

    Scenario: A repository matching the generator passes validation
      Given a repository whose generated binding files match the generated content
      And the platform-bindings catalog references every present binding directory
      When the developer runs harness bindings validate
      Then the command exits successfully
      And the output reports all binding checks as passing

    Scenario: A present binding directory absent from the catalog fails validation
      Given a repository with a known binding directory that the platform-bindings catalog does not reference
      When the developer runs harness bindings validate
      Then the command exits with a failure code
      And the output identifies the binding directory missing a catalog row

    Scenario: Absent binding directories require no catalog row
      Given a repository where some known binding directories do not exist on disk
      When the developer runs harness bindings validate
      Then the command exits successfully
      And no catalog row is required for the absent binding directories

  @codex-agents-extension
  Rule: .codex/agents/ accepts standalone .toml agent files and rejects .md ones

    Scenario: A .codex/agents directory holding only .toml files passes validation
      Given a repository whose .codex/agents directory holds a standalone .toml agent file
      When the developer runs harness bindings validate
      Then the command exits successfully

    Scenario: A .md file under .codex/agents fails validation
      Given a repository whose .codex/agents directory holds a .md agent file
      When the developer runs harness bindings validate
      Then the command exits with a failure code
      And the output names .toml as the officially-correct extension

  @mirror-orphans
  Rule: a generated agent mirror whose source agent no longer exists fails validation

    Scenario: A mirror whose source agent was renamed away fails validation
      Given a repository whose generated agent directory holds a mirror with no source agent
      When the developer runs harness bindings validate
      Then the command exits with a failure code
      And the output names the orphaned mirror and the source that no longer exists

    Scenario: A generated agent directory whose mirrors all have sources passes validation
      Given a repository whose generated agent mirrors each have a source agent
      When the developer runs harness bindings validate
      Then the command exits successfully

    Scenario: A mirror the registry declares vendored is exempt from the orphan check
      Given a repository whose generated agent directory holds a vendored mirror with no source agent
      When the developer runs harness bindings validate
      Then the command exits successfully
