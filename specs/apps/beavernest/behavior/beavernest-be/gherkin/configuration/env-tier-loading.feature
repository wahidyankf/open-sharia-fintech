Feature: beavernest-be environment tier loading

  As a platform operator
  I want beavernest-be to load exactly one .env.<APP_ENV> tier file at startup
  So that agent-restricted tiers (.env.stag, .env.prod) never need to be opened by an AI
    agent, while process environment variables set by CI always take precedence over any
    file value

  @unit
  Scenario Outline: beavernest-be loads exactly one tier file
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
