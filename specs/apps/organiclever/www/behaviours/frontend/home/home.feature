Feature: OrganicLever marketing home page

  The public marketing site (organiclever-www) renders the OrganicLever
  landing experience at the domain root, carried over from the former
  organiclever-app-web landing context.

  Scenario: Hero heading visible
    When I navigate to the marketing home page
    Then I see text "Your life,"
    And I see text "tracked."
    And I see text "Analyzed."

  Scenario: Primary call-to-action button present
    When I navigate to the marketing home page
    Then I see a button "Open the app"

  Scenario: Footer link present
    When I navigate to the marketing home page
    Then I see text "Open app →"

  Scenario: Pre-Alpha badge visible in nav
    When I navigate to the marketing home page
    Then I see text "Pre-Alpha"

  Scenario: Alpha warning banner visible
    When I navigate to the marketing home page
    Then I see text "Pre-Alpha — expect bugs, rough edges, and breaking changes"

  Scenario: All five event type cards visible
    When I navigate to the marketing home page
    Then I see text "Workouts"
    And I see text "Reading"
    And I see text "Learning"
    And I see text "Meals"
    And I see text "Focus"

  Scenario: Custom event card visible
    When I navigate to the marketing home page
    Then I see text "Plus your own."

  Scenario: Weekly rhythm demo visible
    When I navigate to the marketing home page
    Then I see text "Last 7 days"

  Scenario: All six principles visible
    When I navigate to the marketing home page
    Then I see text "Local-first"
    And I see text "Yours to take"
    And I see text "Flexible"
    And I see text "Quiet"
    And I see text "Open"
    And I see text "Multilingual"
