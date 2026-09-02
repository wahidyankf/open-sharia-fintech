Feature: History Screen

  As an app user
  I want to view my past journal entries in reverse chronological order
  So that I can review my recent activity at a glance

  @unit @e2e
  Scenario: History shows entries in reverse order
    Given the history screen has entries
    Then entries are shown newest first

  @unit @e2e
  Scenario: Empty history shows empty state
    Given the history screen has no entries
    Then the empty state message is shown

  @unit @e2e
  Scenario: Session card expands on click
    Given the history screen shows a workout entry
    When the user taps the session card
    Then the card expands showing details
