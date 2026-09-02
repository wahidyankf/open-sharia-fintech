Feature: OrganicLever marketing home page

  The public marketing site (organiclever-www) renders the OrganicLever
  landing experience at the domain root, carried over from the former
  organiclever-app-web landing context.

  Background:
    Given I navigate to the marketing home page

  @unit @e2e
  Scenario: Hero heading visible
    Then I see text "Your life,"
    And I see text "tracked."
    And I see text "Analyzed."

  @unit @e2e
  Scenario: Primary call-to-action button present
    Then I see a button "Open the app"

  @unit @e2e
  Scenario: Footer link present
    Then I see text "Open app →"

  @unit @e2e
  Scenario: Pre-Alpha badge visible in nav
    Then I see text "Pre-Alpha"

  @unit @e2e
  Scenario: Alpha warning banner visible
    Then I see text "Pre-Alpha — expect bugs, rough edges, and breaking changes"

  @unit @e2e
  Scenario: All five event type cards visible
    Then I see text "Workouts"
    And I see text "Reading"
    And I see text "Learning"
    And I see text "Meals"
    And I see text "Focus"

  @unit @e2e
  Scenario: Custom event card visible
    Then I see text "Plus your own."

  @unit @e2e
  Scenario: Weekly rhythm demo visible
    Then I see text "Last 7 days"

  @unit @e2e
  Scenario: All six principles visible
    Then I see text "Local-first"
    And I see text "Yours to take"
    And I see text "Flexible"
    And I see text "Quiet"
    And I see text "Open"
    And I see text "Multilingual"
