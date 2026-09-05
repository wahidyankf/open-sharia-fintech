Feature: APP_ENV tier env-file loading

  As a developer running organiclever-www across local, staging, and production tiers
  I want the app to load exactly one .env.<tier> file selected by APP_ENV
  So that .env.stag and .env.prod stay agent-restricted while builds still resolve correct config

  # Exemption(e2e): the public browser boundary starts only after the app has consumed its private app-directory environment layout; alternative-proof: organiclever-www:test:unit / organiclever-www bootstrap selects the staging tier file
  @e2e-exempt
  Scenario: organiclever-www bootstrap selects the staging tier file
    Given only ".env.stag" exists in the app directory
    When the organiclever-www environment bootstrap runs with APP_ENV set to "stag"
    Then only the ".env.stag" values are loaded into the app process

  # Exemption(e2e): the public browser boundary cannot inject or distinguish private process-environment precedence before startup; alternative-proof: organiclever-www:test:unit / organiclever-www process env wins over the local tier file
  @e2e-exempt
  Scenario: organiclever-www process env wins over the local tier file
    Given ".env.local" sets an app variable to a file value
    When the process starts with that variable already exported at tier "local"
    Then the exported process value is used
    And the ".env.local" value is not applied over it

  # Exemption(e2e): the public browser boundary cannot remove a private app-directory tier file before the server process starts; alternative-proof: organiclever-www:test:unit / organiclever-www tolerates a missing tier file
  @e2e-exempt
  Scenario: organiclever-www tolerates a missing tier file
    Given no ".env.stag" file exists in the app directory
    When the loader runs with APP_ENV set to "stag"
    Then the loader does not throw
    And startup proceeds using whatever the process environment already supplies

  # Exemption(e2e): the public browser boundary cannot inject a stray private app-directory env file into the pre-start loader; alternative-proof: organiclever-www:test:unit / organiclever-www fails loudly on a stray auto-loaded env file
  @e2e-exempt
  Scenario Outline: organiclever-www fails loudly on a stray auto-loaded env file
    Given a stray "<file>" sits beside the app's tier file
    When the loader runs with APP_ENV set to a non-local tier
    Then the loader throws, naming "<file>" and the correct ".env.<tier>" replacement

    Examples:
      | file            |
      | .env            |
      | .env.production |
      | .env.local      |
