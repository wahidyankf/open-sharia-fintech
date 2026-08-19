Feature: Generated Harness Binding Files

  As a repository maintainer
  I want to generate and guard the binding files of every generated-tier harness
  So that each supported harness follows the canonical AGENTS.md instructions without drifting

  @harness-purge
  Rule: dropped-harness binding directories leave nothing behind

    Scenario: Generated binding directories for dropped harnesses no longer exist
      Given .cursor/ tracked 93 files, .amazonq/ tracked 2 files, and .pi/ tracked 1 file before the purge
      When git ls-files is run against those three paths after the purge
      Then each returns zero tracked files
      And harness bindings validate exits successfully, where before the purge it required .amazonq/ byte-parity

  @binding-surface-set
  Rule: the known binding surfaces are exactly the three supported harnesses need

    Scenario: Only surviving harness surfaces are known
      Given the compiled set of known binding directories
      When the set is inspected
      Then it contains exactly .claude, .opencode, .codex, .agents, and .github
      And it names no dropped harness surface

    Scenario: No dropped-harness binding file is expected any more
      Given the compiled set of known binding directories
      When the expected binding files are computed
      Then no expected file lives under a dropped harness surface

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
