Feature: organiclever-be tiered env-file loading

  As a platform operator
  I want organiclever-be to load exactly one .env.<tier> file selected by APP_ENV
  So that agent-restricted .env.stag/.env.prod files never need to be opened by an AI agent

  @unit
  Scenario Outline: organiclever-be loads exactly one tier file
    Given the files ".env.local" and ".env.stag" both exist at the app's composition root
    When the process starts with APP_ENV set to "<tier>"
    Then configuration values are read from ".env.<tier>"
    And no value is read from any other env file

    Examples:
      | tier  |
      | local |
      | test  |
      | stag  |
      | prod  |

  @unit
  Scenario: organiclever-be process env wins over a tier file value
    Given a tier file at the app's composition root sets a variable to a file value
    When the process starts with that variable already set in the process environment
    Then the process environment value is used
    And the tier file value is not applied over it

  @unit
  Scenario: organiclever-be tolerates a missing tier file
    Given no tier file exists at the app's composition root for the selected tier
    When the process starts with APP_ENV set to that tier
    Then startup does not throw
    And configuration proceeds using whatever the process environment already supplies
