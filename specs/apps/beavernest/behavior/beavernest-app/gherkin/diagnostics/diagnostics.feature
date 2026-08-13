Feature: Safe workspace diagnostics
  The workspace shows only contract-declared operational information.

  Scenario: A ready diagnostics response is rendered safely
    Given the diagnostics endpoint reports a ready workspace
    When I open Workspace diagnostics
    Then I can read the version, uptime and server time
    And I cannot read an unavailable cause or connection detail
    And I can retry diagnostics to request a fresh safe snapshot
