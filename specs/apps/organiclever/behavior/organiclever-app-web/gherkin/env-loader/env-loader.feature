Feature: APP_ENV tier env-file loading

  As a developer running organiclever-app-web across local, staging, and production tiers
  I want the app to load exactly one .env.<tier> file selected by APP_ENV
  So that .env.stag and .env.prod stay agent-restricted while builds still resolve correct config

  @unit
  Scenario: organiclever-app-web builds against the staging tier
    Given only ".env.stag" exists in the app directory
    When "next build" runs with APP_ENV set to "stag"
    Then every variable consumed by the build resolves to its ".env.stag" value

  @unit
  Scenario: organiclever-app-web process env wins over the local tier file
    Given ".env.local" sets an app variable to a file value
    When the process starts with that variable already exported at tier "local"
    Then the exported process value is used
    And the ".env.local" value is not applied over it

  @unit
  Scenario: organiclever-app-web tolerates a missing tier file
    Given no ".env.stag" file exists in the app directory
    When the loader runs with APP_ENV set to "stag"
    Then the loader does not throw
    And startup proceeds using whatever the process environment already supplies

  @unit
  Scenario Outline: organiclever-app-web fails loudly on a stray auto-loaded env file
    Given a stray "<file>" sits beside the app's tier file
    When the loader runs with APP_ENV set to a non-local tier
    Then the loader throws, naming "<file>" and the correct ".env.<tier>" replacement

    Examples:
      | file            |
      | .env            |
      | .env.production |
      | .env.local      |
