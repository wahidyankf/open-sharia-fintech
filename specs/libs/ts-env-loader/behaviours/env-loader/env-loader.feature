Feature: APP_ENV tier env-file loading
  As a developer setting up an app's composition root
  I want a single shared loader to apply exactly the current tier's env file
  So that every app enforces the same APP_ENV tier-loading contract without duplicating the logic

  # Exemption(e2e): the public next-with-port process boundary does not invoke the library's tier-file loader; alternative-proof: ts-env-loader:test:integration / Loads the selected tier's file
  @e2e-exempt
  Scenario: Loads the selected tier's file
    Given only ".env.stag" exists in the app directory
    When the loader runs with APP_ENV set to "stag"
    Then every variable defined in ".env.stag" is applied

  # Exemption(e2e): the public next-with-port process boundary does not invoke the library's tier-file loader; alternative-proof: ts-env-loader:test:integration / Process env always wins over the tier file
  @e2e-exempt
  Scenario: Process env always wins over the tier file
    Given ".env.local" sets a variable to a file value
    When the process already has that variable set at tier "local"
    Then the process value is used
    And the ".env.local" value is not applied over it

  # Exemption(e2e): the public next-with-port process boundary does not invoke the library's tier-file loader; alternative-proof: ts-env-loader:test:integration / Tolerates a missing tier file
  @e2e-exempt
  Scenario: Tolerates a missing tier file
    Given no ".env.stag" file exists in the app directory
    When the loader runs with APP_ENV set to "stag"
    Then the loader does not throw
    And the process environment is left otherwise untouched

  # Exemption(e2e): the public next-with-port process boundary does not invoke the library's tier-file loader; alternative-proof: ts-env-loader:test:integration / Fails loudly on a stray auto-loaded env file
  @e2e-exempt
  Scenario Outline: Fails loudly on a stray auto-loaded env file
    Given a stray "<file>" sits beside the tier file
    When the loader runs with APP_ENV set to a non-local tier
    Then the loader throws, naming "<file>" and the correct ".env.<tier>" replacement

    Examples:
      | file            |
      | .env            |
      | .env.production |
      | .env.local      |

  # Exemption(e2e): the public next-with-port process boundary does not invoke the library's tier-file loader; alternative-proof: ts-env-loader:test:integration / Tolerates a stray file at the local tier
  @e2e-exempt
  Scenario: Tolerates a stray file at the local tier
    Given a stray ".env" sits beside ".env.local"
    When the loader runs with APP_ENV set to "local"
    Then the loader does not throw
