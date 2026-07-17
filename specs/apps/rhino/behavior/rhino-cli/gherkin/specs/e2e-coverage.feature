@specs-e2e-coverage
Feature: specs e2e-coverage validate

  As a developer relying on playwright-bdd's missingSteps: "skip-scenario" setting
  I want rhino-cli specs e2e-coverage validate to detect Gherkin scenarios that
  silently lose E2E coverage via test.fixme, gated against a checked-in baseline
  So that new unbound scenarios fail the gate while pre-existing ones do not

  @unit
  Scenario: A project's current unbound gaps exactly match its checked-in baseline
    Given a playwright-bdd project whose generated output marks scenarios "A" and "B" as test.fixme
    And a baseline manifest that lists exactly scenarios "A" and "B" as allowed unbound
    When rhino-cli specs e2e-coverage validate runs for that project
    Then it passes with exit code 0
    And it reports 2 declared-but-unbound scenarios all covered by the baseline

  @unit
  Scenario: A newly added @e2e scenario ships without a step definition
    Given a baseline manifest that lists exactly scenario "A" as allowed unbound
    And generated output that marks scenarios "A" and "C" as test.fixme
    When rhino-cli specs e2e-coverage validate runs for that project
    Then it fails with a non-zero exit code
    And it names scenario "C" and its containing .feature file as a new unbound gap
    And it does not report scenario "A" as a new gap

  @unit
  Scenario: A previously-unbound scenario is now bound
    Given a baseline manifest that lists scenarios "A" and "B" as allowed unbound
    And generated output that marks only scenario "A" as test.fixme
    When rhino-cli specs e2e-coverage validate runs for that project
    Then it passes with exit code 0
    And it reports scenario "B" as newly bound relative to the baseline

  @unit
  Scenario: The baseline lists a scenario that is no longer unbound
    Given a baseline manifest that lists scenarios "A" and "B" as allowed unbound
    And generated output that marks only scenario "A" as test.fixme
    When rhino-cli specs e2e-coverage validate runs for that project
    Then it passes with exit code 0
    And it reports scenario "B" as a stale baseline entry that can be pruned

  @unit
  Scenario: A test.fixme scenario that is not @e2e-tagged is ignored
    Given a scenario tagged @unit only that appears as test.fixme in the generated output
    And a baseline manifest that lists no allowed unbound scenarios
    When rhino-cli specs e2e-coverage validate runs for that project
    Then it passes with exit code 0
    And it does not report the @unit-only scenario as an unbound gap

  @unit
  Scenario: Output identifies each new gap by feature path and scenario title
    Given a new unbound scenario "Resize the sidebar by keyboard" in "resizable-panel.feature"
    When rhino-cli specs e2e-coverage validate runs and detects it as a new gap
    Then the failure output contains the scenario title "Resize the sidebar by keyboard"
    And the failure output contains the feature file path ending in "resizable-panel.feature"
    And the failure output states the delta is an increase of 1 over baseline

  @unit
  Scenario: First-time baseline generation snapshots current unbound scenarios
    Given a project with no baseline manifest yet
    And generated output that marks scenarios "A" and "B" as test.fixme
    When rhino-cli specs e2e-coverage validate runs with the --update-baseline flag
    Then it writes a baseline manifest listing scenarios "A" and "B" as allowed unbound
    And a subsequent validate run for that project passes with exit code 0

  @unit
  Scenario: The generated output directory is absent
    Given a project whose .features-gen directory does not exist
    When rhino-cli specs e2e-coverage validate runs for that project
    Then it fails with a non-zero exit code
    And it reports that bddgen output was not found and must be generated first
