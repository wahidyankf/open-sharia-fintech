Feature: ProgressRing component

  Scenario: Full progress ring
    When I render a ProgressRing with progress 1
    Then the progressbar should have aria-valuenow "100"

  Scenario: Half progress ring
    When I render a ProgressRing with progress 0.5
    Then the progressbar should have aria-valuenow "50"

  Scenario: Empty progress ring
    When I render a ProgressRing with progress 0
    Then the progressbar should have aria-valuenow "0"

  Scenario: Has correct aria attributes
    When I render a ProgressRing with progress 0.75
    Then the progressbar should have aria-valuemin "0"
    And the progressbar should have aria-valuemax "100"
