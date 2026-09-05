Feature: ose-be environment tier loading

  As a platform operator
  I want ose-be to load exactly one .env.<APP_ENV> tier file at startup
  So that agent-restricted tiers (.env.stag, .env.prod) never need to be opened by an AI
    agent, while process environment variables set by CI always take precedence over any
    file value

  # Exemption(e2e): exact file-selection reads are not observable through the service's public HTTP boundary; alternative-proof: ose-be:test:integration / ose-be loads exactly one tier file
  @e2e-exempt
  Scenario Outline: ose-be loads exactly one tier file
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

  # Exemption(e2e): environment-source precedence is not observable through the service's public HTTP boundary; alternative-proof: ose-be:test:integration / ose-be process env wins over a tier file value
  @e2e-exempt
  Scenario: ose-be process env wins over a tier file value
    Given a tier file at the app's composition root sets a variable to a file value
    When the process starts with that variable already set in the process environment
    Then the process environment value is used
    And the tier file value is not applied over it

  # Exemption(e2e): missing-file tolerance is a local startup-input concern with no distinct HTTP observation; alternative-proof: ose-be:test:integration / ose-be tolerates a missing tier file
  @e2e-exempt
  Scenario: ose-be tolerates a missing tier file
    Given no tier file exists at the app's composition root for the selected tier
    When the process starts with APP_ENV set to that tier
    Then startup does not throw
    And configuration proceeds using whatever the process environment already supplies
