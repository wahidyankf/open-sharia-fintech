@binding-ownership
Feature: Total ownership of binding files

  As the maintainer of a repository whose binding trees are mostly generated
  I want every tracked file under every binding directory to carry exactly one declared class
  So that nothing can sit in a binding directory unowned and unnoticed the way .opencode/skills/ did

  The schema half of US-8 — that there is no fourth class and that a vendored
  declaration cannot omit its reason — is covered by the repo-config-validate
  feature, because those assertions exercise "rhino-cli repo-config validate"
  rather than the ownership validator.

  Scenario: An unclassified file under a binding directory fails the validator
    Given a fixture repository whose binding files are all declared generated, vendored, or source
    When a tracked file with no declared class is introduced under a binding directory
    Then rhino-cli harness ownership validate exits non-zero naming that exact file as unclassified
    And it exits 0 once the file is removed, proving the check is falsifiable in both directions rather than always-green

  Scenario: A generated file must reproduce byte-for-byte
    Given a fixture repository whose mirror trees are declared generated
    When one emitted file is hand-edited
    Then rhino-cli harness ownership validate exits non-zero naming the drifted generated file
    And it exits 0 after regeneration restores the canonical bytes

  Scenario: A vendored file carries no byte guard
    Given a fixture repository declaring one vendored skill directory with a recorded reason
    When the vendored file is hand-edited
    Then rhino-cli harness ownership validate still exits 0, because a vendored path has no in-repo source to compare against
    And the vendored file is still present, so nothing deleted it in passing

  Scenario: A source path is never written by the emitter
    Given a fixture repository declaring the .claude tree as source
    When rhino-cli harness bindings generate runs
    Then every declared source path is byte-identical to what it was before the run
    And a registry declaring an emitter output directory as source makes the generator refuse rather than silently succeed

  Scenario: Every tracked binding file in this repository carries exactly one class
    Given this repository's registry declares an ownership class for every binding path
    When rhino-cli harness ownership validate runs against it
    Then it exits 0
    And it reports a per-class count that sums to the total tracked binding-file count
