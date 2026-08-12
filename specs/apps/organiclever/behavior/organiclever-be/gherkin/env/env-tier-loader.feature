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
