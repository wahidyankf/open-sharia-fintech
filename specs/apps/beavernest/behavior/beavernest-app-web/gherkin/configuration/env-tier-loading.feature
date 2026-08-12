Feature: beavernest-app-web environment tier loading

  As a platform operator
  I want beavernest-app-web to build with exactly one .env.<APP_ENV> tier file selected via Vite's
    native --mode flag
  So that agent-restricted tiers (.env.stag, .env.prod) never need to be opened by an AI agent, and a
    stray auto-loaded file can never leak into a non-local build

  @unit
  Scenario Outline: beavernest-app-web builds with the tier selected via --mode
    Given the Nx "<target>" target for beavernest-app-web
    When it runs with APP_ENV set to "<tier>"
    Then Vite is invoked with "--mode <tier>"

    Examples:
      | target    |
      | dev       |
      | build     |
      | test:unit |

  @unit
  Scenario: beavernest-app-web process env wins at the local tier
    Given a VITE_-prefixed variable already exported in the process
    When beavernest-app-web starts at mode "local"
    Then the exported process value is used
    And no .env.local value overrides it

  @unit
  Scenario Outline: beavernest-app-web guards against a stray auto-loaded env file
    Given a stray "<file>" exists beside beavernest-app-web's tier file
    When beavernest-app-web starts at a non-local mode
    Then the guard throws before the build proceeds

    Examples:
      | file       |
      | .env       |
      | .env.local |
