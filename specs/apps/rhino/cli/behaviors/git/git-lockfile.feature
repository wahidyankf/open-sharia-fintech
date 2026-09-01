Feature: Lockfile synchronization

  As a developer
  I want staged app lockfiles kept in sync with their package manifests
  So that a stale lockfile never reaches a commit

  Scenario: A staged package manifest with a stale lockfile is regenerated and staged
    Given a staged app package.json whose version disagrees with its package-lock.json
    When the developer runs "git lockfile sync"
    Then the command regenerates the app's package-lock.json to match the manifest
    And the regenerated package-lock.json is staged

  Scenario: A staged package manifest whose lockfile is already current is left untouched
    Given a staged app package.json whose fields already agree with its package-lock.json
    When the developer runs "git lockfile sync"
    Then the command exits successfully
    And the output reports no lockfile was synced
    And the package-lock.json file is not modified

  Scenario: No staged app package.json means no lockfile work
    Given no app package.json file is staged
    When the developer runs "git lockfile sync"
    Then the command exits successfully
    And the output is empty
    And the staged file set is unchanged
