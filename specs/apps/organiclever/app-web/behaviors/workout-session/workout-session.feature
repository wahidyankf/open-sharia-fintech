Feature: Workout Session

  As an app user
  I want to start, log sets, and complete a workout session
  So that my exercise activity is recorded in the journal

  @unit @e2e
  Scenario: Start a blank workout
    Given the workout screen is open with no routine
    When the user starts the workout
    Then the workout is in active exercising state

  @unit @e2e
  Scenario: Log a set triggers rest timer
    Given an active workout with one exercise with rest
    When the user logs a set
    Then the rest timer is visible

  @unit @e2e
  Scenario: Skip rest returns to exercising
    Given the rest timer is active
    When the user skips rest
    Then the workout returns to exercising state

  @unit @e2e
  Scenario: End workout shows confirmation sheet
    Given an active workout
    When the user ends the workout
    Then the confirmation sheet is shown

  @unit @e2e
  Scenario: Discard workout returns to idle
    Given the confirmation sheet is shown
    When the user discards the workout
    Then the workout is in idle state

  @unit @e2e
  Scenario: Keep going continues exercising
    Given the confirmation sheet is shown
    When the user keeps going
    Then the workout returns to exercising state
