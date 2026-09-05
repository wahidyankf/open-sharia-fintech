Feature: Skills category landing fixed-arc statement

  As a reader exploring skills paths
  I want the skills category landing to state its one ramp promise plainly, with no chooser
  So that I'm not asked to pick among arcs that don't exist for this category

  # Bound Phase 3, Cycle 3.1b-ii — unit (category-landing.test.tsx) and e2e (course-paths.steps.ts).
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The skills category landing states its fixed arc once, with no chooser
  @integration-exempt
  Scenario: The skills category landing states its fixed arc once, with no chooser
    Given a fixture skills manifest set is loaded
    When a reader opens the skills category landing at /en/learn/paths/skills/
    Then the page renders the ramp promise once as a statement, not a question
    And no arc-selection control is present anywhere on the page
