@repo-config-validate
Feature: Schema-parity gate for repo-config.yml

  As a maintainer keeping rhino-cli byte-identical across ose-public and ose-private
  I want a "repo-config validate" command that strict-deserializes repo-config.yml
  So that both repo-config.yml files are guaranteed to carry an identical key set

  Scenario: A schema-parity gate enforces the identical key set
    Given "rhino-cli repo-config validate" in each repo's pre-commit and pre-push/PR
    When repo-config.yml is validated
    Then the command strict-deserializes it against the canonical RepoConfig schema
    And it passes when only values differ
    And it fails when a required key is missing or an unknown key is present
    And running it independently against the byte-identical schema in both repos is equivalent to an identical key set across both repo-config.yml files
