Feature: Verified restore
  Scenario: Verified restore returns the application to ready state
    Given a validated backup and the application is stopped
    When I run the restore command against the configured durable directory
    Then the replaced database is preserved at a recoverable path
    And the restored migration journal is current
    And the restarted application reports ready
