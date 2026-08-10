Feature: Verified restore
  Scenario: Verified restore returns the application to ready state
    Given a validated backup and the application is stopped
    When I run the restore command against the configured durable directory
    Then the replaced database is preserved at a recoverable path
    And the restored migration journal is current
    And the restarted application reports ready

  Scenario: Restore rolls back to the preserved database when the final promote fails
    Given a validated backup and the application is stopped
    And the final promote of the staged database will fail
    When I run the restore command against the configured durable directory
    Then the pre-restore database is restored at the live path
    And the command reports that the restore failed

  Scenario: Restore reports a distinguishable error when the rollback also fails
    Given a validated backup and the application is stopped
    And the final promote of the staged database will fail
    And the rollback to the preserved database will also fail
    When I run the restore command against the configured durable directory
    Then the command reports that the restore failed and the rollback failed
    And the command instructs the operator to recover the live database manually
